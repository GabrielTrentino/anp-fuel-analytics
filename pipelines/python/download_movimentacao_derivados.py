"""Download amostra de movimentacao-derivados (ZIPs por produto)."""
from __future__ import annotations

import sys
import urllib.request
import zipfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "pipelines"))

from core.config import study_paths  # noqa: E402

SLUG = "movimentacao-derivados"
BASE = "https://www.gov.br/anp/pt-br/centrais-de-conteudo/dados-abertos/arquivos/mdpg"
USER_AGENT = "Mozilla/5.0 (anp-fuel-analytics; research)"

FILES: list[tuple[str, str]] = [
    ("metadado-unificado-logistica.pdf", "metadado-unificado-logistica.pdf"),
    ("liquidos.zip", "liquidos.zip"),
    ("glp.zip", "glp.zip"),
    ("lubrificante.zip", "lubrificante.zip"),
    ("trr.zip", "trr.zip"),
    ("aviacao.zip", "aviacao.zip"),
    ("asfalto.zip", "asfalto.zip"),
    ("solvente.zip", "solvente.zip"),
    ("fornecedores-vendas-diretas.zip", "fornecedores-vendas-diretas.zip"),
    ("movimentacaologistica.zip", "movimentacaologistica.zip"),
]


def download(url: str, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=180) as resp:
        dest.write_bytes(resp.read())


def extract_zip(zip_path: Path, dest_dir: Path) -> None:
    dest_dir.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(zip_path, "r") as zf:
        zf.extractall(dest_dir)


def main() -> None:
    root = study_paths(SLUG)["raw"]
    ok, fail = 0, 0
    for name, rel in FILES:
        url = f"{BASE}/{rel}"
        dest = root / name
        if dest.exists() and dest.stat().st_size > 0:
            print(f"skip {dest.relative_to(REPO_ROOT)}")
            ok += 1
        else:
            try:
                print(f"get  {dest.relative_to(REPO_ROOT)}")
                download(url, dest)
                ok += 1
            except Exception as e:
                print(f"FAIL {name}: {e}")
                fail += 1
                continue
        if name.endswith(".zip"):
            extract_dir = root / name.replace(".zip", "")
            marker = extract_dir / ".extracted"
            if not marker.exists():
                print(f"unzip {name} -> {extract_dir.relative_to(REPO_ROOT)}")
                extract_zip(dest, extract_dir)
                marker.write_text("ok\n", encoding="utf-8")
    print(f"\n{ok} arquivos ok, {fail} falhas -> {root.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
