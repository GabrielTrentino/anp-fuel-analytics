"""Perfil rapido dos CSVs MVP de precos (colunas, CNPJ, separador)."""
from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[3]
RAW = REPO_ROOT / "data/raw/serie-historica-precos"


def sniff_csv(path: Path) -> dict:
    for enc in ("utf-8", "latin-1", "cp1252"):
        for sep in (";", ","):
            try:
                df = pd.read_csv(path, sep=sep, nrows=5000, dtype=str, encoding=enc, low_memory=False)
                if df.shape[1] < 2:
                    continue
                cols = list(df.columns)
                cnpj_cols = [c for c in cols if "cnpj" in c.lower()]
                return {
                    "file": path.relative_to(RAW).as_posix(),
                    "encoding": enc,
                    "sep": sep,
                    "cols": cols,
                    "rows_sample": len(df),
                    "cnpj_cols": cnpj_cols,
                    "cnpj_unique": int(df[cnpj_cols[0]].nunique()) if cnpj_cols else None,
                }
            except Exception:
                continue
    return {"file": path.name, "error": "unreadable"}


def main() -> None:
    rows = []
    for path in sorted(RAW.rglob("*.csv")):
        rows.append(sniff_csv(path))
    print(json.dumps(rows, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
