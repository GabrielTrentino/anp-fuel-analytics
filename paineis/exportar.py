"""Gera ``paineis/sources/anp/anp_paineis.duckdb``: os extratos agregados que o site lê.

O site público (Evidence, em ``paineis/``) não lê os Parquets do pipeline direto,
que têm milhões de linhas e não vão para o git. Este script agrega as saídas
trusted em tabelas pequenas (dezenas de milhares de linhas no total) e grava um
único arquivo DuckDB versionado. Rode depois de atualizar os pipelines:

    py pipelines/run.py paineis
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import duckdb

REPO_ROOT = Path(__file__).resolve().parents[1]
TARGET = Path("paineis") / "sources" / "anp" / "anp_paineis.duckdb"

INPUTS = {
    "precos": "data/trusted/serie-historica-precos/lpc_posto.parquet",
    "pmqc": "data/trusted/pmqc/pmqc.parquet",
    "vendas": "data/trusted/vendas-derivados/vendas_mensal.parquet",
    "revendas": "data/trusted/cadastro-revendas-combustiveis/revendas.parquet",
}

# Cada extrato: nome da tabela -> SQL sobre os insumos (``{precos}``, ``{pmqc}``, ...).
EXTRATOS = {
    # Preço médio semanal por produto e UF (LPC: levantamento de preços nos postos).
    "precos_semanais": """
        SELECT date_trunc('week', data_coleta)::DATE AS semana, produto, unidade, regiao, uf,
               round(avg(valor_venda), 3) AS preco_medio,
               round(median(valor_venda), 3) AS preco_mediano,
               round(min(valor_venda), 3) AS preco_min,
               round(max(valor_venda), 3) AS preco_max,
               count(*) AS coletas,
               count(DISTINCT cnpj) AS postos
        FROM {precos}
        WHERE valor_venda IS NOT NULL
        GROUP BY ALL
    """,
    # Preço médio por bandeira nas últimas 4 semanas de coleta de cada produto.
    "precos_bandeira": """
        WITH ultima AS (SELECT produto, max(data_coleta) AS fim FROM {precos} GROUP BY produto)
        SELECT p.produto, p.unidade, p.uf, p.bandeira,
               round(avg(p.valor_venda), 3) AS preco_medio,
               count(DISTINCT p.cnpj) AS postos
        FROM {precos} p JOIN ultima u USING (produto)
        WHERE p.data_coleta > u.fim - INTERVAL 28 DAY AND p.valor_venda IS NOT NULL
        GROUP BY ALL
    """,
    # PMQC por mês: amostras (id_numeric) e quantas tiveram algum ensaio não conforme.
    "pmqc_mensal": """
        WITH amostra AS (
            SELECT id_numeric, date_trunc('month', min(data_coleta))::DATE AS mes,
                   any_value(uf) AS uf, any_value(regiao) AS regiao, any_value(grupo_produto) AS grupo_produto,
                   bool_or(conforme = false) AS nao_conforme
            FROM {pmqc}
            GROUP BY id_numeric
        )
        SELECT mes, regiao, uf, grupo_produto,
               count(*) AS amostras,
               count(*) FILTER (WHERE nao_conforme) AS amostras_nao_conformes
        FROM amostra
        GROUP BY ALL
    """,
    # Ensaios que mais reprovam, por ano e grupo de produto.
    "pmqc_ensaios": """
        SELECT year(data_coleta) AS ano, grupo_produto, ensaio,
               count(DISTINCT id_numeric) AS amostras,
               count(DISTINCT id_numeric) FILTER (WHERE conforme = false) AS amostras_nao_conformes
        FROM {pmqc}
        GROUP BY ALL
    """,
    # Vendas de derivados pelas distribuidoras (m³) por mês, UF e produto.
    "vendas_mensal": """
        SELECT data_referencia AS mes, ano, grande_regiao AS regiao, uf, produto,
               sum(vendas_m3) AS vendas_m3
        FROM {vendas}
        GROUP BY ALL
    """,
    # Postos revendedores autorizados por UF e bandeira (cadastro atual).
    "revendas_uf_bandeira": """
        SELECT uf, bandeira, count(DISTINCT cnpj) AS postos
        FROM {revendas}
        GROUP BY ALL
    """,
}

# Período coberto por insumo, mostrado no rodapé das páginas.
PERIODOS = {
    "precos": "min(data_coleta), max(data_coleta)",
    "pmqc": "min(data_coleta), max(data_coleta)",
    "vendas": "min(data_referencia), max(data_referencia)",
    "revendas": "min(data_publicacao), max(data_publicacao)",
}


def exportar(repo_root: Path = REPO_ROOT, target: Path | None = None) -> Path:
    target = target or repo_root / TARGET
    paths = {k: (repo_root / v).resolve() for k, v in INPUTS.items()}
    missing = [INPUTS[k] for k, p in paths.items() if not p.exists()]
    if missing:
        raise SystemExit(f"Faltam saídas do pipeline (rode os estudos antes): {missing}")
    src = {k: f"read_parquet('{p.as_posix()}')" for k, p in paths.items()}

    target.parent.mkdir(parents=True, exist_ok=True)
    tmp = target.with_suffix(".tmp")
    tmp.unlink(missing_ok=True)
    con = duckdb.connect(str(tmp))
    try:
        for name, sql in EXTRATOS.items():
            con.execute(f"CREATE TABLE {name} AS {sql.format(**src)} ORDER BY ALL")

        now = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
        con.execute("CREATE TABLE fontes (insumo VARCHAR, arquivo VARCHAR, linhas BIGINT, inicio DATE, fim DATE)")
        for key, cols in PERIODOS.items():
            con.execute(
                f"INSERT INTO fontes SELECT ?, ?, count(*), {cols} FROM {src[key]}", [key, INPUTS[key]]
            )
        con.execute("CREATE TABLE sobre AS SELECT ?::TIMESTAMP AS gerado_em", [now[:19]])

        con.execute(
            "CREATE TABLE qualidade (estudo VARCHAR, tabela VARCHAR, regra VARCHAR, detalhe VARCHAR,"
            " status VARCHAR, falhas BIGINT, nota VARCHAR, gerado_em VARCHAR)"
        )
        for report in sorted((repo_root / "data" / "quality").glob("*.json")):
            payload = json.loads(report.read_text(encoding="utf-8"))
            con.executemany(
                "INSERT INTO qualidade VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                [
                    (payload["slug"], Path(r["table"]).name, r["rule"], r["detail"], r["status"],
                     r.get("failing", 0), r.get("note"), payload.get("generated_at"))
                    for r in payload["results"]
                ],
            )
        con.execute("CHECKPOINT")
    finally:
        con.close()
    tmp.replace(target)

    con = duckdb.connect(str(target), read_only=True)
    try:
        for (name,) in con.sql("SELECT table_name FROM duckdb_tables() ORDER BY 1").fetchall():
            print(f"  {name:22} {con.sql(f'SELECT count(*) FROM {name}').fetchone()[0]:>8,} linhas")
    finally:
        con.close()
    print(f"-> {target.as_posix()} ({target.stat().st_size / 1e6:.1f} MB)")
    return target


if __name__ == "__main__":
    exportar()
