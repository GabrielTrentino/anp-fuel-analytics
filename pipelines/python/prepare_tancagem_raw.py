"""Prepara raw: converte XLSX (out/2022) em CSV para ingestão SQL."""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "pipelines"))

from core.config import study_paths  # noqa: E402

SLUG = "tancagem-abastecimento"
EXPECTED_COLS = [
    "Data",
    "NomeEmpresarial",
    "Uf",
    "Municipio",
    "Cnpj",
    "CodInstalacao",
    "Segmento",
    "DetalheInstalacao",
    "Tag",
    "TipoDaUnidade",
    "GrupoDeProdutos",
    "TancagemM3",
]

XLSX = (
    "2022/tancagem_terminais_dados_abertos_outubro_2022-csv.xlsx"
)
OUT_CSV = (
    "2022/tancagem_terminais_dados_abertos_outubro_2022-csv.csv"
)


def main() -> None:
    raw = study_paths(SLUG)["raw"]
    xlsx_path = raw / XLSX
    csv_path = raw / OUT_CSV

    if not xlsx_path.exists():
        print(f"skip (xlsx ausente): {xlsx_path.relative_to(REPO_ROOT)}")
        return

    raw_x = pd.read_excel(xlsx_path, header=4)
    df = raw_x[[c for c in raw_x.columns if c in EXPECTED_COLS]].copy()
    df = df.dropna(subset=["Data"])
    df.to_csv(csv_path, index=False, encoding="utf-8")
    print(f"ok  {csv_path.relative_to(REPO_ROOT)} ({len(df):,} linhas)")


if __name__ == "__main__":
    main()
