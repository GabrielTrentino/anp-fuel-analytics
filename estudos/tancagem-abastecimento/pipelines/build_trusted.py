"""
Consolida todos os CSV (e out/2022 XLSX) da tancagem em uma camada trusted única.

Saída: data/trusted/tancagem-abastecimento/
  - tancagem.parquet
  - manifest.json
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

SLUG = "tancagem-abastecimento"
EXPECTED_COLS = [
    "Data",
    "NomeEmpresarial",
    "Uf",
    "Municipio",
    "Cnpj",
    "CodInstalacao",
    "Segmento",
    "DetalheInstalacao",
    "Tag",
    "TipoDaUnidade",
    "GrupoDeProdutos",
    "TancagemM3",
]
META_COLS = ["_source_file", "_source_year", "_source_period"]


def repo_root() -> Path:
    return Path(__file__).resolve().parents[3]


def raw_dir() -> Path:
    return repo_root() / "data" / "raw" / SLUG


def trusted_dir() -> Path:
    return repo_root() / "data" / "trusted" / SLUG


def list_source_files() -> list[Path]:
    root = raw_dir()
    files: list[Path] = []
    for ext in ("*.csv", "*.xlsx"):
        files.extend(root.rglob(ext))
    return sorted(files, key=lambda p: str(p.relative_to(root)))


def read_csv(path: Path) -> pd.DataFrame:
    try:
        df = pd.read_csv(path, encoding="utf-8")
    except UnicodeDecodeError:
        df = pd.read_csv(path, encoding="latin-1")
    missing = set(EXPECTED_COLS) - set(df.columns)
    if missing:
        raise ValueError(f"{path.name}: colunas ausentes {missing}")
    return df[EXPECTED_COLS].copy()


def read_xlsx_outubro_2022(path: Path) -> pd.DataFrame:
    raw = pd.read_excel(path, header=4)
    rename = {c: c for c in raw.columns if c in EXPECTED_COLS}
    df = raw[list(rename.keys())].copy()
    df = df.rename(columns=rename)
    df = df.dropna(subset=["Data"])
    df["Data"] = pd.to_datetime(df["Data"], errors="coerce")
    df = df.dropna(subset=["Data"])
    return df[EXPECTED_COLS]


def infer_period(path: Path, root: Path) -> tuple[str | None, str]:
    rel = path.relative_to(root)
    year = rel.parts[0] if len(rel.parts) > 1 and rel.parts[0].isdigit() else None
    period = path.stem
    return year, period


def enrich(df: pd.DataFrame, path: Path, root: Path) -> pd.DataFrame:
    year, period = infer_period(path, root)
    rel = path.relative_to(root).as_posix()
    out = df.copy()
    out["_source_file"] = rel
    out["_source_year"] = year
    out["_source_period"] = period
    out["Data"] = pd.to_datetime(out["Data"], errors="coerce")
    out["Cnpj"] = out["Cnpj"].astype(str).str.replace(r"\.0$", "", regex=True)
    out["CodInstalacao"] = out["CodInstalacao"].astype(str).str.replace(r"\.0$", "", regex=True)
    out["TancagemM3"] = pd.to_numeric(out["TancagemM3"], errors="coerce")
    return out


def build() -> tuple[pd.DataFrame, list[dict]]:
    root = raw_dir()
    frames: list[pd.DataFrame] = []
    manifest: list[dict] = []

    for path in list_source_files():
        try:
            if path.suffix.lower() == ".csv":
                df = read_csv(path)
            elif path.suffix.lower() == ".xlsx":
                df = read_xlsx_outubro_2022(path)
            else:
                continue
            df = enrich(df, path, root)
            frames.append(df)
            manifest.append(
                {
                    "arquivo": path.relative_to(root).as_posix(),
                    "linhas": len(df),
                    "data_min": df["Data"].min().isoformat() if df["Data"].notna().any() else None,
                    "data_max": df["Data"].max().isoformat() if df["Data"].notna().any() else None,
                    "soma_m3": int(df["TancagemM3"].sum()),
                }
            )
            print(f"ok   {path.relative_to(root)} ({len(df):,} linhas)")
        except Exception as e:
            print(f"FAIL {path.relative_to(root)}: {e}")
            manifest.append(
                {"arquivo": path.relative_to(root).as_posix(), "erro": str(e)}
            )

    if not frames:
        raise RuntimeError("Nenhum arquivo carregado.")

    trusted = pd.concat(frames, ignore_index=True)
    return trusted, manifest


def save(trusted: pd.DataFrame, manifest: list[dict]) -> None:
    out_dir = trusted_dir()
    out_dir.mkdir(parents=True, exist_ok=True)

    parquet_path = out_dir / "tancagem.parquet"
    trusted.to_parquet(parquet_path, index=False)

    manifest_path = out_dir / "manifest.json"
    payload = {
        "slug": SLUG,
        "gerado_em": datetime.now(timezone.utc).isoformat(),
        "linhas_total": len(trusted),
        "arquivos": len(manifest),
        "colunas": EXPECTED_COLS + META_COLS,
        "fontes": manifest,
    }
    manifest_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"\nTrusted: {parquet_path}")
    print(f"Linhas: {len(trusted):,}")
    print(f"Periodo Data: {trusted['Data'].min()} ate {trusted['Data'].max()}")
    print(f"Arquivos fonte: {trusted['_source_file'].nunique()}")


def main() -> None:
    trusted, manifest = build()
    save(trusted, manifest)


if __name__ == "__main__":
    main()
