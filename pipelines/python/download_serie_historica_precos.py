"""Download serie historica de precos (LPC) — MVP + dsan mensal."""
from __future__ import annotations

import argparse
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

DSAN_FAMILIES = (
    "precos-gasolina-etanol",
    "precos-diesel-gnv",
    "precos-glp",
)

STATIC: list[tuple[str, str]] = [
    ("", "metadados-serie-historica-precos-combustiveis-1.pdf"),
    ("qus", "qus/ultimas-4-semanas-gasolina-etanol.csv"),
    ("qus", "qus/ultimas-4-semanas-diesel-gnv.csv"),
    ("qus", "qus/ultimas-4-semanas-glp.csv"),
    ("dsas/ca", "dsas/ca/ca-2025-02.zip"),
]


def dsan_files(years: list[int], months: range | None = None) -> list[tuple[str, str]]:
    """Gera paths dsan/YYYY/precos-*-MM.csv."""
    months = months or range(1, 13)
    out: list[tuple[str, str]] = []
    for year in years:
        for fam in DSAN_FAMILIES:
            for m in months:
                rel = f"dsan/{year}/{fam}-{m:02d}.csv"
                out.append((f"dsan/{year}", rel))
    return out


def all_files(years: list[int] | None) -> list[tuple[str, str]]:
    files = list(STATIC)
    if years:
        files.extend(dsan_files(years))
    return files


def download(url: str, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=180) as resp:
        data = resp.read()
    if dest.suffix.lower() == ".zip":
        with zipfile.ZipFile(BytesIO(data)) as zf:
            zf.extractall(dest.parent)
        dest.write_bytes(data)
    else:
        dest.write_bytes(data)


def main() -> None:
    parser = argparse.ArgumentParser(description="Download LPC (serie historica precos)")
    parser.add_argument(
        "--years",
        default="",
        help="Anos dsan separados por virgula (ex.: 2024,2025). Vazio = so arquivos estaticos/MVP.",
    )
    args = parser.parse_args()
    years = [int(y.strip()) for y in args.years.split(",") if y.strip()] if args.years else None

    root = study_paths(SLUG)["raw"]
    ok, fail, skip = 0, 0, 0
    for sub, rel in all_files(years):
        url = f"{BASE}/{rel}"
        name = Path(rel).name
        dest = root / sub / name if sub else root / name
        if dest.exists() and dest.stat().st_size > 0:
            skip += 1
            continue
        try:
            print(f"get  {dest.relative_to(REPO_ROOT)}")
            download(url, dest)
            ok += 1
        except Exception as e:
            print(f"FAIL {rel}: {e}")
            fail += 1
    print(
        f"\n{ok} baixados, {skip} skip, {fail} falhas -> {root.relative_to(REPO_ROOT)}"
        + (f" (dsan anos: {years})" if years else " (MVP)")
    )


if __name__ == "__main__":
    main()
