"""Executa arquivos .sql com DuckDB substituindo variáveis {{NOME}}."""
from __future__ import annotations

import re
from pathlib import Path

import duckdb


def render_sql(template: str, variables: dict[str, str]) -> str:
    def repl(match: re.Match[str]) -> str:
        key = match.group(1)
        if key not in variables:
            raise KeyError(f"Variável SQL não definida: {key}")
        return variables[key]

    return re.sub(r"\{\{(\w+)\}\}", repl, template)


def run_sql_file(sql_path: Path, variables: dict[str, str]) -> None:
    sql = render_sql(sql_path.read_text(encoding="utf-8"), variables)
    con = duckdb.connect()
    try:
        for statement in _split_statements(sql):
            if statement.strip():
                con.execute(statement)
    finally:
        con.close()


def _split_statements(sql: str) -> list[str]:
    parts: list[str] = []
    buf: list[str] = []
    for line in sql.splitlines():
        buf.append(line)
        if line.rstrip().endswith(";"):
            parts.append("\n".join(buf))
            buf = []
    if buf:
        parts.append("\n".join(buf))
    return parts
