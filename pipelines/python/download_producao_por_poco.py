"""Download producao-por-poco (ZIPs mensais — amostra 2023 para MVP).

Os ZIPs ficam em zips/ e os CSVs extraidos em csv/.
"""
from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "pipelines"))

from core.download import Remote, main_for  # noqa: E402

SLUG = "producao-por-poco"
BASE = "https://www.gov.br/anp/pt-br/centrais-de-conteudo/dados-abertos/arquivos/arquivos-producao-de-petroleo-e-gas-natural-por-poco"

MONTHS_2023 = [f"2023/producao-{m:02d}.zip" for m in range(1, 13)]


def remotes() -> list[Remote]:
    return [
        Remote(f"{BASE}/{rel}", f"zips/{rel.split('/')[-1]}", extract_to="csv")
        for rel in MONTHS_2023
    ]


if __name__ == "__main__":
    main_for(SLUG, remotes(), timeout=300)
