"""Download producao-biocombustiveis."""
from __future__ import annotations

import sys
import urllib.request
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "pipelines"))

from core.config import study_paths  # noqa: E402

SLUG = "producao-biocombustiveis"
BASE = "https://www.gov.br/anp/pt-br/centrais-de-conteudo/dados-abertos/arquivos/arquivos-producao-de-biocombustiveis"
USER_AGENT = "Mozilla/5.0 (anp-fuel-analytics; research)"

FILES = [
    "metadados-biodiesel.pdf",
    "metadados-producao-etanol.pdf",
    "producao-biodiesel-m3-2005-2023.csv",
    "producao-biodiesel-m3-2024-2026.csv",
    "producao-etanol-anidro-hidratado-m3-2012-2026.csv",
]


def download(url: str, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=180) as resp:
        dest.write_bytes(resp.read())


def main() -> None:
    root = study_paths(SLUG)["raw"]
    ok, fail = 0, 0
    for name in FILES:
        url = f"{BASE}/{name}"
        dest = root / name
        if dest.exists() and dest.stat().st_size > 0:
            print(f"skip {name}")
            ok += 1
            continue
        try:
            print(f"get  {name}")
            download(url, dest)
            ok += 1
        except Exception as e:
            print(f"FAIL {name}: {e}")
            fail += 1
    print(f"\n{ok} ok, {fail} falhas -> {root.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
