"""Cruzamento movimentacao-terminais x capacidade x vendas-derivados."""
from __future__ import annotations

from pathlib import Path
import pandas as pd

REPO = Path(__file__).resolve().parents[3]
TRUSTED = REPO / "data" / "trusted"


def main() -> None:
    mov = pd.read_parquet(TRUSTED / "movimentacao-terminais-aquaviarios" / "movimentacao_terminais.parquet")
    print(f"movimentacao-terminais: {len(mov)} registros")
    print(f"  periodo: {mov['mes_referencia'].min()} a {mov['mes_referencia'].max()}")
    print(f"  terminais unicos: {mov['codigo_terminal'].nunique()}")
    print(f"  produtos unicos: {mov['produto'].nunique()}")
    print(f"  UFs: {sorted(mov['uf'].unique())}")
    print(f"  volume total: {mov['volume_m3'].sum():,.0f} m3")
    print()

    vendas_path = TRUSTED / "vendas-derivados" / "vendas_mensal.parquet"
    if vendas_path.exists():
        vendas = pd.read_parquet(vendas_path)
        mov_prods = set(mov["produto"].str.upper().str.strip().unique())
        vnd_prods = set(vendas["produto"].str.upper().str.strip().unique())
        print(f"Produtos movimentacao: {len(mov_prods)}")
        print(f"Produtos vendas: {len(vnd_prods)}")
        overlap = mov_prods & vnd_prods
        print(f"Produtos em comum: {len(overlap)}")
        if overlap:
            print(f"  exemplos: {list(overlap)[:5]}")
    else:
        print("vendas-derivados/vendas_mensal trusted nao encontrado.")


if __name__ == "__main__":
    main()
