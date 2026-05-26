"""Cruzamento producao-por-poco x producao-por-estado."""
from __future__ import annotations

from pathlib import Path
import pandas as pd

REPO = Path(__file__).resolve().parents[3]
TRUSTED = REPO / "data" / "trusted"


def main() -> None:
    poco = pd.read_parquet(TRUSTED / "producao-por-poco" / "producao_poco.parquet")
    print(f"producao por poco (amostra 2023): {len(poco)} registros")
    print(f"  estados: {sorted(poco['estado'].dropna().unique())}")
    print(f"  bacias: {poco['bacia'].nunique()}")
    print(f"  operadores: {poco['operador'].nunique()}")
    print(f"  campos: {poco['campo'].nunique()}")
    print(f"  petroleo total (bbl/dia sum): {poco['petroleo_bbl_dia'].sum():,.0f}")
    print()

    estado_path = TRUSTED / "producao-por-estado" / "producao_petroleo.parquet"
    if estado_path.exists():
        est = pd.read_parquet(estado_path)
        poco_ufs = set(poco["estado"].dropna().str.upper().str.strip().unique())
        est_ufs = set(est["uf"].str.upper().str.strip().unique())
        print(f"Estados no poco: {len(poco_ufs)}")
        print(f"UFs no estado: {len(est_ufs)}")
        print(f"Em comum: {len(poco_ufs & est_ufs)}")


if __name__ == "__main__":
    main()
