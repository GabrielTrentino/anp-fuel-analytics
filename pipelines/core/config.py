"""Utilitários compartilhados dos pipelines na raiz do monorepo."""
from __future__ import annotations

from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
CONFIG_PATH = REPO_ROOT / "config" / "monorepo.yaml"


def load_config() -> dict:
    with CONFIG_PATH.open(encoding="utf-8") as f:
        return yaml.safe_load(f)


def study_config(slug: str) -> dict:
    cfg = load_config()
    studies = cfg.get("studies", {})
    if slug not in studies:
        raise KeyError(f"Estudo não configurado: {slug}. Disponíveis: {list(studies)}")
    return studies[slug]


def abs_path(relative: str) -> Path:
    return (REPO_ROOT / relative).resolve()


def study_paths(slug: str) -> dict[str, Path]:
    study = study_config(slug)
    return {key: abs_path(value) for key, value in study["paths"].items()}
