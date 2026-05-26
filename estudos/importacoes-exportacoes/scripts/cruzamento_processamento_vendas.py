"""Cruzamento importacoes-exportacoes x processamento x vendas."""
from __future__ import annotations

from pathlib import Path
import pandas as pd

REPO = Path(__file__).resolve().parents[3]
TRUSTED = REPO / "data" / "trusted"


def main() -> None:
    ie = pd.read_parquet(TRUSTED / "importacoes-exportacoes" / "ie_derivados.parquet")
    print(f"ie_derivados: {len(ie)} registros, {ie['ano'].min()}-{ie['ano'].max()}")
    print(f"  produtos: {ie['produto'].nunique()}")
    print(f"  operacoes: {ie['operacao'].unique().tolist()}")
    imp = ie[ie["operacao"].str.contains("IMPORT", case=False, na=False)]
    exp = ie[ie["operacao"].str.contains("EXPORT", case=False, na=False)]
    print(f"  volume importado total: {imp['volume_m3'].sum():,.0f} m3")
    print(f"  volume exportado total: {exp['volume_m3'].sum():,.0f} m3")
    print()

    ie_pet = pd.read_parquet(TRUSTED / "importacoes-exportacoes" / "ie_petroleo.parquet")
    print(f"ie_petroleo: {len(ie_pet)} registros, {ie_pet['ano'].min()}-{ie_pet['ano'].max()}")
    print()

    ie_eta = pd.read_parquet(TRUSTED / "importacoes-exportacoes" / "ie_etanol.parquet")
    print(f"ie_etanol: {len(ie_eta)} registros, {ie_eta['ano'].min()}-{ie_eta['ano'].max()}")
    print()

    proc_path = TRUSTED / "processamento-petroleo-derivados" / "processamento.parquet"
    if proc_path.exists():
        proc = pd.read_parquet(proc_path)
        print(f"Sobreposicao temporal proc x ie: {max(proc['ano'].min(), ie['ano'].min())}-{min(proc['ano'].max(), ie['ano'].max())}")


if __name__ == "__main__":
    main()
