"""Orquestrador de pipelines por estudo (config/monorepo.yaml).

    py pipelines/run.py <slug>                 # todas as etapas + testes de qualidade
    py pipelines/run.py <slug> trusted         # uma etapa (pode repetir: raw trusted)
    py pipelines/run.py <slug> check           # só os testes de qualidade
    py pipelines/run.py all [--skip-raw]       # todos os estudos
    py pipelines/run.py catalog                # recria data/anp.duckdb com uma view por saída
    py pipelines/run.py --list                 # estudos e etapas
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
import time
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "pipelines"))

from core import quality  # noqa: E402
from core.catalog import build_catalog  # noqa: E402
from core.config import load_config, study_config  # noqa: E402
from core.run_sql import run_sql_file  # noqa: E402

QUALITY_DIR = REPO_ROOT / "data" / "quality"


def _abs(rel: str) -> str:
    return (REPO_ROOT / rel).resolve().as_posix()


def step_outputs(step: dict) -> list[str]:
    """Saídas declaradas da etapa (aceita o formato antigo ``output``)."""
    outs = step.get("outputs")
    if outs is None:
        outs = [step["output"]] if "output" in step else []
    return list(outs)


def sql_vars(study: dict, step: dict) -> dict[str, str]:
    """Variáveis {{NOME}} disponíveis para o SQL da etapa.

    Padrão: RAW_DIR, TRUSTED_DIR, REFINED_DIR, TRUSTED_UF_DIR, UF_<UF> e
    TRUSTED_PARQUET (= primeira saída declarada). ``vars`` da etapa sobrescreve.
    """
    paths = study["paths"]
    out: dict[str, str] = {
        "RAW_DIR": _abs(paths["raw"]),
        "TRUSTED_DIR": _abs(paths["trusted"]),
        "REFINED_DIR": _abs(paths["refined"]),
    }
    if "trusted_uf" in paths:
        out["TRUSTED_UF_DIR"] = _abs(paths["trusted_uf"])
        for uf in study.get("trusted_uf_split", []):
            out[f"UF_{uf}"] = f"{out['TRUSTED_UF_DIR']}/{uf}.parquet"
    outs = step_outputs(step)
    if outs:
        out["TRUSTED_PARQUET"] = _abs(outs[0])
    for key, value in (step.get("vars") or {}).items():
        out[key] = _abs(value) if "/" in str(value) else str(value)
    return out


def sql_placeholders(sql_path: Path) -> set[str]:
    return set(re.findall(r"\{\{(\w+)\}\}", sql_path.read_text(encoding="utf-8")))


def run_step(slug: str, study: dict, step: dict) -> None:
    name, engine = step["step"], step["engine"]
    print(f"\n== {slug} / {name} ({engine}) ==")
    started = time.time()

    if engine == "download":
        cmd = [sys.executable, str(REPO_ROOT / "pipelines/python/download.py"), slug, *step.get("args", [])]
        subprocess.run(cmd, check=True, cwd=REPO_ROOT)
    elif engine == "python":
        cmd = [sys.executable, str(REPO_ROOT / step["script"]), *step.get("args", [])]
        print("python", step["script"], *step.get("args", []))
        subprocess.run(cmd, check=True, cwd=REPO_ROOT)
    elif engine == "sql":
        for key in ("trusted", "refined", "trusted_uf"):
            if key in study["paths"]:
                (REPO_ROOT / study["paths"][key]).mkdir(parents=True, exist_ok=True)
        for out in step_outputs(step):
            (REPO_ROOT / out).parent.mkdir(parents=True, exist_ok=True)
        run_sql_file(REPO_ROOT / step["script"], sql_vars(study, step))
    else:
        raise ValueError(f"Engine desconhecido: {engine}")

    # Contrato: toda saída declarada precisa existir e ter sido escrita agora.
    stale = [
        out
        for out in step_outputs(step)
        if not (REPO_ROOT / out).exists() or (REPO_ROOT / out).stat().st_mtime < started - 1
    ]
    if stale:
        raise SystemExit(f"Etapa {slug}/{name} não gerou as saídas declaradas: {stale}")
    for out in step_outputs(step):
        print(f"-> {out}")


def run_quality(slug: str, study: dict) -> bool:
    if not study.get("quality"):
        print(f"\n== {slug} / check: sem testes declarados ==")
        return True
    print(f"\n== {slug} / check ==")
    results = quality.run_study(slug, study, REPO_ROOT, QUALITY_DIR)
    quality.print_results(results)
    failed = quality.has_errors(results)
    print(f"-> data/quality/{slug}.json ({'FALHOU' if failed else 'ok'})")
    return not failed


def run_study(slug: str, steps_filter: list[str], skip_raw: bool = False) -> bool:
    study = study_config(slug)
    only_check = steps_filter == ["check"]
    steps = study["pipeline"]
    if steps_filter:
        unknown = set(steps_filter) - {s["step"] for s in steps} - {"check"}
        if unknown:
            raise SystemExit(f"Etapa(s) não encontrada(s) em {slug}: {sorted(unknown)}")
        steps = [s for s in steps if s["step"] in steps_filter]
    if skip_raw:
        steps = [s for s in steps if not s["step"].startswith("raw")]
    if not only_check:
        for step in steps:
            run_step(slug, study, step)
    if not steps_filter or "check" in steps_filter:
        return run_quality(slug, study)
    return True


def main() -> None:
    parser = argparse.ArgumentParser(description="Executa pipeline de um estudo")
    parser.add_argument("slug", nargs="?", help="slug do estudo, 'all' ou 'catalog'")
    parser.add_argument("steps", nargs="*", help="etapas (raw, trusted, ..., check). Omitir = todas")
    parser.add_argument("--list", action="store_true", help="lista estudos e etapas")
    parser.add_argument("--skip-raw", action="store_true", help="pula download/prepare (usa data/raw atual)")
    args = parser.parse_args()

    cfg = load_config()
    if args.list or not args.slug:
        for slug, study in cfg["studies"].items():
            print(f"{slug:40} {' → '.join(s['step'] for s in study['pipeline'])}")
        return
    if args.slug == "catalog":
        build_catalog(cfg, REPO_ROOT)
        return

    slugs = list(cfg["studies"]) if args.slug == "all" else [args.slug]
    ok = True
    for slug in slugs:
        ok = run_study(slug, args.steps, args.skip_raw) and ok
    if not ok:
        raise SystemExit("Testes de qualidade com falha (veja data/quality/).")


if __name__ == "__main__":
    main()
