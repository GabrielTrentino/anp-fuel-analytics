"""Inventário empírico do CSV cadastro revendas (stdout)."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[2]
RAW = REPO_ROOT / "data/raw/cadastro-revendas-combustiveis"
CSV = RAW / "dados-cadastrais-revendedores-varejistas-combustiveis-automoveis.csv"


def main() -> None:
    if not CSV.exists():
        print(f"Arquivo ausente: {CSV}", file=sys.stderr)
        sys.exit(1)
    df = pd.read_csv(CSV, sep=";", dtype=str, encoding="latin-1", low_memory=False)
    row = {
        "file": CSV.name,
        "linhas": len(df),
        "colunas": list(df.columns),
        "cnpj_unicos": int(df["CNPJ"].nunique()),
        "codigo_isimp_unicos": int(df["CODIGOISIMP"].nunique()),
        "ufs": int(df["UF"].nunique()),
        "bandeiras_top": df["BANDEIRA"].value_counts().head(8).to_dict(),
    }
    print(json.dumps(row, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
