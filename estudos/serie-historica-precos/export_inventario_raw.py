"""Inventario empirico dos CSVs LPC em data/raw/serie-historica-precos/."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[2]
RAW = REPO_ROOT / "data/raw/serie-historica-precos"


def scan(path: Path) -> dict:
    rel = path.relative_to(RAW).as_posix()
    for enc in ("utf-8", "latin-1"):
        try:
            df = pd.read_csv(path, sep=";", nrows=2000, dtype=str, encoding=enc)
            break
        except Exception:
            df = None
    if df is None or df.shape[1] < 2:
        return {"file": rel, "error": "read"}
    dates = pd.to_datetime(df.get("Data da Coleta"), errors="coerce", dayfirst=True)
    cnpj = df.get("CNPJ da Revenda")
    return {
        "file": rel,
        "linhas_amostra": len(df),
        "colunas": len(df.columns),
        "cnpj_cols": bool(cnpj is not None),
        "periodo": f"{dates.min()} – {dates.max()}" if dates.notna().any() else "—",
    }


def main() -> None:
    rows = [scan(p) for p in sorted(RAW.rglob("*.csv"))]
    print(json.dumps(rows, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
