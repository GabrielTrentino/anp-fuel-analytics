"""Run a SQL file with DuckDB, replacing template variables."""
import sys
from pathlib import Path

import duckdb

sql_file = Path(sys.argv[1])
replacements = dict(a.split("=", 1) for a in sys.argv[2:])

sql = sql_file.read_text(encoding="utf-8")
for k, v in replacements.items():
    sql = sql.replace("{{" + k + "}}", v)

duckdb.sql(sql)
print(f"OK: {sql_file.name}")
