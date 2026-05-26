"""Perfil dos CSVs PMQC baixados — schema, encoding, contagem."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[3]
RAW = REPO_ROOT / "data" / "raw" / "pmqc"


def profile_csv(path: Path) -> dict | None:
    for enc in ("utf-8-sig", "utf-8", "latin-1"):
        for sep in (";", ","):
            try:
                df = pd.read_csv(path, sep=sep, nrows=5, dtype=str, encoding=enc, low_memory=False)
                if df.shape[1] >= 3:
                    total = sum(1 for _ in open(path, encoding=enc)) - 1
                    return {
                        "file": str(path.relative_to(RAW)),
                        "enc": enc,
                        "sep": sep,
                        "rows": total,
                        "cols": list(df.columns),
                    }
            except Exception:
                pass
    return None


def main() -> None:
    results = []
    for p in sorted(RAW.rglob("*.csv")):
        info = profile_csv(p)
        if info:
            results.append(info)
    print(json.dumps(results, ensure_ascii=False, indent=2))
    print(f"\n--- {len(results)} CSVs perfilados")

    if results:
        first = results[0]
        last = results[-1]
        print(f"\nPrimeiro: {first['file']} — {first['rows']} linhas, {len(first['cols'])} colunas")
        print(f"Ultimo:   {last['file']} — {last['rows']} linhas, {len(last['cols'])} colunas")
        print(f"\nColunas do primeiro: {first['cols']}")
        print(f"Colunas do ultimo:   {last['cols']}")


if __name__ == "__main__":
    main()
