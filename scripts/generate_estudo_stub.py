"""Gera README de estudo planejado no anp-fuel-analytics."""
from __future__ import annotations

from pathlib import Path

import sys

FUEL_ROOT = Path(__file__).resolve().parents[1]
ATLAS_SCRIPTS = FUEL_ROOT.parent / "anp-data-atlas" / "scripts"
sys.path.insert(0, str(ATLAS_SCRIPTS))
from _conjuntos_fuel_metadata import CONJUNTOS_FUEL  # noqa: E402

FUEL_ROOT = Path(__file__).resolve().parents[1]


def render(c: dict) -> str:
    return f"""# Estudo: {c["title"]}

**Slug:** `{c["slug"]}`  
**Status:** planejado — documentação de referência no atlas; pipeline pendente.

**Referência:** [anp-data-atlas — {c["slug"]}.md](https://github.com/GabrielTrentino/anp-data-atlas/blob/main/docs/conjuntos/{c["slug"]}.md)

## Próximos passos

- [ ] Download raw (`data/raw/{c["slug"]}/`)
- [ ] Notebook `01_perfil_exploratorio.ipynb`
- [ ] Entrada em `config/monorepo.yaml`
- [ ] Pipeline raw (Python) + trusted/refined (SQL)

## Relevância

{c["relevancia"]}
"""


def main() -> None:
    for c in CONJUNTOS_FUEL:
        d = FUEL_ROOT / "estudos" / c["slug"]
        d.mkdir(parents=True, exist_ok=True)
        readme = d / "README.md"
        readme.write_text(render(c), encoding="utf-8")
        print("wrote", readme.relative_to(FUEL_ROOT))


if __name__ == "__main__":
    main()
