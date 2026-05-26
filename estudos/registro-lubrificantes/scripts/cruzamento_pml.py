"""Cruzamento registro-lubrificantes x pml (monitoramento qualidade)."""
from __future__ import annotations

from pathlib import Path
import pandas as pd

REPO = Path(__file__).resolve().parents[3]
TRUSTED = REPO / "data" / "trusted"


def main() -> None:
    reg = pd.read_parquet(TRUSTED / "registro-lubrificantes" / "registro_lubrificantes.parquet")
    print(f"registro-lubrificantes: {len(reg)} registros")
    print(f"  situacoes: {reg['situacao'].value_counts().to_dict()}")
    print(f"  tipos produto: {reg['tipo_produto'].nunique()} unicos")
    print(f"  detentores: {reg['detentor'].nunique()} unicos")
    print(f"  periodo (ano): {reg['ano'].min()} a {reg['ano'].max()}")
    print()

    pml_path = TRUSTED / "pml" / "pml.parquet"
    if pml_path.exists():
        pml = pd.read_parquet(pml_path)
        print(f"PML: {len(pml)} amostras, periodo {pml['ano'].min()}-{pml['ano'].max()}")

        reg_cnpj = set(reg["cnpj_detentor"].dropna().unique())
        pml_cnpj = set(pml["cnpj_detentor"].dropna().unique())
        overlap = reg_cnpj & pml_cnpj
        print(f"\nCNPJ detentores no registro: {len(reg_cnpj)}")
        print(f"CNPJ detentores no PML: {len(pml_cnpj)}")
        print(f"Em comum: {len(overlap)} ({len(overlap)/max(len(pml_cnpj),1)*100:.1f}% dos PML)")

        reg_marcas = set(reg["marca_comercial"].str.upper().str.strip().unique())
        pml_marcas = set(pml["marca_comercial"].str.upper().str.strip().unique())
        marca_overlap = reg_marcas & pml_marcas
        print(f"\nMarcas no registro: {len(reg_marcas)}")
        print(f"Marcas no PML: {len(pml_marcas)}")
        print(f"Em comum: {len(marca_overlap)} ({len(marca_overlap)/max(len(pml_marcas),1)*100:.1f}% dos PML)")
    else:
        print("PML trusted nao encontrado.")


if __name__ == "__main__":
    main()
