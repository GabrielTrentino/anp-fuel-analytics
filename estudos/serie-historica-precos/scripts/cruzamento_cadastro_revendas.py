"""Cruzamento precos LPC x cadastro revendas por CNPJ."""
from __future__ import annotations

from pathlib import Path

import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[3]
PRECOS = REPO_ROOT / "data/trusted/serie-historica-precos/qus_gasolina_etanol.parquet"
REVENDAS = REPO_ROOT / "data/trusted/cadastro-revendas-combustiveis/revendas.parquet"


def norm_cnpj(s: pd.Series) -> pd.Series:
    return s.astype(str).str.replace(r"[^0-9]", "", regex=True)


def main() -> None:
    pre = pd.read_parquet(PRECOS, columns=["cnpj", "produto", "data_coleta", "valor_venda"])
    rev = pd.read_parquet(REVENDAS, columns=["cnpj", "razao_social", "uf", "bandeira"])

    pre_c = set(norm_cnpj(pre["cnpj"].dropna()))
    rev_c = set(norm_cnpj(rev["cnpj"].dropna()))
    match = pre_c & rev_c

    lines = [
        "# Cruzamento precos LPC x cadastro revendas (CNPJ)",
        "",
        f"Precos: `qus_gasolina_etanol.parquet` · Cadastro: `revendas.parquet`",
        "",
        "| Metrica | Valor |",
        "|---------|------:|",
        f"| CNPJs distintos precos (amostra qus) | {len(pre_c):,} |",
        f"| CNPJs cadastro revendas | {len(rev_c):,} |",
        f"| **Intersecao CNPJ** | **{len(match):,}** ({100*len(match)/len(pre_c):.1f}% precos · {100*len(match)/len(rev_c):.1f}% cadastro) |",
        f"| Linhas precos com CNPJ no cadastro | {(norm_cnpj(pre['cnpj']).isin(rev_c)).sum():,} / {len(pre):,} |",
        "",
        "Join recomendado: `precos.cnpj = revendas.cnpj` para enriquecer preco com bandeira/endereco cadastral.",
        "",
    ]
    out = Path(__file__).resolve().parent.parent / "cruzamento_cadastro_resultado.md"
    out.write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(lines))
    print(f"\n-> {out.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
