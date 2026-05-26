"""Cruzamento producao-biocombustiveis x vendas-derivados (etanol/biodiesel)."""
from __future__ import annotations

from pathlib import Path
import pandas as pd

REPO = Path(__file__).resolve().parents[3]
TRUSTED = REPO / "data" / "trusted"


def main() -> None:
    bio = pd.read_parquet(TRUSTED / "producao-biocombustiveis" / "producao_biodiesel.parquet")
    print(f"biodiesel: {len(bio)} registros, {bio['ano'].min()}-{bio['ano'].max()}")
    print(f"  regioes: {bio['grande_regiao'].nunique()}")
    print(f"  producao total: {bio['producao_m3'].sum():,.0f} m3")
    print()

    etanol = pd.read_parquet(TRUSTED / "producao-biocombustiveis" / "producao_etanol.parquet")
    print(f"etanol: {len(etanol)} registros, {etanol['ano'].min()}-{etanol['ano'].max()}")
    print(f"  UFs: {etanol['uf'].nunique()}")
    print(f"  produtos: {etanol['produto'].unique().tolist()}")
    print(f"  producao total: {etanol['producao_m3'].sum():,.0f} m3")
    print()

    vendas_path = TRUSTED / "vendas-derivados" / "vendas_mensal.parquet"
    if vendas_path.exists():
        vendas = pd.read_parquet(vendas_path)
        etanol_vendas = vendas[vendas["produto"].str.contains("ETANOL|HIDRATADO|ANIDRO", case=False, na=False)]
        print(f"vendas etanol (filtrado): {len(etanol_vendas)} registros")
        if len(etanol_vendas) > 0:
            print(f"  UFs vendas: {etanol_vendas['uf'].nunique()}")


if __name__ == "__main__":
    main()
