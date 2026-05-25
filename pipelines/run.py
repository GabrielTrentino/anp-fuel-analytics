"""Orquestrador de pipelines por estudo (config/monorepo.yaml)."""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "pipelines"))

from core.config import REPO_ROOT, load_config, study_config  # noqa: E402
from core.run_sql import run_sql_file  # noqa: E402


def _run_python(script: str) -> None:
    path = REPO_ROOT / script
    print(f"python {path.relative_to(REPO_ROOT)}")
    subprocess.run([sys.executable, str(path)], check=True, cwd=REPO_ROOT)


def _sql_vars(slug: str, step: dict) -> dict[str, str]:
    study = study_config(slug)
    paths = study["paths"]

    def p(key: str) -> str:
        return str((REPO_ROOT / paths[key]).resolve()).replace("\\", "/")

    trusted_parquet = step.get("output")
    if trusted_parquet:
        trusted_parquet = str((REPO_ROOT / trusted_parquet).resolve()).replace("\\", "/")
    else:
        trusted_parquet = f"{p('trusted')}/tancagem.parquet"

    vars_: dict[str, str] = {
        "RAW_DIR": p("raw"),
        "TRUSTED_DIR": p("trusted"),
        "TRUSTED_PARQUET": trusted_parquet,
        "REFINED_DIR": p("refined"),
    }
    if "trusted_uf" in paths:
        vars_["TRUSTED_UF_DIR"] = p("trusted_uf")
    if slug == "tancagem-abastecimento":
        vars_["REFINED_PARQUET"] = f"{p('refined')}/tancagem_por_mes_uf_grupo_tag.parquet"
    for uf in study.get("trusted_uf_split", []):
        vars_[f"UF_{uf}"] = f"{p('trusted_uf')}/{uf}.parquet"
    return vars_


def run_step(slug: str, step: dict) -> None:
    name = step["step"]
    engine = step["engine"]
    print(f"\n== {slug} / {name} ({engine}) ==")

    if engine == "python":
        _run_python(step["script"])
        return

    if engine == "sql":
        sql_path = REPO_ROOT / step["script"]
        study = study_config(slug)
        paths = study["paths"]
        for key in ("trusted", "refined"):
            if key in paths:
                (REPO_ROOT / paths[key]).mkdir(parents=True, exist_ok=True)
        if "trusted_uf" in paths:
            (REPO_ROOT / paths["trusted_uf"]).mkdir(parents=True, exist_ok=True)
        out = step.get("output")
        if out:
            out_path = REPO_ROOT / out
            out_path.parent.mkdir(parents=True, exist_ok=True)
        run_sql_file(sql_path, _sql_vars(slug, step))
        if out:
            print(f"-> {out}")
        return

    raise ValueError(f"Engine desconhecido: {engine}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Executa pipeline de um estudo")
    parser.add_argument("slug", help="Slug do estudo (ex.: tancagem-abastecimento)")
    parser.add_argument(
        "step",
        nargs="?",
        help="Etapa (raw, raw_prepare, trusted, trusted_uf, refined). Omitir = todas",
    )
    args = parser.parse_args()

    study = study_config(args.slug)
    steps = study["pipeline"]
    if args.step:
        steps = [s for s in steps if s["step"] == args.step]
        if not steps:
            raise SystemExit(f"Etapa não encontrada: {args.step}")

    for step in steps:
        run_step(args.slug, step)


if __name__ == "__main__":
    main()
