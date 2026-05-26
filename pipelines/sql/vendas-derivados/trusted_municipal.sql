-- Trusted: vendas anuais por município (gasolina, diesel, etanol, GLP) — 1990+
-- Requer: prepare_vendas_derivados_raw.py (gera _prepared/vendas_municipal_*.csv)

CREATE OR REPLACE TABLE trusted AS
WITH unioned AS (
    SELECT ano, grande_regiao, uf, produto, cod_ibge, municipio, vendas_m3
    FROM read_csv('{{RAW_DIR}}/_prepared/vendas_municipal_gasolina.csv', header=TRUE, auto_detect=TRUE)
    UNION ALL
    SELECT ano, grande_regiao, uf, produto, cod_ibge, municipio, vendas_m3
    FROM read_csv('{{RAW_DIR}}/_prepared/vendas_municipal_diesel.csv', header=TRUE, auto_detect=TRUE)
    UNION ALL
    SELECT ano, grande_regiao, uf, produto, cod_ibge, municipio, vendas_m3
    FROM read_csv('{{RAW_DIR}}/_prepared/vendas_municipal_etanol.csv', header=TRUE, auto_detect=TRUE)
    UNION ALL
    SELECT ano, grande_regiao, uf, produto, cod_ibge, municipio, vendas_m3
    FROM read_csv('{{RAW_DIR}}/_prepared/vendas_municipal_glp.csv', header=TRUE, auto_detect=TRUE)
)
SELECT
    CAST(ano AS INTEGER) AS ano,
    trim(grande_regiao) AS grande_regiao,
    trim(uf) AS uf,
    trim(produto) AS produto,
    CAST(cod_ibge AS VARCHAR) AS cod_ibge,
    trim(municipio) AS municipio,
    CAST(vendas_m3 AS DOUBLE) AS vendas_m3
FROM unioned
WHERE ano IS NOT NULL;

COPY (SELECT * FROM trusted) TO '{{TRUSTED_DIR}}/vendas_municipal.parquet' (FORMAT PARQUET);
