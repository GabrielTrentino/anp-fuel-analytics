"""Commit incremental: estudo stub README por slug (etapa Fuel planejada)."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

FUEL_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(FUEL_ROOT.parent / "anp-data-atlas" / "scripts"))
from _conjuntos_fuel_metadata import CONJUNTOS_FUEL  # noqa: E402


def main() -> None:
    for c in CONJUNTOS_FUEL:
        slug = c["slug"]
        path = FUEL_ROOT / "estudos" / slug / "README.md"
        if not path.exists():
            raise FileNotFoundError(path)
        subprocess.run(["git", "add", str(path.relative_to(FUEL_ROOT))], cwd=FUEL_ROOT, check=True)
        msg = (
            f"Estudo planejado: {slug} — stub README.\n\n"
            f"Referencia doc atlas e proximos passos para pipeline {c['title']}."
        )
        subprocess.run(["git", "commit", "-m", msg], cwd=FUEL_ROOT, check=True)
        print("committed", slug)


if __name__ == "__main__":
    main()
