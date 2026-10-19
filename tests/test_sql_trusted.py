"""Executa SQLs trusted contra fixtures pequenas (formato real da ANP)."""
import duckdb

from conftest import FIXTURES, REPO_ROOT
from core.run_sql import run_sql_file


def test_pmqc_reads_year_folders_and_merges_coordinates(tmp_path):
    out = tmp_path / "pmqc.parquet"
    run_sql_file(
        REPO_ROOT / "pipelines/sql/pmqc/trusted.sql",
        {"RAW_DIR": (FIXTURES / "pmqc").as_posix(), "TRUSTED_PARQUET": out.as_posix()},
    )
    rows = duckdb.sql(
        f"SELECT id_numeric, ensaio, n_coordenadas, round(latitude, 2), cnpj, conforme, _source_file "
        f"FROM '{out.as_posix()}' ORDER BY id_numeric, ensaio"
    ).fetchall()
    # _prepared/ é ignorado; o resíduo duplicado por coordenada vira uma linha
    assert rows == [
        (873651, "Destilação - Resíduo", 2, -19.81, "02323005000180", True, "2024/pmqc-01.csv"),
        (873651, "Teor de Etanol", 1, -19.8, "02323005000180", True, "2024/pmqc-01.csv"),
        (873700, "Aspecto", 1, -16.68, "11297774000142", False, "2024/pmqc-01.csv"),
    ]


def test_biodiesel_keeps_producer_and_normalizes_month(tmp_path):
    run_sql_file(
        REPO_ROOT / "pipelines/sql/producao-biocombustiveis/trusted.sql",
        {"RAW_DIR": (FIXTURES / "producao-biocombustiveis").as_posix(), "TRUSTED_DIR": tmp_path.as_posix()},
    )
    rows = duckdb.sql(
        f"SELECT ano, mes, uf, produtor, nivel, producao_m3 FROM '{(tmp_path / 'producao_biodiesel.parquet').as_posix()}' "
        "ORDER BY ano, mes, uf"
    ).fetchall()
    assert rows == [
        (2023, 1, "MINAS GERAIS", "USINA A", "produtor", 10.5),
        (2023, 1, "SÃO PAULO", "USINA B", "produtor", 20.0),
        (2023, 2, "MINAS GERAIS", "USINA A", "produtor", 11.0),
        (2024, 1, None, None, "regiao", 40554.13),
        (2024, 3, None, None, "regiao", 39582.866),
    ]
    assert (tmp_path / "producao_etanol.parquet").exists()
