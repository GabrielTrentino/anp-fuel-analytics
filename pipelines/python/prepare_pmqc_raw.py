"""Concatena e normaliza headers dos CSVs PMQC mensais para trusted."""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "pipelines"))

from core.config import study_paths  # noqa: E402

SLUG = "pmqc"

COL_MAP = {
    "DataColeta": "data_coleta",
    "IdNumeric": "id_numeric",
    "GrupoProduto": "grupo_produto",
    "Produto": "produto",
    "RazaoSocialPosto": "razao_social",
    "CnpjPosto": "cnpj",
    "Distribuidora": "distribuidora",
    "Endereço": "endereco",
    "Complemento": "complemento",
    "Bairro": "bairro",
    "Município": "municipio",
    "Latitude": "latitude",
    "Longitude": "longitude",
    "Uf": "uf",
    "RegiaoPolitica": "regiao",
    "Ensaio": "ensaio",
    "Resultado": "resultado",
    "UnidadeEnsaio": "unidade_ensaio",
    "Conforme": "conforme",
}


def normalize_col(name: str) -> str:
    if name in COL_MAP:
        return COL_MAP[name]
    for key, val in COL_MAP.items():
        if key.lower() == name.lower() or val == name.lower():
            return val
    return name.lower().replace(" ", "_")


def main() -> None:
    raw_dir = study_paths(SLUG)["raw"]
    out = raw_dir / "_prepared" / "pmqc_all.csv"
    out.parent.mkdir(parents=True, exist_ok=True)

    frames = []
    for csv_path in sorted(raw_dir.rglob("*.csv")):
        if "_prepared" in str(csv_path):
            continue
        df = pd.read_csv(csv_path, sep=";", dtype=str, encoding="utf-8-sig", low_memory=False)
        df.columns = [normalize_col(c) for c in df.columns]
        frames.append(df)

    if not frames:
        print("Nenhum CSV encontrado")
        return

    all_df = pd.concat(frames, ignore_index=True)
    all_df.to_csv(out, index=False)
    print(f"-> {out.relative_to(REPO_ROOT)} ({len(all_df):,} linhas, {len(frames)} arquivos)")


if __name__ == "__main__":
    main()
