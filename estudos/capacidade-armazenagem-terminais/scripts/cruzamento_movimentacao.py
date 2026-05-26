"""Cruzamento capacidade-armazenagem x movimentacao-terminais."""
from __future__ import annotations

from pathlib import Path
import pandas as pd

REPO = Path(__file__).resolve().parents[3]
TRUSTED = REPO / "data" / "trusted"


def main() -> None:
    cap = pd.read_parquet(TRUSTED / "capacidade-armazenagem-terminais" / "capacidade.parquet")
    print(f"capacidade: {len(cap)} terminais, {cap['uf'].nunique()} UFs")
    print(f"  tipos: {cap['tipo'].value_counts().to_dict()}")
    print(f"  capacidade total derivados: {cap['capacidade_derivados_m3'].sum():,.0f} m3")
    print(f"  capacidade total GLP: {cap['capacidade_glp_m3'].sum():,.0f} m3")
    print()

    mov_path = TRUSTED / "movimentacao-terminais-aquaviarios" / "movimentacao_terminais.parquet"
    if mov_path.exists():
        mov = pd.read_parquet(mov_path)
        print(f"movimentacao: {len(mov)} registros, {mov['uf'].nunique()} UFs")
        print(f"  periodo: {mov['mes_referencia'].min()} a {mov['mes_referencia'].max()}")

        cap_ufs = set(cap["uf"].unique())
        mov_ufs = set(mov["uf"].unique())
        print(f"\nUFs em capacidade: {sorted(cap_ufs)}")
        print(f"UFs em movimentacao: {sorted(mov_ufs)}")
        print(f"UFs em comum: {sorted(cap_ufs & mov_ufs)} ({len(cap_ufs & mov_ufs)})")

        cap_ops = set(cap["operador"].str.upper().str.strip().unique())
        mov_inst = set(mov["nome_instalacao"].str.upper().str.strip().unique())
        overlap_names = cap_ops & mov_inst
        print(f"\nOperadores (capacidade) presentes em nome_instalacao (movimentacao): {len(overlap_names)}")
    else:
        print("movimentacao-terminais trusted nao encontrado.")


if __name__ == "__main__":
    main()
