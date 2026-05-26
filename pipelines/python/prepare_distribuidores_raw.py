"""Prepara os CSVs de distribuidores (header irregular em aea-filiais e inutilizadores)."""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "pipelines"))

from core.config import study_paths  # noqa: E402

SLUG = "distribuidores-combustiveis-liquidos"


def parse_report_style(path: Path, expected_cols: list[str]) -> pd.DataFrame:
    """Parse CSVs that have 2 header rows (ANP report format)."""
    df = pd.read_csv(path, sep=";", dtype=str, encoding="latin-1", header=None, low_memory=False)
    header_row = None
    for i in range(min(5, len(df))):
        row_vals = df.iloc[i].astype(str).tolist()
        if any("CNPJ" in str(v).upper() for v in row_vals):
            header_row = i
            break
    if header_row is None:
        return pd.DataFrame()
    headers = df.iloc[header_row].tolist()
    data = df.iloc[header_row + 1:].copy()
    data.columns = headers
    data = data.dropna(how="all")
    return data


def main() -> None:
    raw_dir = study_paths(SLUG)["raw"]
    out_dir = raw_dir / "_prepared"
    out_dir.mkdir(parents=True, exist_ok=True)

    # planilha-aea-filiais (distributors list)
    aea = raw_dir / "planilha-aea-filiais.csv"
    if aea.exists():
        df = parse_report_style(aea, [])
        if not df.empty:
            dest = out_dir / "distribuidores_aea.csv"
            df.to_csv(dest, index=False)
            print(f"-> {dest.relative_to(REPO_ROOT)} ({len(df):,} linhas)")

    # inutilizadores
    inut = raw_dir / "inutilizadores.csv"
    if inut.exists():
        df = parse_report_style(inut, [])
        if not df.empty:
            dest = out_dir / "inutilizadores.csv"
            df.to_csv(dest, index=False)
            print(f"-> {dest.relative_to(REPO_ROOT)} ({len(df):,} linhas)")


if __name__ == "__main__":
    main()
