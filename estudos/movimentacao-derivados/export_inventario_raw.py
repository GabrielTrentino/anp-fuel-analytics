"""Gera inventário empírico dos CSVs brutos de movimentacao-derivados."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[2]
RAW_DIR = REPO_ROOT / "data" / "raw" / "movimentacao-derivados"


def sniff_sep(path: Path) -> str:
    line = path.read_text(encoding="latin-1", errors="replace").splitlines()[0]
    if ";" in line and line.count(";") >= line.count(","):
        return ";"
    return ","


def read_csv(path: Path) -> pd.DataFrame:
    sep = sniff_sep(path)
    for enc in ("utf-8", "latin-1", "cp1252"):
        try:
            return pd.read_csv(path, encoding=enc, sep=sep, dtype=str, on_bad_lines="skip")
        except UnicodeDecodeError:
            continue
    return pd.read_csv(path, encoding="latin-1", sep=sep, dtype=str, on_bad_lines="skip")


def volume_col(df: pd.DataFrame) -> str | None:
    for c in df.columns:
        cl = c.lower()
        if "quantidade" in cl or cl.startswith("volume") or "qtd" in cl:
            return c
    return None


def period_range(df: pd.DataFrame) -> str:
    mes_col = next((c for c in df.columns if c.strip().lower() in ("mês", "mes") or (len(c.strip()) <= 4 and "m" in c.lower())), None)
    ano_col = next((c for c in df.columns if c.strip().lower() == "ano"), None)
    if ano_col and mes_col:
        ano = pd.to_numeric(df[ano_col], errors="coerce")
        mes = pd.to_numeric(df[mes_col], errors="coerce")
        ok = ano.notna() & mes.notna()
        if ok.any():
            idx = ano[ok] * 100 + mes[ok]
            return f"{int(idx.min())//100}-{int(idx.min())%100:02d} – {int(idx.max())//100}-{int(idx.max())%100:02d}"
    if "Período" in df.columns or any("per" in c.lower() for c in df.columns):
        pcol = next(c for c in df.columns if "per" in c.lower())
        vals = df[pcol].dropna().astype(str)
        if len(vals):
            return f"{vals.min()} – {vals.max()}"
    return "—"


def scan_raw() -> list[dict]:
    rows: list[dict] = []
    for path in sorted(RAW_DIR.rglob("*.csv")):
        rel = path.relative_to(RAW_DIR).as_posix()
        try:
            df = read_csv(path)
        except Exception as e:
            rows.append({"file": rel, "error": str(e)})
            continue
        vcol = volume_col(df)
        vol = pd.to_numeric(df[vcol].astype(str).str.replace(",", ".", regex=False), errors="coerce").sum() if vcol else None
        note = ""
        if "Historico_2007" in path.name and "Agente Regulado" not in df.columns:
            note = "sem cabeçalho — colunas inferidas na exploração"
        rows.append(
            {
                "file": rel,
                "linhas": len(df),
                "volume_col": vcol or "—",
                "volume_sum": round(float(vol), 3) if vol is not None and pd.notna(vol) else None,
                "periodo": period_range(df),
                "colunas": len(df.columns),
                "notas": note,
            }
        )
    return rows


def to_markdown(rows: list[dict]) -> str:
    lines = [
        "| Arquivo local | Linhas | Col. volume | Soma volume | Período | Notas |",
        "|---------------|-------:|-------------|------------:|---------|-------|",
    ]
    for r in rows:
        if "error" in r:
            lines.append(f"| `{r['file']}` | — | — | — | — | {r['error']} |")
            continue
        n = f"{r['linhas']:,}".replace(",", ".")
        vol = f"{r['volume_sum']:,.3f}".replace(",", "X").replace(".", ",").replace("X", ".") if r.get("volume_sum") is not None else "—"
        lines.append(
            f"| `{r['file']}` | {n} | {r['volume_col']} | {vol} | {r['periodo']} | {r.get('notas', '')} |"
        )
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="Inventário empírico raw movimentacao-derivados")
    parser.add_argument("--json", type=Path)
    parser.add_argument("--md", type=Path)
    args = parser.parse_args()
    rows = scan_raw()
    if args.json:
        args.json.write_text(json.dumps(rows, indent=2, ensure_ascii=False), encoding="utf-8")
    if args.md:
        args.md.write_text(to_markdown(rows), encoding="utf-8")
    if not args.json and not args.md:
        print(to_markdown(rows))
    print(f"# {len(rows)} arquivos", file=sys.stderr)


if __name__ == "__main__":
    main()
