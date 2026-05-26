"""Prepare producao-por-poco: consolida CSVs extraidos dos ZIPs em um unico CSV."""
from __future__ import annotations

import sys
import re
import unicodedata
from pathlib import Path

import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "pipelines"))

from core.config import study_paths  # noqa: E402

SLUG = "producao-por-poco"

KEY_COLS = [
    "Estado", "Bacia", "Nome Poço", "Campo", "Operador",
    "Número do Contrato", "Período",
    "Óleo (bbl/dia)", "Condensado (bbl/dia)", "Petróleo (bbl/dia)",
    "Gás Natural (Mm³/dia)", "Água (bbl/dia)",
    "Instalação Destino", "Tipo Instalação",
    "Tempo de Produção (hs por mês)",
]


def normalize_col(name: str) -> str:
    s = unicodedata.normalize("NFKD", str(name))
    s = s.encode("ascii", "ignore").decode()
    s = re.sub(r"[^a-z0-9]+", "_", s.lower()).strip("_")
    return s


def main() -> None:
    paths = study_paths(SLUG)
    csv_dir = paths["raw"] / "csv"
    out_dir = paths["raw"] / "_prepared"
    out_dir.mkdir(parents=True, exist_ok=True)

    frames = []
    for f in sorted(csv_dir.rglob("*.csv")):
        try:
            df = pd.read_csv(f, sep=";", encoding="latin-1", low_memory=False)
            available = [c for c in KEY_COLS if c in df.columns]
            if len(available) < 5:
                continue
            frames.append(df[available])
        except Exception as e:
            print(f"  skip {f.name}: {e}")

    if not frames:
        print("WARN: nenhum CSV valido encontrado")
        return

    df = pd.concat(frames, ignore_index=True)
    df.columns = [normalize_col(c) for c in df.columns]
    out = out_dir / "producao_poco.csv"
    df.to_csv(out, index=False, sep=";")
    print(f"ok -> {out.relative_to(REPO_ROOT)} ({len(df)} linhas, {len(df.columns)} colunas)")


if __name__ == "__main__":
    main()
