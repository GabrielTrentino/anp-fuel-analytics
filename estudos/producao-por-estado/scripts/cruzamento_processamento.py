"""Cruzamento producao-por-estado x processamento."""
from __future__ import annotations

from pathlib import Path
import pandas as pd

REPO = Path(__file__).resolve().parents[3]
TRUSTED = REPO / "data" / "trusted"


def main() -> None:
    pet = pd.read_parquet(TRUSTED / "producao-por-estado" / "producao_petroleo.parquet")
    print(f"producao petroleo por estado: {len(pet)} registros")
    print(f"  periodo: {pet['ano'].min()}-{pet['ano'].max()}")
    print(f"  UFs: {sorted(pet['uf'].unique())}")
    print(f"  localizacoes: {pet['localizacao'].unique().tolist()}")
    print(f"  producao total: {pet['producao_m3'].sum():,.0f} m3")
    print()

    gn = pd.read_parquet(TRUSTED / "producao-por-estado" / "producao_gas_natural.parquet")
    print(f"producao gas natural por estado: {len(gn)} registros")
    print(f"  periodo: {gn['ano'].min()}-{gn['ano'].max()}")
    print(f"  producao total: {gn['producao_1000m3'].sum():,.0f} x1000 m3")
    print()

    proc_path = TRUSTED / "processamento-petroleo-derivados" / "processamento.parquet"
    if proc_path.exists():
        proc = pd.read_parquet(proc_path)
        pet_ufs = set(pet["uf"].unique())
        proc_ufs = set(proc["uf"].unique())
        print(f"UFs producao: {len(pet_ufs)}")
        print(f"UFs processamento: {len(proc_ufs)}")
        print(f"Em comum: {len(pet_ufs & proc_ufs)}")


if __name__ == "__main__":
    main()
