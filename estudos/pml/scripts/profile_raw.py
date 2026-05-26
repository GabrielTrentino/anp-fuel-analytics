"""Perfil do CSV PML."""
from __future__ import annotations

from pathlib import Path

import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[3]
RAW = REPO_ROOT / "data" / "raw" / "pml" / "dados-abertos-pml.csv"


def main() -> None:
    for enc in ("utf-8-sig", "utf-8", "latin-1"):
        for sep in (";", ","):
            try:
                df = pd.read_csv(RAW, sep=sep, dtype=str, encoding=enc, low_memory=False)
                if df.shape[1] >= 3:
                    break
            except Exception:
                continue
        else:
            continue
        break

    print(f"Encoding: {enc}, sep: '{sep}'")
    print(f"Linhas: {len(df):,}, Colunas: {df.shape[1]}")
    print(f"Cols: {list(df.columns)}")
    print()
    for col in df.columns:
        nuniq = df[col].nunique()
        sample = df[col].dropna().head(3).tolist()
        print(f"  {col}: {nuniq} distintos — ex: {sample}")


if __name__ == "__main__":
    main()
