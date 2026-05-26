"""Cruzamento distribuidores x movimentacao-derivados e cadastro-revendas."""
from __future__ import annotations

from pathlib import Path

import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[3]
DIST = REPO_ROOT / "data/trusted/distribuidores-combustiveis-liquidos/distribuidores.parquet"
MOV = REPO_ROOT / "data/trusted/movimentacao-derivados/liquidos_vendas_atual.parquet"


def main() -> None:
    dist = pd.read_parquet(DIST)
    lines = [
        "# Cruzamento distribuidores-combustiveis-liquidos",
        "",
        f"Base: `distribuidores.parquet` — **{len(dist):,}** distribuidores autorizados.",
        f"UFs: {dist['uf'].nunique()} | Situações: {dist['situacao'].value_counts().to_dict()}",
        "",
        "## Top-10 por UF",
        "",
        "| UF | Distribuidores |",
        "|-----|---------------|",
    ]
    for uf, n in dist["uf"].value_counts().head(10).items():
        lines.append(f"| {uf} | {n} |")
    lines.append("")

    # Movimentacao
    if MOV.exists():
        mov = pd.read_parquet(MOV)
        if "razao_social" in mov.columns:
            mov_names = set(mov["razao_social"].dropna().str.upper().unique())
        elif "distribuidora" in mov.columns:
            mov_names = set(mov["distribuidora"].dropna().str.upper().unique())
        else:
            mov_names = set()
        dist_names = set(dist["razao_social"].dropna().str.upper().unique())
        overlap_name = dist_names & mov_names
        lines += [
            "## Movimentacao derivados",
            "",
            f"Distribuidores no trusted: {len(dist_names):,}",
            f"Razoes sociais na movimentacao: {len(mov_names):,}",
            f"Match por razao social (exact upper): **{len(overlap_name)}**",
            "",
            "Join principal: `cnpj` (quando disponivel na movimentacao).",
            "",
        ]

    out = Path(__file__).resolve().parent.parent / "cruzamento_resultado.md"
    out.write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(lines))
    print(f"\n-> {out.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
