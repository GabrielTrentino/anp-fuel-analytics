"""Compatibilidade: delega trusted para pipelines/sql (DuckDB)."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
SLUG = "tancagem-abastecimento"


def main() -> None:
    cmd = [
        sys.executable,
        str(REPO_ROOT / "pipelines" / "run.py"),
        SLUG,
        "raw_prepare",
        "trusted",
    ]
    subprocess.run(cmd, check=True, cwd=REPO_ROOT)


if __name__ == "__main__":
    main()
