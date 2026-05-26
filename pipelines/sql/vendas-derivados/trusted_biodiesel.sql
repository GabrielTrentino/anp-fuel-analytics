-- Trusted: vendas de biodiesel B100 (origem × destino regional)
-- Requer: prepare_vendas_derivados_raw.py (gera _prepared/vendas_biodiesel.csv)

CREATE OR REPLACE TABLE trusted AS
WITH raw AS (
    SELECT *
    FROM read_csv(
        '{{RAW_DIR}}/_prepared/vendas_biodiesel.csv',
        header = TRUE,
        auto_detect = TRUE
    )
)
SELECT
    CAST(ano AS INTEGER) AS ano,
    CAST(mes AS INTEGER) AS mes,
    make_date(CAST(ano AS INTEGER), CAST(mes AS INTEGER), 1) AS data_referencia,
    trim(regiao_origem) AS regiao_origem,
    trim(regiao_destino) AS regiao_destino,
    vendas_m3,
    'vendas-biodiesel-b100-m3.csv' AS _source_file
FROM raw
WHERE ano IS NOT NULL AND mes IS NOT NULL;

COPY (SELECT * FROM trusted) TO '{{TRUSTED_DIR}}/vendas_biodiesel.parquet' (FORMAT PARQUET);
