-- Trusted: vendas mensal de derivados (serie principal 1990-2025)
-- Variaveis: {{RAW_DIR}}, {{TRUSTED_PARQUET}}
-- Requer: prepare_vendas_derivados_raw.py (gera _prepared/vendas_mensal.csv)

CREATE OR REPLACE TABLE trusted AS
WITH raw AS (
    SELECT *
    FROM read_csv(
        '{{RAW_DIR}}/_prepared/vendas_mensal.csv',
        header = TRUE,
        auto_detect = TRUE
    )
)
SELECT
    CAST(ano AS INTEGER) AS ano,
    CAST(mes AS INTEGER) AS mes,
    make_date(CAST(ano AS INTEGER), CAST(mes AS INTEGER), 1) AS data_referencia,
    trim(grande_regiao) AS grande_regiao,
    trim(uf) AS uf,
    trim(produto) AS produto,
    vendas_m3,
    'vendas-combustiveis-m3-1990-2025.csv' AS _source_file
FROM raw
WHERE ano IS NOT NULL AND mes IS NOT NULL;

COPY (SELECT * FROM trusted) TO '{{TRUSTED_PARQUET}}' (FORMAT PARQUET);
