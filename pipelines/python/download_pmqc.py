"""Download PMQC (Programa de Monitoramento da Qualidade dos Combustiveis).

Portal: .../arquivos/pmqc/YYYY/<nome>.csv
Naming varies by year — this script builds the known URL list.
"""
from __future__ import annotations

import argparse
import sys
import urllib.request
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "pipelines"))

from core.config import study_paths  # noqa: E402

SLUG = "pmqc"
BASE = "https://www.gov.br/anp/pt-br/centrais-de-conteudo/dados-abertos/arquivos/pmqc"
USER_AGENT = "Mozilla/5.0 (anp-fuel-analytics; research)"

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


def download(url: str, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=180) as resp:
        dest.write_bytes(resp.read())


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--years", nargs="*", type=int, default=list(range(2024, 2027)))
    args = parser.parse_args()

    root = study_paths(SLUG)["raw"]
    ok, fail = 0, 0

    for name in STATIC:
        url = f"{BASE}/{name}"
        dest = root / name
        if dest.exists() and dest.stat().st_size > 0:
            ok += 1
            continue
        try:
            print(f"get  {name}")
            download(url, dest)
            ok += 1
        except Exception as e:
            print(f"FAIL {name}: {e}")
            fail += 1

    for year in args.years:
        if year not in MONTHLY:
            print(f"skip year {year} (nao mapeado)")
            continue
        for name in MONTHLY[year]:
            url = f"{BASE}/{year}/{name}"
            dest = root / str(year) / name
            if dest.exists() and dest.stat().st_size > 0:
                ok += 1
                continue
            try:
                print(f"get  {year}/{name}")
                download(url, dest)
                ok += 1
            except Exception as e:
                print(f"FAIL {year}/{name}: {e}")
                fail += 1

    print(f"\n{ok} ok, {fail} falhas -> {root.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
