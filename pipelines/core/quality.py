"""Testes de qualidade de dados declarados no bloco ``quality`` de cada estudo.

Cada item aponta para uma tabela (Parquet) e lista regras:

    quality:
      - table: data/trusted/pmqc/pmqc.parquet
        min_rows: 1000000
        not_null: [data_coleta, id_numeric]
        unique: [id_numeric, ensaio]          # ou {columns: [...], severity: warn, note: ...}
        no_duplicate_rows: true
        accepted_values: {uf: [AC, AL, ...]}
        range: {valor_venda: {min: 0, max: 50}}

Toda regra aceita a forma longa ``{..., severity: error|warn, note: "..."}``.
``warn`` registra uma anomalia conhecida da fonte sem falhar o pipeline.
"""
from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path

import duckdb

RULES = ("min_rows", "not_null", "unique", "no_duplicate_rows", "accepted_values", "range")


@dataclass
class CheckResult:
    table: str
    rule: str
    detail: str
    passed: bool
    severity: str
    failing: int = 0
    note: str | None = None

    @property
    def status(self) -> str:
        if self.passed:
            return "ok"
        return "FALHA" if self.severity == "error" else "aviso"


def _split(spec, key: str):
    """Separa o valor da regra de ``severity``/``note`` (forma curta ou longa)."""
    if isinstance(spec, dict) and key in spec:
        return spec[key], spec.get("severity", "error"), spec.get("note")
    if isinstance(spec, dict) and ("severity" in spec or "note" in spec) and key == "enabled":
        return True, spec.get("severity", "error"), spec.get("note")
    return spec, "error", None


def _q(col: str) -> str:
    return '"' + col.replace('"', '""') + '"'


def run_checks(item: dict, repo_root: Path, con: duckdb.DuckDBPyConnection | None = None) -> list[CheckResult]:
    table = item["table"]
    path = (repo_root / table).as_posix()
    con = con or duckdb.connect()
    results: list[CheckResult] = []

    if not Path(path).exists():
        return [CheckResult(table, "exists", "arquivo existe", False, "error")]

    src = f"read_parquet('{path}')"
    total = con.sql(f"SELECT count(*) FROM {src}").fetchone()[0]
    columns = {r[0] for r in con.sql(f"DESCRIBE SELECT * FROM {src}").fetchall()}

    def missing(cols: list[str]) -> list[str]:
        return [c for c in cols if c not in columns]

    def add(rule, detail, failing, severity, note, ok=None):
        passed = failing == 0 if ok is None else ok
        results.append(CheckResult(table, rule, detail, passed, severity, failing, note))

    for rule in RULES:
        if rule not in item:
            continue
        spec = item[rule]

        if rule == "min_rows":
            value, sev, note = _split(spec, "value")
            add(rule, f">= {value:,} linhas (tem {total:,})", 0, sev, note, ok=total >= value)

        elif rule == "not_null":
            cols, sev, note = _split(spec, "columns")
            if bad := missing(cols):
                add(rule, f"colunas inexistentes: {bad}", len(bad), "error", note)
                continue
            for c in cols:
                n = con.sql(f"SELECT count(*) FROM {src} WHERE {_q(c)} IS NULL").fetchone()[0]
                add(rule, c, n, sev, note)

        elif rule == "unique":
            cols, sev, note = _split(spec, "columns")
            if bad := missing(cols):
                add(rule, f"colunas inexistentes: {bad}", len(bad), "error", note)
                continue
            key = ", ".join(_q(c) for c in cols)
            n = con.sql(f"SELECT count(*) - count(DISTINCT ({key})) FROM {src}").fetchone()[0]
            add(rule, "+".join(cols), n, sev, note)

        elif rule == "no_duplicate_rows":
            enabled, sev, note = _split(spec, "enabled")
            if enabled:
                distinct = con.sql(f"SELECT count(*) FROM (SELECT DISTINCT * FROM {src})").fetchone()[0]
                add(rule, "linhas idênticas", total - distinct, sev, note)

        elif rule == "accepted_values":
            mapping, sev, note = _split(spec, "values")
            for c, allowed in mapping.items():
                if c not in columns:
                    add(rule, f"coluna inexistente: {c}", 1, "error", note)
                    continue
                values = ", ".join("'" + str(v).replace("'", "''") + "'" for v in allowed)
                n = con.sql(
                    f"SELECT count(*) FROM {src} WHERE {_q(c)} IS NOT NULL AND {_q(c)} NOT IN ({values})"
                ).fetchone()[0]
                add(rule, f"{c} em {len(allowed)} valores", n, sev, note)

        elif rule == "range":
            mapping, sev, note = _split(spec, "columns")
            for c, bounds in mapping.items():
                if c not in columns:
                    add(rule, f"coluna inexistente: {c}", 1, "error", note)
                    continue
                conds = []
                if "min" in bounds:
                    conds.append(f"{_q(c)} < {bounds['min']}")
                if "max" in bounds:
                    conds.append(f"{_q(c)} > {bounds['max']}")
                n = con.sql(f"SELECT count(*) FROM {src} WHERE {' OR '.join(conds)}").fetchone()[0]
                add(rule, f"{c} em [{bounds.get('min', '-inf')}, {bounds.get('max', 'inf')}]", n, sev, note)

    unknown = set(item) - set(RULES) - {"table"}
    if unknown:
        add("config", f"regras desconhecidas: {sorted(unknown)}", len(unknown), "error", None)
    return results


def run_study(slug: str, study: dict, repo_root: Path, report_dir: Path | None = None) -> list[CheckResult]:
    con = duckdb.connect()
    results: list[CheckResult] = []
    for item in study.get("quality", []):
        results += run_checks(item, repo_root, con)
    if report_dir is not None:
        report_dir.mkdir(parents=True, exist_ok=True)
        payload = {
            "slug": slug,
            "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
            "results": [asdict(r) | {"status": r.status} for r in results],
        }
        (report_dir / f"{slug}.json").write_text(
            json.dumps(payload, indent=2, ensure_ascii=False, default=str) + "\n", encoding="utf-8"
        )
    return results


def print_results(results: list[CheckResult]) -> None:
    for r in results:
        extra = f" ({r.failing:,})" if not r.passed and r.failing else ""
        note = f" — {r.note}" if r.note and not r.passed else ""
        print(f"  [{r.status:5}] {Path(r.table).name:40} {r.rule:18} {r.detail}{extra}{note}")


def has_errors(results: list[CheckResult]) -> bool:
    return any(not r.passed and r.severity == "error" for r in results)
