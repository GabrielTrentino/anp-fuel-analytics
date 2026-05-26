"""Download importacoes-exportacoes (4 CSVs)."""
from __future__ import annotations

import sys
import urllib.request
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "pipelines"))

from core.config import study_paths  # noqa: E402

SLUG = "importacoes-exportacoes"
BASE_IE = "https://www.gov.br/anp/pt-br/centrais-de-conteudo/dados-abertos/arquivos/ie"
USER_AGENT = "Mozilla/5.0 (anp-fuel-analytics; research)"

FILES = [
    ("derivados/metadados-importacao-exportacao-derivados-1.pdf", "metadados-derivados.pdf"),
    ("derivados/importacoes-exportacoes-derivados-2000-2025.csv", "importacoes-exportacoes-derivados.csv"),
    ("etanol/metadados-importacao-exportacao-etanol-1.pdf", "metadados-etanol.pdf"),
    ("etanol/importacoes-exportacoes-etanol-2012-2025.csv", "importacoes-exportacoes-etanol.csv"),
    ("gn/metadados-importacao-gas-natural-1.pdf", "metadados-gas-natural.pdf"),
    ("gn/importacao-gas-natural-2000-2025.csv", "importacao-gas-natural.csv"),
    ("petroleo/metadados-importacao-exportacao-petroleo-1.pdf", "metadados-petroleo.pdf"),
    ("petroleo/importacoes-exportacoes-petroleo-2000-2025.csv", "importacoes-exportacoes-petroleo.csv"),
]


def download(url: str, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=180) as resp:
        dest.write_bytes(resp.read())


def main() -> None:
    root = study_paths(SLUG)["raw"]
    ok, fail = 0, 0
    for rel_path, local_name in FILES:
        url = f"{BASE_IE}/{rel_path}"
        dest = root / local_name
        if dest.exists() and dest.stat().st_size > 0:
            print(f"skip {local_name}")
            ok += 1
            continue
        try:
            print(f"get  {local_name}")
            download(url, dest)
            ok += 1
        except Exception as e:
            print(f"FAIL {local_name}: {e}")
            fail += 1
    print(f"\n{ok} ok, {fail} falhas -> {root.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
