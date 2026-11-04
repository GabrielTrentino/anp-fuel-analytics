import duckdb

from core.catalog import build_catalog, catalog_entries


def test_catalog_creates_views_for_existing_outputs(tmp_path):
    out = tmp_path / "data/trusted/x/tabela.parquet"
    out.parent.mkdir(parents=True)
    duckdb.sql(f"COPY (SELECT 1 AS a) TO '{out.as_posix()}' (FORMAT PARQUET)")
    cfg = {"studies": {"meu-estudo": {"pipeline": [
        {"step": "trusted", "outputs": ["data/trusted/x/tabela.parquet"]},
        {"step": "refined", "outputs": ["data/refined/x/ainda_nao.parquet"]},
    ]}}}
    assert catalog_entries(cfg) == [
        ("meu_estudo", "trusted_tabela", "data/trusted/x/tabela.parquet"),
        ("meu_estudo", "refined_ainda_nao", "data/refined/x/ainda_nao.parquet"),
    ]
    db = build_catalog(cfg, tmp_path)
    con = duckdb.connect(str(db), read_only=True)
    assert con.sql("SELECT a FROM meu_estudo.trusted_tabela").fetchall() == [(1,)]
