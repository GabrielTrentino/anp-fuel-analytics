"""Cruzamento movimentacao (liquidos vendas) x tancagem trusted por nome + UF."""
from __future__ import annotations

import re
import unicodedata
from pathlib import Path

import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[3]
MOV_SAMPLE = (
    REPO_ROOT
    / "data/raw/movimentacao-derivados/liquidos/Liquidos_Vendas_Atual.csv"
)
TANCAGEM = REPO_ROOT / "data/trusted/tancagem-abastecimento/tancagem.parquet"


def norm_name(s: str) -> str:
    s = unicodedata.normalize("NFKD", str(s)).encode("ascii", "ignore").decode("ascii")
    s = re.sub(r"[^A-Z0-9 ]", " ", s.upper())
    return re.sub(r"\s+", " ", s).strip()


def read_mov() -> pd.DataFrame:
    line = MOV_SAMPLE.read_text(encoding="latin-1", errors="replace").splitlines()[0]
    sep = ";" if line.count(";") >= line.count(",") else ","
    return pd.read_csv(MOV_SAMPLE, encoding="latin-1", sep=sep, dtype=str, on_bad_lines="skip")


def main() -> None:
    if not MOV_SAMPLE.exists():
        raise FileNotFoundError(f"Baixe raw primeiro: {MOV_SAMPLE}")
    if not TANCAGEM.exists():
        raise FileNotFoundError(f"Rode pipeline tancagem trusted: {TANCAGEM}")

    mov = read_mov()
    agente_col = "Agente Regulado"
    uf_col = next(c for c in mov.columns if "UF Origem" in c or c.strip() == "UF Origem")
    mov_agents = (
        mov[[agente_col, uf_col]]
        .dropna()
        .drop_duplicates()
        .assign(_key=lambda d: d[agente_col].map(norm_name) + "|" + d[uf_col].str.upper().str.strip())
    )

    tan = pd.read_parquet(TANCAGEM, columns=["NomeEmpresarial", "Uf"])
    tan_agents = (
        tan.dropna()
        .drop_duplicates()
        .assign(_key=lambda d: d["NomeEmpresarial"].map(norm_name) + "|" + d["Uf"].str.upper().str.strip())
    )

    mov_keys = set(mov_agents["_key"])
    tan_keys = set(tan_agents["_key"])
    matched = mov_keys & tan_keys

    print("=== Cruzamento Agente Regulado x NomeEmpresarial (nome normalizado + UF) ===")
    print(f"Movimentacao agentes unicos (nome+UF): {len(mov_keys):,}")
    print(f"Tancagem empresas unicas (nome+UF):     {len(tan_keys):,}")
    print(f"Match exato (intersecao):               {len(matched):,}")
    print(f"Taxa match / movimentacao:              {100 * len(matched) / len(mov_keys):.1f}%")
    print(f"Taxa match / tancagem:                  {100 * len(matched) / len(tan_keys):.1f}%")

    mov_n = set(mov[agente_col].map(norm_name).dropna().unique())
    tan_n = set(tan["NomeEmpresarial"].map(norm_name).dropna().unique())
    matched_n = mov_n & tan_n
    mov_only = mov_keys - tan_keys

    # agente movimentacao existe em alguma UF da tancagem (nome only, any UF)
    tan_by_name = tan.groupby(tan["NomeEmpresarial"].map(norm_name))["Uf"].apply(set)
    matched_any_uf = sum(1 for a in mov_n if a in tan_by_name.index)

    lines = [
        "# Cruzamento movimentacao x tancagem",
        "",
        "Amostra: `liquidos/Liquidos_Vendas_Atual.csv` x `tancagem.parquet` (trusted).",
        "Normalizacao: nome sem acento/pontuacao + UF.",
        "",
        "| Metrica | Valor |",
        "|---------|------:|",
        f"| Agentes unicos movimentacao (nome+UF origem) | {len(mov_keys):,} |",
        f"| Empresas unicas tancagem (nome+UF instalacao) | {len(tan_keys):,} |",
        f"| Match exato nome+UF | {len(matched):,} ({100 * len(matched) / len(mov_keys):.1f}% dos agentes mov) |",
        f"| Match so por nome (ignora UF) | {len(matched_n):,} ({100 * len(matched_n) / len(mov_n):.1f}% dos {len(mov_n):,} nomes mov) |",
        f"| Nome mov presente em tancagem (qualquer UF) | {matched_any_uf:,} ({100 * matched_any_uf / len(mov_n):.1f}%) |",
        "",
        "## Interpretacao",
        "",
        "- Movimentacao usa **UF Origem** do fluxo; tancagem usa **UF da instalacao** — por isso match nome+UF e moderado (~30%).",
        "- Para join operacional: priorizar **nome normalizado** + validar UF; ou aguardar **cadastro revendas** (CNPJ).",
        "",
        "## Amostra sem match (nome+UF)",
        "",
    ]
    for k in list(mov_only)[:8]:
        lines.append(f"- `{k}`")

    out = Path(__file__).resolve().parent.parent / "cruzamento_tancagem_resultado.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))
    print(f"\n-> {out.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
