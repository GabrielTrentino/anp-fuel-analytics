"""Converte xlsx de fiscalizacao para CSV normalizado."""
from __future__ import annotations

import sys
import unicodedata
import re
from pathlib import Path

import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "pipelines"))

from core.config import study_paths  # noqa: E402

SLUG = "fiscalizacao-abastecimento"


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

    frames = []
    for f in sorted(raw.glob("*.xlsx")):
        print(f"read {f.name}")
        df = pd.read_excel(f)
        frames.append(df)

    if not frames:
        print("WARN: nenhum xlsx encontrado")
        return

    df = pd.concat(frames, ignore_index=True)
    df.columns = [normalize_col(c) for c in df.columns]
    out = out_dir / "fiscalizacao.csv"
    df.to_csv(out, index=False, sep=";")
    print(f"ok -> {out.relative_to(REPO_ROOT)} ({len(df)} linhas, {len(df.columns)} colunas)")


if __name__ == "__main__":
    main()
