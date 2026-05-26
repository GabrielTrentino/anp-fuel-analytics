-- Trusted: vendas de óleo diesel por tipo (S-10, S-500, etc.) — 2013+
-- Requer: prepare_vendas_derivados_raw.py (gera _prepared/vendas_diesel_tipo.csv)

CREATE OR REPLACE TABLE trusted AS
WITH raw AS (
    SELECT *
    FROM read_csv(
        '{{RAW_DIR}}/_prepared/vendas_diesel_tipo.csv',
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
    'vendas-oleo-diesel-tipo-m3-2013-2025.csv' AS _source_file
FROM raw
WHERE ano IS NOT NULL AND mes IS NOT NULL;

COPY (SELECT * FROM trusted) TO '{{TRUSTED_DIR}}/vendas_diesel_tipo.parquet' (FORMAT PARQUET);
