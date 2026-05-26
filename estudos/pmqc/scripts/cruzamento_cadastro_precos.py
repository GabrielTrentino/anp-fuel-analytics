"""Cruzamento PMQC x cadastro-revendas x serie-historica-precos."""
from __future__ import annotations

from pathlib import Path

import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[3]
PMQC = REPO_ROOT / "data/trusted/pmqc/pmqc.parquet"
CADASTRO = REPO_ROOT / "data/trusted/cadastro-revendas-combustiveis/cadastro_revendas.parquet"
PRECOS = REPO_ROOT / "data/trusted/serie-historica-precos/lpc_posto.parquet"


def main() -> None:
    pmqc = pd.read_parquet(PMQC, columns=["cnpj", "uf", "data_coleta", "grupo_produto", "conforme"])
    lines = [
        "# Cruzamento PMQC x cadastro-revendas e precos",
        "",
        f"Base: `pmqc.parquet` — **{len(pmqc):,}** ensaios, {pmqc['data_coleta'].min()} – {pmqc['data_coleta'].max()}.",
        f"Postos distintos (CNPJ): **{pmqc['cnpj'].nunique():,}**",
        "",
    ]

    # Cadastro
    if CADASTRO.exists():
        cad = pd.read_parquet(CADASTRO)
        cnpj_col = "cnpj" if "cnpj" in cad.columns else cad.columns[0]
        cad_cnpjs = set(cad[cnpj_col].dropna().unique())
        pmqc_cnpjs = set(pmqc["cnpj"].dropna().unique())
        overlap = pmqc_cnpjs & cad_cnpjs
        lines += [
            "## Cadastro revendas",
            "",
            f"| Metrica | PMQC | Cadastro | Sobreposição |",
            f"|---------|------|----------|--------------|",
            f"| CNPJs distintos | {len(pmqc_cnpjs):,} | {len(cad_cnpjs):,} | **{len(overlap):,}** ({len(overlap)/len(pmqc_cnpjs)*100:.1f}%) |",
            "",
            "Join: `cnpj` — postos amostrados no PMQC que constam no cadastro.",
            "",
        ]

    # Precos
    if PRECOS.exists():
        pre = pd.read_parquet(PRECOS, columns=["cnpj", "uf", "data_coleta"])
        pre_cnpjs = set(pre["cnpj"].dropna().unique())
        pmqc_cnpjs = set(pmqc["cnpj"].dropna().unique())
        overlap_pre = pmqc_cnpjs & pre_cnpjs
        lines += [
            "## Serie historica precos (LPC)",
            "",
            f"| Metrica | PMQC | Precos | Sobreposição |",
            f"|---------|------|--------|--------------|",
            f"| CNPJs distintos | {len(pmqc_cnpjs):,} | {len(pre_cnpjs):,} | **{len(overlap_pre):,}** ({len(overlap_pre)/len(pmqc_cnpjs)*100:.1f}%) |",
            "",
            "Join: `cnpj` + `data_coleta` (semana) — correlacionar qualidade e preço.",
            "",
        ]

    # Nao conformidade por grupo
    nc = pmqc[~pmqc["conforme"]]
    if len(nc) > 0:
        lines += [
            "## Nao-conformidades",
            "",
            f"Total nao conforme: **{len(nc):,}** ({len(nc)/len(pmqc)*100:.3f}%)",
            "",
            "| Grupo produto | Nao conforme | % do grupo |",
            "|---------------|-------------|------------|",
        ]
        for gp in pmqc["grupo_produto"].unique():
            sub = pmqc[pmqc["grupo_produto"] == gp]
            nc_gp = sub[~sub["conforme"]]
            lines.append(f"| {gp} | {len(nc_gp)} | {len(nc_gp)/len(sub)*100:.3f}% |")
        lines.append("")

    out = Path(__file__).resolve().parent.parent / "cruzamento_resultado.md"
    out.write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(lines))
    print(f"\n-> {out.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
