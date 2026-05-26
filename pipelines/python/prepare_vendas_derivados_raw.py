"""Normaliza headers dos CSVs de vendas-derivados (BOM + encoding)."""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "pipelines"))

from core.config import study_paths  # noqa: E402

SLUG = "vendas-derivados"

MONTH_MAP = {
    "JAN": 1, "FEV": 2, "MAR": 3, "ABR": 4, "MAI": 5, "JUN": 6,
    "JUL": 7, "AGO": 8, "SET": 9, "OUT": 10, "NOV": 11, "DEZ": 12,
}

FILES = [
    ("vendas-combustiveis-m3-1990-2025.csv", "vendas_mensal.csv"),
    ("segmento/vendas-combustiveis-segmento-m3-2012-2025.csv", "vendas_segmento.csv"),
]


def normalize_cols(df: pd.DataFrame) -> pd.DataFrame:
    renames = {}
    for c in df.columns:
        low = c.strip().upper()
        if "ANO" in low:
            renames[c] = "ano"
        elif "MÊS" in low or "MES" in low or "M\xc3\x8aS" in low or low.startswith("M") and len(low) <= 4:
            renames[c] = "mes_abrev"
        elif "GRANDE" in low:
            renames[c] = "grande_regiao"
        elif "FEDERA" in low:
            renames[c] = "uf"
        elif "PRODUTO" in low:
            renames[c] = "produto"
        elif "SEGMENTO" in low:
            renames[c] = "segmento"
        elif "VENDAS" in low:
            renames[c] = "vendas_raw"
    return df.rename(columns=renames)


def parse_vendas(s: pd.Series) -> pd.Series:
    return pd.to_numeric(s.str.replace(",", "."), errors="coerce")


def main() -> None:
    raw_dir = study_paths(SLUG)["raw"]
    out_dir = raw_dir / "_prepared"
    out_dir.mkdir(parents=True, exist_ok=True)

    for src_rel, dst_name in FILES:
        src = raw_dir / src_rel
        if not src.exists():
            print(f"skip (ausente) {src_rel}")
            continue
        df = pd.read_csv(src, sep=";", dtype=str, encoding="utf-8-sig")
        df = normalize_cols(df)
        if "mes_abrev" in df.columns:
            df["mes"] = df["mes_abrev"].str.strip().str.upper().map(MONTH_MAP)
        if "vendas_raw" in df.columns:
            df["vendas_m3"] = parse_vendas(df["vendas_raw"])
        dest = out_dir / dst_name
        df.to_csv(dest, index=False)
        print(f"-> {dest.relative_to(REPO_ROOT)} ({len(df):,} linhas)")


if __name__ == "__main__":
    main()
