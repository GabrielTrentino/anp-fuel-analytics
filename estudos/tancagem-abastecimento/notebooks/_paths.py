"""Caminhos compartilhados pelos notebooks deste estudo."""
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
SLUG = "tancagem-abastecimento"
RAW_DIR = REPO_ROOT / "data" / "raw" / SLUG
TRUSTED_DIR = REPO_ROOT / "data" / "trusted" / SLUG
TRUSTED_PARQUET = TRUSTED_DIR / "tancagem.parquet"
TRUSTED_UF_DIR = TRUSTED_DIR / "uf"
TRUSTED_MANIFEST = TRUSTED_DIR / "manifest.json"
REFINED_DIR = REPO_ROOT / "data" / "refined" / SLUG
REFINED_PARQUET = REFINED_DIR / "tancagem_por_mes_uf_grupo_tag.parquet"
