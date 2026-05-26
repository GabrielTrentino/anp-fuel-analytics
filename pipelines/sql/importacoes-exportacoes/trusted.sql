CREATE OR REPLACE TABLE trusted_derivados AS
SELECT
    CAST("ANO" AS INTEGER) AS ano,
    trim("MÊS") AS mes_abrev,
    trim("PRODUTO") AS produto,
    trim("OPERAÇÃO COMERCIAL") AS operacao,
    TRY_CAST(replace(CAST("IMPORTADO / EXPORTADO" AS VARCHAR), ',', '.') AS DOUBLE) AS volume_m3,
    TRY_CAST(replace(CAST("DISPÊNDIO / RECEITA" AS VARCHAR), ',', '.') AS DOUBLE) AS valor_usd_mil
FROM read_csv(
    '{{RAW_DIR}}/importacoes-exportacoes-derivados.csv',
    delim = ';',
    header = TRUE,
    auto_detect = TRUE
)
WHERE "ANO" IS NOT NULL;

CREATE OR REPLACE TABLE trusted_etanol AS
SELECT
    CAST("ANO" AS INTEGER) AS ano,
    trim("MÊS") AS mes_abrev,
    trim("PRODUTO") AS produto,
    trim("OPERAÇÃO COMERCIAL") AS operacao,
    TRY_CAST(replace(CAST("IMPORTADO / EXPORTADO" AS VARCHAR), ',', '.') AS DOUBLE) AS volume_m3,
    TRY_CAST(replace(CAST("DISPÊNDIO / RECEITA" AS VARCHAR), ',', '.') AS DOUBLE) AS valor_usd_mil
FROM read_csv(
    '{{RAW_DIR}}/importacoes-exportacoes-etanol.csv',
    delim = ';',
    header = TRUE,
    auto_detect = TRUE
)
WHERE "ANO" IS NOT NULL;

CREATE OR REPLACE TABLE trusted_petroleo AS
SELECT
    CAST("ANO" AS INTEGER) AS ano,
    trim("MÊS") AS mes_abrev,
    trim("PRODUTO") AS produto,
    trim("OPERAÇÃO COMERCIAL") AS operacao,
    TRY_CAST(replace(CAST("IMPORTADO / EXPORTADO" AS VARCHAR), ',', '.') AS DOUBLE) AS volume_m3,
    TRY_CAST(replace(CAST("DISPÊNDIO / RECEITA" AS VARCHAR), ',', '.') AS DOUBLE) AS valor_usd_mil
FROM read_csv(
    '{{RAW_DIR}}/importacoes-exportacoes-petroleo.csv',
    delim = ';',
    header = TRUE,
    auto_detect = TRUE
)
WHERE "ANO" IS NOT NULL;

COPY (SELECT * FROM trusted_derivados) TO '{{TRUSTED_DIR}}/ie_derivados.parquet' (FORMAT PARQUET);
COPY (SELECT * FROM trusted_etanol) TO '{{TRUSTED_DIR}}/ie_etanol.parquet' (FORMAT PARQUET);
COPY (SELECT * FROM trusted_petroleo) TO '{{TRUSTED_DIR}}/ie_petroleo.parquet' (FORMAT PARQUET);
