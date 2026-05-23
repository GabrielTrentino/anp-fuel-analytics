"""Gera inventário empírico dos CSVs brutos de tancagem (stdout ou arquivo)."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[2]
RAW_DIR = REPO_ROOT / "data" / "raw" / "tancagem-abastecimento"


def scan_raw() -> list[dict]:
    rows: list[dict] = []
    for path in sorted(RAW_DIR.rglob("*.csv")):
        rel = path.relative_to(RAW_DIR).as_posix()
        df = None
        for enc in ("utf-8", "latin-1", "cp1252"):
            try:
                df = pd.read_csv(path, dtype=str, low_memory=False, encoding=enc)
                break
            except UnicodeDecodeError:
                continue
        if df is None:
            rows.append({"file": rel, "error": "encoding"})
            continue

        m3 = pd.to_numeric(df.get("TancagemM3"), errors="coerce").sum()
        dates = pd.to_datetime(df.get("Data"), errors="coerce")
        dmin, dmax = dates.min(), dates.max()
        dr = f"{dmin.date()} – {dmax.date()}" if pd.notna(dmin) else "—"

        note = ""
        if "2022/tancagem" in rel and ("novembro" in rel or "dezembro" in rel):
            note = "anomalia ~−44% m³ vs jun–out/2022"
        elif any(
            x in rel
            for x in (
                "marco-julho",
                "maio-junho",
                "julho-agosto",
                "setembro-outubro",
                "setembro-a-novembro",
            )
        ):
            note = "bloco multi-mês"
        elif "2022_09_01" in rel:
            note = "encoding latin-1; nome set/2022"
        if rel in ("2023/novembro.csv", "2023/outubro.csv"):
            note = (note + "; " if note else "") + "idêntico a dez/2023"

        rows.append(
            {
                "file": rel,
                "linhas": len(df),
                "m3": int(round(m3)),
                "data": dr,
                "notas": note,
            }
        )
    return rows


def to_markdown(rows: list[dict]) -> str:
    lines = [
        "| Arquivo local | Linhas | Soma m³ | `Data` (min – max) | Notas |",
        "|---------------|-------:|--------:|--------------------|-------|",
    ]
    for r in rows:
        if "error" in r:
            continue
        n = f"{r['linhas']:,}".replace(",", ".")
        m3m = r["m3"] / 1e6
        lines.append(
            f"| `{r['file']}` | {n} | {m3m:.2f} M | {r['data']} | {r.get('notas', '')} |"
        )
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="Inventário empírico raw tancagem")
    parser.add_argument("--json", type=Path, help="Salvar JSON")
    parser.add_argument("--md", type=Path, help="Salvar tabela Markdown")
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
