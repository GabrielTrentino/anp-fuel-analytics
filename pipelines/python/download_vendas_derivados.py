"""Download vendas de derivados de petroleo e biocombustiveis."""
from __future__ import annotations

import sys
import urllib.request
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "pipelines"))

from core.config import study_paths  # noqa: E402

SLUG = "vendas-derivados"
BASE = "https://www.gov.br/anp/pt-br/centrais-de-conteudo/dados-abertos/arquivos/vdpb"
USER_AGENT = "Mozilla/5.0 (anp-fuel-analytics; research)"

# (subdir local, path relativo no portal)
FILES: list[tuple[str, str]] = [
    # Serie principal (mensal, 1990-2025)
    ("", "vendas-derivados-petroleo-e-etanol/metadados-vendas-derivados-petroleo-etanol.pdf"),
    ("", "vendas-derivados-petroleo-e-etanol/vendas-combustiveis-m3-1990-2025.csv"),
    # Vendas por segmento (mensal, 2012-2025)
    ("segmento", "vcs/metadados-vendas-combustiveis-por-segmento.pdf"),
    ("segmento", "vcs/vendas-combustiveis-segmento-m3-2012-2025.csv"),
    # Vendas por tipo (diesel / GLP)
    ("tipo", "vct/metadados-vendas-oleo-diesel-por-tipo.pdf"),
    ("tipo", "vct/vendas-oleo-diesel-tipo-m3-2013-2025.csv"),
    ("tipo", "vct/metadados-vendas-glp-por-tipo-vasilhame.pdf"),
    ("tipo", "vct/vendas-glp-tipo-vasilhame-m3-2007-2025.csv"),
    # Biodiesel
    ("biodiesel", "vendas-de-biodiesel/metadados-vendas-biodiesel-b100.pdf"),
    ("biodiesel", "vendas-de-biodiesel/vendas-biodiesel-b100-m3.csv"),
    # Anuais por municipio (MVP: gasolina, diesel, etanol, GLP)
    ("municipio", "vaehdpm/gasolina-c/vendas-anuais-de-gasolina-c-por-municipio.csv"),
    ("municipio", "vaehdpm/oleo-diesel/vendas-anuais-de-oleo-diesel-por-municipio.csv"),
    ("municipio", "vaehdpm/etanol-hidratado/vendas-anuais-de-etanol-hidratado-por-municipio.csv"),
    ("municipio", "vaehdpm/glp/vendas-anuais-de-glp-por-municipio.csv"),
]


def download(url: str, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=180) as resp:
        dest.write_bytes(resp.read())


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
