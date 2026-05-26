"""Perfil dos CSVs de distribuidores de combustiveis liquidos."""
from __future__ import annotations

from pathlib import Path

import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[3]
RAW = REPO_ROOT / "data" / "raw" / "distribuidores-combustiveis-liquidos"


def main() -> None:
    for csv_path in sorted(RAW.glob("*.csv")):
        for enc in ("utf-8-sig", "utf-8", "latin-1"):
            for sep in (";", ","):
                try:
                    df = pd.read_csv(csv_path, sep=sep, dtype=str, encoding=enc, low_memory=False)
                    if df.shape[1] >= 3:
                        break
                except Exception:
                    continue
            else:
                continue
            break

        print(f"== {csv_path.name} ==")
        print(f"  Encoding: {enc}, sep: '{sep}'")
        print(f"  Linhas: {len(df):,}, Colunas: {df.shape[1]}")
        print(f"  Cols: {list(df.columns)}")
        for col in df.columns[:6]:
            print(f"    {col}: {df[col].nunique()} distintos, ex: {df[col].dropna().head(2).tolist()}")
        print()


if __name__ == "__main__":
    main()
