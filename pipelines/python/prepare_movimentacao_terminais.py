"""Converte xlsx (disfarçado de csv) de movimentacao-terminais para CSV real."""
from __future__ import annotations

import sys
import unicodedata
import re
from pathlib import Path

import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "pipelines"))

from core.config import study_paths  # noqa: E402

SLUG = "movimentacao-terminais-aquaviarios"


def normalize_col(name: str) -> str:
    s = unicodedata.normalize("NFKD", str(name))
    s = s.encode("ascii", "ignore").decode()
    s = re.sub(r"[^a-z0-9]+", "_", s.lower()).strip("_")
    return s


def main() -> None:
    paths = study_paths(SLUG)
    raw = paths["raw"]
    out_dir = raw / "_prepared"
    out_dir.mkdir(parents=True, exist_ok=True)

    src = raw / "dados-abertos-movimentacao-terminais-aquaviarios.csv"
    print(f"read {src.name} (xlsx format)")
    df = pd.read_excel(src)
    df.columns = [normalize_col(c) for c in df.columns]
    out = out_dir / "movimentacao_terminais.csv"
    df.to_csv(out, index=False, sep=";")
    print(f"ok -> {out.relative_to(REPO_ROOT)} ({len(df)} linhas, {len(df.columns)} colunas)")


if __name__ == "__main__":
    main()
