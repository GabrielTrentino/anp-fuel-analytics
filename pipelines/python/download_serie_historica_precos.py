"""Download serie historica de precos (LPC) — MVP + dsan mensal.

    py pipelines/python/download_serie_historica_precos.py [--years 2024,2025] [--force] [--check]
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "pipelines"))

from core.download import Remote, main_for  # noqa: E402

SLUG = "serie-historica-precos"
BASE = "https://www.gov.br/anp/pt-br/centrais-de-conteudo/dados-abertos/arquivos/shpc"

DSAN_FAMILIES = (
    "precos-gasolina-etanol",
    "precos-diesel-gnv",
    "precos-glp",
)

# (subdir local, path relativo no portal)
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
                out.append((f"dsan/{year}", f"dsan/{year}/{fam}-{m:02d}.csv"))
    return out


def remotes(years: list[int] | None) -> list[Remote]:
    files = list(STATIC) + (dsan_files(years) if years else [])
    out: list[Remote] = []
    for sub, rel in files:
        name = Path(rel).name
        dest = f"{sub}/{name}" if sub else name
        # ZIPs sao extraidos na propria pasta e mantidos (comportamento original)
        out.append(Remote(f"{BASE}/{rel}", dest, extract_to=sub if rel.endswith(".zip") else None))
    return out


def main() -> None:
    parser = argparse.ArgumentParser(description="Download LPC (serie historica precos)")
    parser.add_argument(
        "--years",
        default="",
        help="Anos dsan separados por virgula (ex.: 2024,2025). Vazio = so arquivos estaticos/MVP.",
    )
    args, rest = parser.parse_known_args()
    years = [int(y.strip()) for y in args.years.split(",") if y.strip()] or None
    main_for(SLUG, remotes(years), argv=rest)


if __name__ == "__main__":
    main()
