"""Normaliza headers dos CSVs de vendas-derivados (BOM + encoding)."""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "pipelines"))

from core.config import study_paths  # noqa: E402

SLUG = "vendas-derivados"

MONTH_MAP = {
    "JAN": 1, "FEV": 2, "MAR": 3, "ABR": 4, "MAI": 5, "JUN": 6,
    "JUL": 7, "AGO": 8, "SET": 9, "OUT": 10, "NOV": 11, "DEZ": 12,
}

FILES = [
    ("vendas-combustiveis-m3-1990-2025.csv", "vendas_mensal.csv"),
    ("segmento/vendas-combustiveis-segmento-m3-2012-2025.csv", "vendas_segmento.csv"),
    ("tipo/vendas-oleo-diesel-tipo-m3-2013-2025.csv", "vendas_diesel_tipo.csv"),
    ("tipo/vendas-glp-tipo-vasilhame-m3-2007-2025.csv", "vendas_glp_vasilhame.csv"),
]

FILES_BIODIESEL = [
    ("biodiesel/vendas-biodiesel-b100-m3.csv", "vendas_biodiesel.csv"),
]

FILES_MUNICIPAL = [
    ("municipio/vendas-anuais-de-gasolina-c-por-municipio.csv", "vendas_municipal_gasolina.csv"),
    ("municipio/vendas-anuais-de-oleo-diesel-por-municipio.csv", "vendas_municipal_diesel.csv"),
    ("municipio/vendas-anuais-de-etanol-hidratado-por-municipio.csv", "vendas_municipal_etanol.csv"),
    ("municipio/vendas-anuais-de-glp-por-municipio.csv", "vendas_municipal_glp.csv"),
]


def normalize_cols(df: pd.DataFrame) -> pd.DataFrame:
    renames = {}
    for c in df.columns:
        low = c.strip().upper()
        if "ANO" in low:
            renames[c] = "ano"
        elif "MÊS" in low or "MES" in low or "M\xc3\x8aS" in low or low.startswith("M") and len(low) <= 4:
            renames[c] = "mes_abrev"
        elif "GRANDE" in low:
            renames[c] = "grande_regiao"
        elif "FEDERA" in low:
            renames[c] = "uf"
        elif "PRODUTO" in low:
            renames[c] = "produto"
        elif "SEGMENTO" in low:
            renames[c] = "segmento"
        elif "VENDAS" in low:
            renames[c] = "vendas_raw"
    return df.rename(columns=renames)


def parse_vendas(s: pd.Series) -> pd.Series:
    return pd.to_numeric(s.str.replace(",", "."), errors="coerce")


def normalize_cols_glp(df: pd.DataFrame) -> pd.DataFrame:
    """GLP tem VASILHAME em vez de PRODUTO."""
    renames = {}
    for c in df.columns:
        low = c.strip().upper()
        if "ANO" in low:
            renames[c] = "ano"
        elif "MÊS" in low or "MES" in low or low.startswith("M") and len(low) <= 4:
            renames[c] = "mes_abrev"
        elif "GRANDE" in low:
            renames[c] = "grande_regiao"
        elif "FEDERA" in low:
            renames[c] = "uf"
        elif "VASILHAME" in low:
            renames[c] = "vasilhame"
        elif "VENDAS" in low:
            renames[c] = "vendas_raw"
    return df.rename(columns=renames)


def normalize_cols_biodiesel(df: pd.DataFrame) -> pd.DataFrame:
    renames = {}
    for c in df.columns:
        low = c.strip().upper()
        if "MÊS" in low or "MES" in low or "M\xc3\x8aS" in low:
            renames[c] = "mes_ano_raw"
        elif "ORIGEM" in low:
            renames[c] = "regiao_origem"
        elif "DESTINO" in low:
            renames[c] = "regiao_destino"
        elif "VENDAS" in low or "BIODIESEL" in low:
            renames[c] = "vendas_raw"
    return df.rename(columns=renames)


def normalize_cols_municipal(df: pd.DataFrame) -> pd.DataFrame:
    renames = {}
    for c in df.columns:
        low = c.strip().upper()
        if "ANO" in low:
            renames[c] = "ano"
        elif "GRANDE" in low:
            renames[c] = "grande_regiao"
        elif low == "UF":
            renames[c] = "uf"
        elif "PRODUTO" in low:
            renames[c] = "produto"
        elif "IBGE" in low or "CÓDIGO" in low or "CODIGO" in low:
            renames[c] = "cod_ibge"
        elif "MUNIC" in low:
            renames[c] = "municipio"
        elif "VENDAS" in low:
            renames[c] = "vendas_raw"
    return df.rename(columns=renames)


def main() -> None:
    raw_dir = study_paths(SLUG)["raw"]
    out_dir = raw_dir / "_prepared"
    out_dir.mkdir(parents=True, exist_ok=True)

    # Standard files (sep=;, month abbreviation)
    for src_rel, dst_name in FILES:
        src = raw_dir / src_rel
        if not src.exists():
            print(f"skip (ausente) {src_rel}")
            continue
        df = pd.read_csv(src, sep=";", dtype=str, encoding="utf-8-sig")
        if "VASILHAME" in ";".join(df.columns).upper():
            df = normalize_cols_glp(df)
        else:
            df = normalize_cols(df)
        if "mes_abrev" in df.columns:
            df["mes"] = df["mes_abrev"].str.strip().str.upper().map(MONTH_MAP)
        if "vendas_raw" in df.columns:
            df["vendas_m3"] = parse_vendas(df["vendas_raw"])
        dest = out_dir / dst_name
        df.to_csv(dest, index=False)
        print(f"-> {dest.relative_to(REPO_ROOT)} ({len(df):,} linhas)")

    # Biodiesel (sep=,, date format MM/YYYY)
    for src_rel, dst_name in FILES_BIODIESEL:
        src = raw_dir / src_rel
        if not src.exists():
            print(f"skip (ausente) {src_rel}")
            continue
        df = pd.read_csv(src, sep=",", dtype=str, encoding="utf-8-sig")
        df = normalize_cols_biodiesel(df)
        if "mes_ano_raw" in df.columns:
            parts = df["mes_ano_raw"].str.split("/", expand=True)
            df["mes"] = pd.to_numeric(parts[0], errors="coerce").astype("Int64")
            df["ano"] = pd.to_numeric(parts[1], errors="coerce").astype("Int64")
        if "vendas_raw" in df.columns:
            df["vendas_m3"] = pd.to_numeric(
                df["vendas_raw"].str.replace(".", "", regex=False).str.replace(",", ".", regex=False),
                errors="coerce",
            )
        dest = out_dir / dst_name
        df.to_csv(dest, index=False)
        print(f"-> {dest.relative_to(REPO_ROOT)} ({len(df):,} linhas)")

    # Municipal (sep=;, annual, no month)
    for src_rel, dst_name in FILES_MUNICIPAL:
        src = raw_dir / src_rel
        if not src.exists():
            print(f"skip (ausente) {src_rel}")
            continue
        df = pd.read_csv(src, sep=";", dtype=str, encoding="utf-8-sig")
        # GLP municipal has P13/OUTROS instead of VENDAS
        if "P13" in df.columns:
            df = normalize_cols_municipal(df)
            p13 = pd.to_numeric(df.get("P13", pd.Series(dtype=float)), errors="coerce").fillna(0)
            outros = pd.to_numeric(df.get("OUTROS", pd.Series(dtype=float)), errors="coerce").fillna(0)
            df["vendas_m3"] = p13 + outros
            df = df.drop(columns=["P13", "OUTROS"], errors="ignore")
        else:
            df = normalize_cols_municipal(df)
            if "vendas_raw" in df.columns:
                df["vendas_m3"] = parse_vendas(df["vendas_raw"])
        df = df.drop(columns=["vendas_raw"], errors="ignore")
        dest = out_dir / dst_name
        df.to_csv(dest, index=False)
        print(f"-> {dest.relative_to(REPO_ROOT)} ({len(df):,} linhas)")


if __name__ == "__main__":
    main()
