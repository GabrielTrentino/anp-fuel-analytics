"""Catálogo DuckDB: um arquivo ``data/anp.duckdb`` com uma view por saída do pipeline.

As views apontam para os Parquets (nada é copiado), então o arquivo é pequeno e
fica atualizado sempre que o pipeline regrava as saídas. Uso:

    py pipelines/run.py catalog
    duckdb -ui data/anp.duckdb        # navegador de tabelas/linhas (DuckDB >= 1.2)

Também abre em DBeaver, Power BI (conector ODBC do DuckDB) ou em notebooks:
``duckdb.connect("data/anp.duckdb", read_only=True).sql("from pmqc.trusted_pmqc")``.
"""
from __future__ import annotations

import re
from pathlib import Path

import duckdb

CATALOG_PATH = Path("data") / "anp.duckdb"


def _ident(text: str) -> str:
    return re.sub(r"\W+", "_", text).strip("_").lower()


def catalog_entries(cfg: dict) -> list[tuple[str, str, str]]:
    """[(schema, view, caminho relativo)] para todas as saídas declaradas."""
    entries: list[tuple[str, str, str]] = []
    seen: set[tuple[str, str]] = set()
    for slug, study in cfg["studies"].items():
        schema = _ident(slug)
        for step in study["pipeline"]:
            for out in step.get("outputs", []):
                if not out.endswith(".parquet"):
                    continue
                layer = out.split("/")[1] if out.startswith("data/") else "out"
                view = _ident(f"{layer}_{Path(out).stem}")
                if (schema, view) in seen:
                    continue
                seen.add((schema, view))
                entries.append((schema, view, out))
    return entries


def build_catalog(cfg: dict, repo_root: Path) -> Path:
    target = repo_root / CATALOG_PATH
    target.parent.mkdir(parents=True, exist_ok=True)
    con = duckdb.connect(str(target))
    created = missing = 0
    try:
        for schema, view, rel in catalog_entries(cfg):
            path = (repo_root / rel).resolve()
            con.execute(f'CREATE SCHEMA IF NOT EXISTS "{schema}"')
            if not path.exists():
                con.execute(f'DROP VIEW IF EXISTS "{schema}"."{view}"')
                missing += 1
                continue
            con.execute(
                f'CREATE OR REPLACE VIEW "{schema}"."{view}" AS '
                f"SELECT * FROM read_parquet('{path.as_posix()}')"
            )
            created += 1
        quality_dir = repo_root / "data" / "quality"
        con.execute("CREATE SCHEMA IF NOT EXISTS meta")
        if any(quality_dir.glob("*.json")):
            con.execute(
                "CREATE OR REPLACE VIEW meta.quality AS "
                "SELECT slug, generated_at, unnest(results, recursive := true) "
                f"FROM read_json('{quality_dir.as_posix()}/*.json')"
            )
    finally:
        con.close()
    print(f"{created} views criadas, {missing} saídas ainda não geradas -> {CATALOG_PATH.as_posix()}")
    return target
