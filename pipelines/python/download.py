"""Download genérico guiado pelo bloco ``download`` do estudo em config/monorepo.yaml.

    py pipelines/python/download.py vendas-derivados [--force] [--check]
"""
from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "pipelines"))

from core.config import study_config  # noqa: E402
from core.download import main_for, remotes_from_config  # noqa: E402


def main() -> None:
    if len(sys.argv) < 2:
        raise SystemExit("uso: download.py <slug> [--force] [--check]")
    slug = sys.argv[1]
    block = study_config(slug).get("download")
    if not block:
        raise SystemExit(f"{slug} não tem bloco 'download' no monorepo.yaml")
    main_for(slug, remotes_from_config(block), timeout=block.get("timeout", 180), argv=sys.argv[2:])


if __name__ == "__main__":
    main()
