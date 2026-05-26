"""Cruzamento processamento x vendas-derivados x importacoes-exportacoes."""
from __future__ import annotations

from pathlib import Path
import pandas as pd

REPO = Path(__file__).resolve().parents[3]
TRUSTED = REPO / "data" / "trusted"


def main() -> None:
    proc = pd.read_parquet(TRUSTED / "processamento-petroleo-derivados" / "processamento.parquet")
    print(f"processamento: {len(proc)} registros")
    print(f"  periodo: {proc['ano'].min()}-{proc['ano'].max()}")
    print(f"  refinarias: {proc['refinaria'].nunique()}")
    print(f"  UFs: {proc['uf'].nunique()}")
    print(f"  volume total: {proc['volume_m3'].sum():,.0f} m3")
    print()

    deriv = pd.read_parquet(TRUSTED / "processamento-petroleo-derivados" / "derivados_refinaria.parquet")
    print(f"derivados_refinaria: {len(deriv)} registros, {deriv['produto'].nunique()} produtos")
    print()

    vendas_path = TRUSTED / "vendas-derivados" / "vendas_mensal.parquet"
    if vendas_path.exists():
        vendas = pd.read_parquet(vendas_path)
        proc_prods = set(deriv["produto"].str.upper().str.strip().unique())
        vnd_prods = set(vendas["produto"].str.upper().str.strip().unique())
        print(f"Produtos derivados processamento: {len(proc_prods)}")
        print(f"Produtos vendas: {len(vnd_prods)}")
        print(f"Em comum: {len(proc_prods & vnd_prods)}")

    ie_path = TRUSTED / "importacoes-exportacoes" / "ie_derivados.parquet"
    if ie_path.exists():
        ie = pd.read_parquet(ie_path)
        print(f"\nimportacoes-exportacoes derivados: {len(ie)} registros")
        print(f"  periodo: {ie['ano'].min()}-{ie['ano'].max()}")
        print(f"  produtos: {ie['produto'].nunique()}")


if __name__ == "__main__":
    main()
