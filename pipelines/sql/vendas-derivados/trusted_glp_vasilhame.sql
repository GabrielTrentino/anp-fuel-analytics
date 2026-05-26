-- Trusted: vendas de GLP por tipo de vasilhame (até P13, acima P13) — 2007+
-- Requer: prepare_vendas_derivados_raw.py (gera _prepared/vendas_glp_vasilhame.csv)

CREATE OR REPLACE TABLE trusted AS
WITH raw AS (
    SELECT *
    FROM read_csv(
        '{{RAW_DIR}}/_prepared/vendas_glp_vasilhame.csv',
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
    trim(vasilhame) AS vasilhame,
    vendas_m3,
    'vendas-glp-tipo-vasilhame-m3-2007-2025.csv' AS _source_file
FROM raw
WHERE ano IS NOT NULL AND mes IS NOT NULL;

COPY (SELECT * FROM trusted) TO '{{TRUSTED_DIR}}/vendas_glp_vasilhame.parquet' (FORMAT PARQUET);
