"""Download PMQC (Programa de Monitoramento da Qualidade dos Combustiveis).

Portal: .../arquivos/pmqc/YYYY/<nome>.csv
O nome do arquivo muda de ano para ano; a lista conhecida fica em MONTHLY.

    py pipelines/python/download_pmqc.py --years 2016 2017 ... [--force] [--check]
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "pipelines"))

from core.download import Remote, main_for  # noqa: E402

SLUG = "pmqc"
BASE = "https://www.gov.br/anp/pt-br/centrais-de-conteudo/dados-abertos/arquivos/pmqc"

STATIC = [
    "pmqc-metadados.pdf",
    "pmqc-tutorial.pdf",
    "orientacoes-analises-pmqc.pdf",
]

MONTHLY: dict[int, list[str]] = {
    2016: [f"pmqc_2016_{m:02d}.csv" for m in range(1, 13)],
    2017: [f"pmqc_2017_{m:02d}.csv" for m in range(1, 13) if m != 8]
           + ["pmqc_2017_08-1.csv"],
    2018: [f"pmqc_2018_{m:02d}.csv" for m in range(1, 13)],
    2019: [f"2019-{m:02d}-pmqc.csv" for m in range(1, 13)],
    2020: [f"2020-{m:02d}-pmqc.csv" for m in range(1, 13)],
    2021: [f"2021-{m:02d}-pmqc.csv" for m in range(1, 4)]
           + ["2021-04-pmqc-csv.csv", "2021-05-pmqc-csv.csv"]
           + [f"2021-{m:02d}-pmqc.csv" for m in range(6, 13)]
           + ["202106pmqc.csv"],
    2022: [f"2022-{m:02d}-pmqc.csv" for m in range(1, 7)]
           + [f"pmqc_2022_{m:02d}.csv" for m in range(7, 13)],
    2023: [f"pmqc-{m:02d}.csv" for m in range(1, 13)],
    2024: [f"pmqc-{m:02d}.csv" for m in range(1, 11)],
    2025: [f"pmqc-{m:02d}.csv" for m in range(1, 4)]
           + [f"pmqc_2025_{m:02d}.csv" for m in range(4, 7)]
           + [f"pmqc-2025-{m:02d}.csv" for m in range(7, 13)],
    2026: [f"pmqc_2026_{m:02d}.csv" for m in range(1, 5)],
}


def remotes(years: list[int]) -> list[Remote]:
    out = [Remote(f"{BASE}/{name}", name) for name in STATIC]
    for year in years:
        if year not in MONTHLY:
            print(f"skip year {year} (nao mapeado)")
            continue
        out += [Remote(f"{BASE}/{year}/{name}", f"{year}/{name}") for name in MONTHLY[year]]
    return out


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--years", nargs="*", type=int, default=list(range(2024, 2027)))
    args, rest = parser.parse_known_args()
    main_for(SLUG, remotes(args.years), argv=rest)


if __name__ == "__main__":
    main()
