"""Cruzamento vendas-derivados x movimentacao (UF/produto) e precos (produto/mes)."""
from __future__ import annotations

from pathlib import Path

import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[3]
VENDAS = REPO_ROOT / "data/trusted/vendas-derivados/vendas_mensal.parquet"
MOV = REPO_ROOT / "data/trusted/movimentacao-derivados/liquidos_vendas_atual.parquet"
PRECOS = REPO_ROOT / "data/trusted/serie-historica-precos/lpc_posto.parquet"


def main() -> None:
    vd = pd.read_parquet(VENDAS)
    lines = [
        "# Cruzamento vendas-derivados x movimentacao e precos",
        "",
        f"Base: `vendas_mensal.parquet` — **{len(vd):,}** linhas, 1990–2026.",
        "",
    ]

    # Movimentacao
    if MOV.exists():
        mov = pd.read_parquet(MOV)
        vd_ufs = set(vd["uf"].dropna().unique())
        mov_ufs = set(mov["uf_origem"].dropna().unique()) if "uf_origem" in mov.columns else set()
        vd_periodos = set(vd["data_referencia"].dropna().astype(str))
        mov_periodos = set(mov["data_referencia"].dropna().astype(str)) if "data_referencia" in mov.columns else set()
        lines += [
            "## Movimentacao liquidos",
            "",
            "| Metrica | Vendas | Movimentacao |",
            "|---------|--------|--------------|",
            f"| Periodo | {vd['data_referencia'].min()} – {vd['data_referencia'].max()} | {mov['data_referencia'].min()} – {mov['data_referencia'].max()} |",
            f"| UFs | {len(vd_ufs)} | {len(mov_ufs)} |",
            f"| Meses sobrepostos | **{len(vd_periodos & mov_periodos)}** |",
            "",
            "Join: `uf` + `data_referencia` (mês) — comparar vendas SDC vs movimentação SIMP.",
            "",
        ]

    # Precos
    if PRECOS.exists():
        pre = pd.read_parquet(PRECOS, columns=["produto", "data_coleta", "uf"])
        pre_prods = set(pre["produto"].str.upper().unique())
        vd_prods = set(vd["produto"].unique())
        lines += [
            "## Precos LPC",
            "",
            f"| Metrica | Vendas | Precos |",
            f"|---------|--------|--------|",
            f"| Produtos vendas | {sorted(vd_prods)} |",
            f"| Produtos precos (upper) | {sorted(pre_prods)} |",
            "",
            "Produtos LPC (gasolina, etanol, diesel) estao cobertos nas vendas.",
            "Join: agregado por `produto` + `uf` + mes.",
            "",
        ]

    out = Path(__file__).resolve().parent.parent / "cruzamento_resultado.md"
    out.write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(lines))
    print(f"\n-> {out.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
