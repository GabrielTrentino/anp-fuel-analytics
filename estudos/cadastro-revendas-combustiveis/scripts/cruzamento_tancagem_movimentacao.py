"""Cruzamento cadastro revendas x tancagem (CNPJ) e movimentacao (nome -> CNPJ)."""
from __future__ import annotations

import re
import unicodedata
from pathlib import Path

import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[3]
REVENDAS = REPO_ROOT / "data/trusted/cadastro-revendas-combustiveis/revendas.parquet"
TANCAGEM = REPO_ROOT / "data/trusted/tancagem-abastecimento/tancagem.parquet"
MOV = REPO_ROOT / "data/trusted/movimentacao-derivados/liquidos_vendas_atual.parquet"


def norm_name(s: str) -> str:
    s = unicodedata.normalize("NFKD", str(s)).encode("ascii", "ignore").decode("ascii")
    s = re.sub(r"[^A-Z0-9 ]", " ", s.upper())
    return re.sub(r"\s+", " ", s).strip()


def main() -> None:
    rev = pd.read_parquet(REVENDAS, columns=["cnpj", "razao_social", "codigo_isimp", "uf", "municipio"])
    rev_cnpj = set(rev["cnpj"].dropna().astype(str))

    lines = [
        "# Cruzamento cadastro revendas x tancagem e movimentacao",
        "",
        f"Base: **{len(rev):,}** postos (`revendas.parquet`), CNPJ e CODIGOISIMP unicos.",
        "",
    ]

    if TANCAGEM.exists():
        tan = pd.read_parquet(TANCAGEM, columns=["Cnpj", "CodInstalacao", "NomeEmpresarial"])
        tan["Cnpj"] = tan["Cnpj"].astype(str).str.replace(r"\.0$", "", regex=True)
        tan_cnpj = set(tan["Cnpj"].dropna())
        match_tan = rev_cnpj & tan_cnpj
        lines += [
            "## Tancagem (por CNPJ)",
            "",
            f"| Metrica | Valor |",
            f"|---------|------:|",
            f"| CNPJs cadastro revendas | {len(rev_cnpj):,} |",
            f"| CNPJs distintos tancagem (snapshots) | {len(tan_cnpj):,} |",
            f"| **Intersecao CNPJ** | **{len(match_tan):,}** ({100*len(match_tan)/len(rev_cnpj):.1f}% revendas) |",
            "",
        ]
        # codigo isimp
        rev_isimp = set(rev["codigo_isimp"].dropna().astype(str))
        tan_isimp = set(tan["CodInstalacao"].astype(str).str.replace(r"\.0$", "", regex=True))
        match_isimp = rev_isimp & tan_isimp
        lines += [
            f"| CODIGOISIMP cadastro x CodInstalacao tancagem | {len(match_isimp):,} |",
            "",
            "Tancagem agrega instalacoes com **tancagem autorizada** (bases TRR, terminais, refinarias).",
            "Postos de rua no cadastro em geral **nao aparecem** na tancagem aberta — intersecao CNPJ nula e esperada.",
            "",
        ]

    if MOV.exists():
        mov = pd.read_parquet(MOV, columns=["agente_regulado"])
        mov_names = mov["agente_regulado"].dropna().map(norm_name).unique()
        rev_by_name = rev.assign(_n=rev["razao_social"].map(norm_name)).drop_duplicates("_n")
        name_to_cnpj = dict(zip(rev_by_name["_n"], rev_by_name["cnpj"]))
        mov_mapped = sum(1 for n in mov_names if n in name_to_cnpj)
        lines += [
            "## Movimentacao liquidos (agente -> CNPJ via cadastro)",
            "",
            f"| Metrica | Valor |",
            f"|---------|------:|",
            f"| Nomes agente unicos movimentacao | {len(mov_names):,} |",
            f"| Nomes com match razao social no cadastro | **{mov_mapped:,}** ({100*mov_mapped/len(mov_names):.1f}%) |",
            "",
            "Agentes em movimentacao sao em geral **distribuidores** (SIMP); o cadastro lista **postos de varejo**.",
            "Join direto agente -> posto e raro; o valor do cadastro e CNPJ para **precos LPC**, geo e fiscalizacao.",
            "",
        ]

    out = Path(__file__).resolve().parent.parent / "cruzamento_resultado.md"
    out.write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(lines))
    print(f"\n-> {out.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
