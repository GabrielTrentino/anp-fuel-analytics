"""Prepara raw movimentacao-derivados: historico sem cabecalho e validacao de separador."""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "pipelines"))

from core.config import study_paths  # noqa: E402

SLUG = "movimentacao-derivados"

HISTORICO_IN = "liquidos/Liquidos_Vendas_Historico_2007_a_2017.csv"
HISTORICO_OUT = "liquidos/Liquidos_Vendas_Historico_2007_a_2017_normalizado.csv"

HISTORICO_COLS = [
    "Ano",
    "Mes",
    "Agente Regulado",
    "Codigo do Produto",
    "Nome do Produto",
    "Regiao Origem",
    "UF Origem",
    "Regiao Destinatario",
    "UF Destino",
    "Mercado Destinatario",
    "Quantidade de Produto (mil m3)",
]


def sniff_sep(path: Path) -> str:
    line = path.read_text(encoding="latin-1", errors="replace").splitlines()[0]
    return ";" if line.count(";") >= line.count(",") else ","


def main() -> None:
    raw = study_paths(SLUG)["raw"]
    src = raw / HISTORICO_IN
    dst = raw / HISTORICO_OUT

    if not src.exists():
        print(f"skip (ausente): {src.relative_to(REPO_ROOT)}")
        return

    sep = sniff_sep(src)
    df = pd.read_csv(src, encoding="latin-1", sep=sep, header=None, names=HISTORICO_COLS, dtype=str)
    vol_col = HISTORICO_COLS[-1]
    df[vol_col] = df[vol_col].str.replace(",", ".", regex=False)
    df.to_csv(dst, index=False, encoding="utf-8", sep=",")
    print(f"ok  {dst.relative_to(REPO_ROOT)} ({len(df):,} linhas, sep origem={sep!r})")

    # validacao rapida separador em vendas atual
    atual = raw / "liquidos" / "Liquidos_Vendas_Atual.csv"
    if atual.exists():
        sep_a = sniff_sep(atual)
        sample = pd.read_csv(atual, encoding="latin-1", sep=sep_a, nrows=5)
        print(f"check Liquidos_Vendas_Atual sep={sep_a!r} cols={len(sample.columns)}")


if __name__ == "__main__":
    main()
