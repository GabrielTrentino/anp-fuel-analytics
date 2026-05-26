"""Cruzamento cadastro-revendas-glp x vendas-derivados e tancagem."""
from __future__ import annotations

from pathlib import Path

import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[3]
GLP = REPO_ROOT / "data/trusted/cadastro-revendas-glp/cadastro_revendas_glp.parquet"
VENDAS = REPO_ROOT / "data/trusted/vendas-derivados/vendas_mensal.parquet"
TANCAGEM = REPO_ROOT / "data/trusted/tancagem-abastecimento"


def main() -> None:
    glp = pd.read_parquet(GLP)
    lines = [
        "# Cruzamento cadastro-revendas-glp",
        "",
        f"Base: `cadastro_revendas_glp.parquet` — **{len(glp):,}** revendas.",
        f"UFs: {glp['uf'].nunique()} | Distribuidoras: {glp['distribuidora'].nunique()}",
        f"Municipios: {glp['municipio'].nunique():,}",
        "",
        "## Distribuidoras (top-10)",
        "",
        "| Distribuidora | Revendas | % |",
        "|---------------|---------|---|",
    ]
    dist = glp["distribuidora"].value_counts().head(10)
    for name, count in dist.items():
        lines.append(f"| {name} | {count:,} | {count/len(glp)*100:.1f}% |")
    lines.append("")

    # Vendas GLP
    if VENDAS.exists():
        vd = pd.read_parquet(VENDAS)
        vd_glp = vd[vd["produto"].str.contains("GLP", case=False, na=False)]
        glp_ufs = set(glp["uf"].unique())
        vd_ufs = set(vd_glp["uf"].unique())
        lines += [
            "## Vendas de GLP (serie mensal)",
            "",
            f"UFs cadastro: {len(glp_ufs)} | UFs vendas GLP: {len(vd_ufs)}",
            f"Periodo vendas: {vd_glp['data_referencia'].min()} - {vd_glp['data_referencia'].max()}",
            "",
            "Join: `uf` — densidade revendas vs volume vendido por UF.",
            "",
        ]

    # Tancagem
    tanc_files = list(TANCAGEM.glob("*.parquet")) if TANCAGEM.exists() else []
    if tanc_files:
        tanc = pd.read_parquet(tanc_files[0])
        tanc_glp = tanc[tanc.get("grupo_produto", pd.Series(dtype=str)).str.contains("GLP|G.s", case=False, na=False)] if "grupo_produto" in tanc.columns else pd.DataFrame()
        lines += [
            "## Tancagem (capacidade armazenamento GLP)",
            "",
            f"Registros tancagem GLP: {len(tanc_glp):,}",
            "",
        ]

    out = Path(__file__).resolve().parent.parent / "cruzamento_resultado.md"
    out.write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(lines))
    print(f"\n-> {out.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
