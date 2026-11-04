"""Extratos do site (paineis/exportar.py) sobre insumos mínimos."""
import json
import sys

import duckdb
import pytest

from conftest import REPO_ROOT

sys.path.insert(0, str(REPO_ROOT / "paineis"))
import exportar  # noqa: E402

FIXTURE_SQL = {
    "precos": """
        SELECT * FROM (VALUES
            ('SE', 'SP', 'A', '1', 'GASOLINA', DATE '2026-05-04', 6.0, 'R$ / litro', 'VIBRA'),
            ('SE', 'SP', 'B', '2', 'GASOLINA', DATE '2026-05-05', 6.4, 'R$ / litro', 'BANDEIRA BRANCA'),
            ('S',  'PR', 'C', '3', 'GASOLINA', DATE '2026-05-12', 6.2, 'R$ / litro', 'VIBRA')
        ) t(regiao, uf, revenda, cnpj, produto, data_coleta, valor_venda, unidade, bandeira)
    """,
    "pmqc": """
        SELECT * FROM (VALUES
            (DATE '2025-01-10', 1, 'Gasolina', 'SP', 'SE', 'Aspecto', TRUE),
            (DATE '2025-01-10', 1, 'Gasolina', 'SP', 'SE', 'Cor', TRUE),
            (DATE '2025-01-11', 2, 'Óleo Diesel', 'SP', 'SE', 'Aspecto', FALSE),
            (DATE '2025-01-11', 2, 'Óleo Diesel', 'SP', 'SE', 'Cor', TRUE)
        ) t(data_coleta, id_numeric, grupo_produto, uf, regiao, ensaio, conforme)
    """,
    "vendas": """
        SELECT * FROM (VALUES
            (2025, 1, DATE '2025-01-01', 'SUDESTE', 'SP', 'GLP', 10.0),
            (2025, 1, DATE '2025-01-01', 'SUDESTE', 'SP', 'GLP', 5.0)
        ) t(ano, mes, data_referencia, grande_regiao, uf, produto, vendas_m3)
    """,
    "revendas": """
        SELECT * FROM (VALUES
            ('1', 'SP', 'VIBRA', DATE '2020-01-01'),
            ('1', 'SP', 'VIBRA', DATE '2020-01-01'),
            ('2', 'RJ', 'BANDEIRA BRANCA', DATE '2021-01-01')
        ) t(cnpj, uf, bandeira, data_publicacao)
    """,
}


@pytest.fixture
def repo(tmp_path):
    con = duckdb.connect()
    for key, sql in FIXTURE_SQL.items():
        out = tmp_path / exportar.INPUTS[key]
        out.parent.mkdir(parents=True, exist_ok=True)
        con.execute(f"COPY ({sql}) TO '{out.as_posix()}' (FORMAT PARQUET)")
    quality = tmp_path / "data" / "quality"
    quality.mkdir(parents=True)
    (quality / "pmqc.json").write_text(json.dumps({
        "slug": "pmqc", "generated_at": "2026-10-19T00:00:00+00:00",
        "results": [{"table": "data/trusted/pmqc/pmqc.parquet", "rule": "min_rows", "detail": "x",
                     "status": "ok", "failing": 0, "note": None}],
    }))
    return tmp_path


def test_exportar_gera_todas_as_tabelas(repo):
    target = exportar.exportar(repo)
    con = duckdb.connect(str(target), read_only=True)
    tables = {r[0] for r in con.sql("SELECT table_name FROM duckdb_tables()").fetchall()}
    assert tables == set(exportar.EXTRATOS) | {"fontes", "sobre", "qualidade"}

    pmqc = con.sql("SELECT grupo_produto, amostras, amostras_nao_conformes FROM pmqc_mensal ORDER BY 1").fetchall()
    assert pmqc == [("Gasolina", 1, 0), ("Óleo Diesel", 1, 1)]
    assert con.sql("SELECT sum(postos) FROM revendas_uf_bandeira").fetchone()[0] == 2
    assert con.sql("SELECT vendas_m3 FROM vendas_mensal").fetchone()[0] == 15.0
    semanas = con.sql("SELECT semana, uf, preco_medio FROM precos_semanais ORDER BY 1, 2").fetchall()
    assert [(str(s), uf, p) for s, uf, p in semanas] == [("2026-05-04", "SP", 6.2), ("2026-05-11", "PR", 6.2)]
    assert con.sql("SELECT count(*) FROM qualidade").fetchone()[0] == 1
    assert con.sql("SELECT linhas FROM fontes WHERE insumo = 'pmqc'").fetchone()[0] == 4


def test_exportar_falha_sem_insumo(repo):
    (repo / exportar.INPUTS["vendas"]).unlink()
    with pytest.raises(SystemExit, match="vendas_mensal"):
        exportar.exportar(repo)


def test_paginas_so_usam_tabelas_exportadas():
    import re

    sources = {p.stem for p in (REPO_ROOT / "paineis" / "sources" / "anp").glob("*.sql")}
    assert sources == set(exportar.EXTRATOS) | {"fontes", "sobre", "qualidade"}
    for page in (REPO_ROOT / "paineis" / "pages").glob("*.md"):
        used = set(re.findall(r"\banp\.(\w+)", page.read_text(encoding="utf-8")))
        assert used <= sources, f"{page.name}: {used - sources}"
