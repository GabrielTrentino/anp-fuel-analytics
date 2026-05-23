"""
Baixa CSVs (e metadados) de Tancagem Autorizada a Operar para data/raw/tancagem-abastecimento/.
Fonte: https://www.gov.br/anp/.../tancagem-do-abastecimento-nacional-de-combustiveis
"""

from __future__ import annotations

import urllib.request
from pathlib import Path

BASE = (
    "https://www.gov.br/anp/pt-br/centrais-de-conteudo/dados-abertos"
    "/arquivos/arquivos-tancagem-do-abastecimento-nacional-de-combustiveis"
)
USER_AGENT = "Mozilla/5.0 (anp-fuel-analytics; research)"

# (subdir, filename on disk, path under dados-abertos/)
FILES: list[tuple[str, str, str]] = [
    ("", "metadados-tancagem.pdf", "metadados-tancagem.pdf"),
    # 2026
    ("2026", "janeiro.csv", "dados-abertos/2026/janeiro.csv"),
    ("2026", "fevereiro.csv", "dados-abertos/2026/fevereiro.csv"),
    ("2026", "marco.csv", "dados-abertos/2026/marco.csv"),
    ("2026", "abril.csv", "dados-abertos/2026/abril.csv"),
    # 2025
    ("2025", "janeiro.csv", "dados-abertos/2025/janeiro.csv"),
    ("2025", "fevereiro.csv", "dados-abertos/2025/fevereiro.csv"),
    ("2025", "marco.csv", "dados-abertos/2025/marco.csv"),
    ("2025", "maio-junho.csv", "dados-abertos/2025/maio-junho.csv"),
    ("2025", "julho-agosto.csv", "dados-abertos/2025/julho-agosto.csv"),
    ("2025", "setembro-a-novembro.csv", "dados-abertos/2025/setembro-a-novembro.csv"),
    ("2025", "dezembro.csv", "dados-abertos/2025/dezembro.csv"),
    # 2024
    ("2024", "janeiro.csv", "dados-abertos/2024/janeiro.csv"),
    ("2024", "fevereiro.csv", "dados-abertos/2024/fevereiro.csv"),
    ("2024", "marco-julho.csv", "dados-abertos/2024/marco-julho.csv"),
    ("2024", "agosto.csv", "dados-abertos/2024/agosto.csv"),
    ("2024", "setembro-outubro.csv", "dados-abertos/2024/setembro-outubro.csv"),
    ("2024", "novembro.csv", "dados-abertos/2024/novembro.csv"),
    ("2024", "dezembro.csv", "dados-abertos/2024/dezembro.csv"),
    # 2023 (julho sem link no portal)
    ("2023", "janeiro.csv", "dados-abertos/2023/janeiro.csv"),
    ("2023", "fevereiro.csv", "dados-abertos/2023/fevereiro.csv"),
    ("2023", "marco.csv", "dados-abertos/2023/marco.csv"),
    ("2023", "abril.csv", "dados-abertos/2023/abril.csv"),
    ("2023", "maio.csv", "dados-abertos/2023/maio.csv"),
    ("2023", "junho.csv", "dados-abertos/2023/junho.csv"),
    ("2023", "agosto.csv", "dados-abertos/2023/agosto.csv"),
    ("2023", "setembro.csv", "dados-abertos/2023/setembro.csv"),
    ("2023", "outubro.csv", "dados-abertos/2023/outubro.csv"),
    ("2023", "novembro.csv", "dados-abertos/2023/novembro.csv"),
    ("2023", "dezembro.csv", "dados-abertos/2023/dezembro.csv"),
    # 2022
    (
        "2022",
        "tancagem_terminais_dados_abertos_junho_2022.csv",
        "dados-abertos/2022/tancagem_terminais_dados_abertos_junho_2022.csv",
    ),
    (
        "2022",
        "tancagem_terminais_dados_abertos_julho_2022.csv",
        "dados-abertos/2022/tancagem_terminais_dados_abertos_julho_2022.csv",
    ),
    (
        "2022",
        "tancagem_terminais_dados_abertos_v1.csv",
        "dados-abertos/2022/tancagem_terminais_dados_abertos_v1.csv",
    ),
    (
        "2022",
        "tancagem_terminais_dados_abertos_2022_09_01.csv",
        "dados-abertos/2022/tancagem_terminais_dados_abertos_2022_09_01.csv",
    ),
    (
        "2022",
        "tancagem_terminais_dados_abertos_outubro_2022-csv.xlsx",
        "dados-abertos/2022/tancagem_terminais_dados_abertos_outubro_2022-csv.xlsx",
    ),
    (
        "2022",
        "tancagem_terminais_dados_abertos_novembro_2022.csv",
        "dados-abertos/2022/tancagem_terminais_dados_abertos_novembro_2022.csv",
    ),
    (
        "2022",
        "tancagem_terminais_dados_abertos_dezembro_2022.csv",
        "dados-abertos/2022/tancagem_terminais_dados_abertos_dezembro_2022.csv",
    ),
]


def repo_root() -> Path:
    return Path(__file__).resolve().parents[3]


def raw_dir() -> Path:
    return repo_root() / "data" / "raw" / "tancagem-abastecimento"


def download(url: str, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=120) as resp:
        dest.write_bytes(resp.read())


def main() -> None:
    root = raw_dir()
    ok, fail = 0, 0
    for subdir, name, rel in FILES:
        url = f"{BASE}/{rel}"
        dest = root / subdir / name if subdir else root / name
        if dest.exists() and dest.stat().st_size > 0:
            print(f"skip {dest.relative_to(repo_root())}")
            ok += 1
            continue
        try:
            print(f"get  {dest.relative_to(repo_root())}")
            download(url, dest)
            ok += 1
        except Exception as e:
            print(f"FAIL {name}: {e}")
            fail += 1
    print(f"\n{ok} arquivos ok, {fail} falhas -> {root}")


if __name__ == "__main__":
    main()
