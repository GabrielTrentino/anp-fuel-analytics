"""Identifica postos amostrados pelo PMQC que NÃO constam no cadastro oficial."""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

REPO = Path(__file__).resolve().parents[3]
TRUSTED = REPO / "data" / "trusted"


def main() -> None:
    pmqc = pd.read_parquet(TRUSTED / "pmqc" / "pmqc.parquet")
    cad = pd.read_parquet(TRUSTED / "cadastro-revendas-combustiveis" / "revendas.parquet")

    pmqc_cnpj = set(pmqc["cnpj"].dropna().unique())
    cad_cnpj = set(cad["cnpj"].dropna().unique())

    only_pmqc = pmqc_cnpj - cad_cnpj
    overlap = pmqc_cnpj & cad_cnpj

    print(f"CNPJs PMQC: {len(pmqc_cnpj):,}")
    print(f"CNPJs Cadastro: {len(cad_cnpj):,}")
    print(f"Overlap: {len(overlap):,} ({len(overlap)/len(pmqc_cnpj)*100:.1f}%)")
    print(f"Só no PMQC: {len(only_pmqc):,}")
    print()

    fora = pmqc[pmqc["cnpj"].isin(only_pmqc)].drop_duplicates(subset=["cnpj"])
    print(f"Postos PMQC fora do cadastro por UF:")
    print(fora["uf"].value_counts().head(10).to_string())
    print()

    fora_nc = pmqc[(pmqc["cnpj"].isin(only_pmqc)) & (~pmqc["conforme"])]
    print(f"Ensaios não-conformes em postos fora do cadastro: {len(fora_nc):,}")

    out = REPO / "data" / "refined" / "pmqc" / "postos_fora_cadastro.csv"
    out.parent.mkdir(parents=True, exist_ok=True)
    fora[["cnpj", "razao_social", "municipio", "uf", "distribuidora"]].to_csv(out, index=False)
    print(f"\n-> {out.relative_to(REPO)} ({len(fora)} postos)")


if __name__ == "__main__":
    main()
