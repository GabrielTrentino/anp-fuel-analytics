"""Cruzamento fiscalizacao-abastecimento x pmqc x cadastro-revendas."""
from __future__ import annotations

from pathlib import Path
import pandas as pd

REPO = Path(__file__).resolve().parents[3]
TRUSTED = REPO / "data" / "trusted"


def main() -> None:
    fisc = pd.read_parquet(TRUSTED / "fiscalizacao-abastecimento" / "fiscalizacao.parquet")
    print(f"fiscalizacao: {len(fisc)} registros, {fisc['uf'].nunique()} UFs")
    print(f"  periodo: {fisc['data_fiscalizacao'].min()} a {fisc['data_fiscalizacao'].max()}")
    print(f"  segmentos: {fisc['segmento'].nunique()} unicos")
    print(f"  resultados top-5:")
    print(fisc["resultado"].value_counts().head())
    print()

    pmqc_path = TRUSTED / "pmqc" / "pmqc.parquet"
    if pmqc_path.exists():
        pmqc = pd.read_parquet(pmqc_path)
        fisc_cnpj = set(fisc["cnpj_cpf"].dropna().unique())
        pmqc_cnpj = set(pmqc["cnpj"].dropna().unique())
        overlap = fisc_cnpj & pmqc_cnpj
        print(f"Cruzamento CNPJ fiscalizacao x PMQC: {len(overlap)} CNPJs em comum")
        print(f"  ({len(overlap)/len(fisc_cnpj)*100:.1f}% dos fiscalizados encontrados no PMQC)")
    else:
        print("PMQC trusted nao encontrado, pulando cruzamento.")

    cad_path = TRUSTED / "cadastro-revendas-combustiveis" / "cadastro_revendas.parquet"
    if cad_path.exists():
        cad = pd.read_parquet(cad_path)
        cad_cnpj = set(cad["cnpj"].dropna().unique())
        fisc_cnpj = set(fisc["cnpj_cpf"].dropna().unique())
        overlap_cad = fisc_cnpj & cad_cnpj
        print(f"\nCruzamento CNPJ fiscalizacao x cadastro-revendas: {len(overlap_cad)} CNPJs")
        print(f"  ({len(overlap_cad)/len(fisc_cnpj)*100:.1f}% dos fiscalizados no cadastro)")
    else:
        print("cadastro-revendas trusted nao encontrado.")


if __name__ == "__main__":
    main()
