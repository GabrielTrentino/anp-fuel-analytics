"""Caminhos compartilhados pelos notebooks deste estudo."""
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
SLUG = "movimentacao-derivados"
RAW_DIR = REPO_ROOT / "data" / "raw" / SLUG
PRODUCTS = [
    "liquidos",
    "glp",
    "lubrificante",
    "trr",
    "aviacao",
    "asfalto",
    "solvente",
    "fornecedores-vendas-diretas",
    "movimentacaologistica",
]
SAMPLE_LIQUIDOS = RAW_DIR / "liquidos" / "Liquidos_Vendas_Atual.csv"
SAMPLE_LOGISTICA = RAW_DIR / "movimentacaologistica" / "DADOS ABERTOS - LOGISTICA 01 - ABASTECIMENTO NACIONAL DE COMBUSTÍVEIS.csv"
