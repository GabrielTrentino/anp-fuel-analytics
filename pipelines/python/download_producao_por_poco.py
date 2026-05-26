"""Download producao-por-poco (ZIPs mensais — amostra 2023 para MVP)."""
from __future__ import annotations

import sys
import urllib.request
import zipfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "pipelines"))

from core.config import study_paths  # noqa: E402

SLUG = "producao-por-poco"
BASE = "https://www.gov.br/anp/pt-br/centrais-de-conteudo/dados-abertos/arquivos/arquivos-producao-de-petroleo-e-gas-natural-por-poco"
USER_AGENT = "Mozilla/5.0 (anp-fuel-analytics; research)"

MONTHS_2023 = [f"2023/producao-{m:02d}.zip" for m in range(1, 13)]


def download(url: str, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=300) as resp:
        dest.write_bytes(resp.read())


def main() -> None:
    root = study_paths(SLUG)["raw"]
    zip_dir = root / "zips"
    csv_dir = root / "csv"
    zip_dir.mkdir(parents=True, exist_ok=True)
    csv_dir.mkdir(parents=True, exist_ok=True)

    ok, fail = 0, 0
    for rel in MONTHS_2023:
        name = rel.split("/")[-1]
        url = f"{BASE}/{rel}"
        dest = zip_dir / name
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

    print(f"\n{ok} ok, {fail} falhas (downloads)")
    print("extracting zips...")
    for zf in sorted(zip_dir.glob("*.zip")):
        try:
            with zipfile.ZipFile(zf) as z:
                z.extractall(csv_dir)
        except Exception as e:
            print(f"  extract FAIL {zf.name}: {e}")

    csvs = list(csv_dir.rglob("*.csv"))
    print(f"  {len(csvs)} CSVs extracted -> {csv_dir.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
