"""Download MVP da serie historica de precos (LPC) — amostra para exploracao."""
from __future__ import annotations

import sys
import urllib.request
import zipfile
from io import BytesIO
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "pipelines"))

from core.config import study_paths  # noqa: E402

SLUG = "serie-historica-precos"
BASE = "https://www.gov.br/anp/pt-br/centrais-de-conteudo/dados-abertos/arquivos/shpc"
USER_AGENT = "Mozilla/5.0 (anp-fuel-analytics; research)"

# (subdir local, path no portal)
FILES: list[tuple[str, str]] = [
    ("", "metadados-serie-historica-precos-combustiveis-1.pdf"),
    ("qus", "qus/ultimas-4-semanas-gasolina-etanol.csv"),
    ("qus", "qus/ultimas-4-semanas-diesel-gnv.csv"),
    ("qus", "qus/ultimas-4-semanas-glp.csv"),
    ("dsas/ca", "dsas/ca/ca-2024-01.csv"),
    ("dsas/ca", "dsas/ca/ca-2025-02.zip"),
    ("dsan/2025", "dsan/2025/precos-gasolina-etanol-12.csv"),
]


def download(url: str, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=180) as resp:
        data = resp.read()
    if dest.suffix.lower() == ".zip":
        with zipfile.ZipFile(BytesIO(data)) as zf:
            zf.extractall(dest.parent)
        dest.write_bytes(data)  # keep zip too
    else:
        dest.write_bytes(data)


def main() -> None:
    root = study_paths(SLUG)["raw"]
    ok, fail = 0, 0
    for sub, rel in FILES:
        url = f"{BASE}/{rel}"
        name = Path(rel).name
        dest = root / sub / name if sub else root / name
        if dest.exists() and dest.stat().st_size > 0:
            print(f"skip {dest.relative_to(REPO_ROOT)}")
            ok += 1
            continue
        try:
            print(f"get  {dest.relative_to(REPO_ROOT)}")
            download(url, dest)
            ok += 1
        except Exception as e:
            print(f"FAIL {rel}: {e}")
            fail += 1
    print(f"\n{ok} arquivos ok, {fail} falhas -> {root.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
