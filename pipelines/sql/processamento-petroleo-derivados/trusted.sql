CREATE OR REPLACE TABLE trusted_processamento AS
SELECT
    CAST("ANO" AS INTEGER) AS ano,
    trim("MÊS") AS mes_abrev,
    trim("UNIDADE DA FEDERAÇÃO") AS uf,
    trim("REFINARIA") AS refinaria,
    trim("MATÉRIA PRIMA") AS materia_prima,
    TRY_CAST(replace(CAST("PROCESSADO" AS VARCHAR), ',', '.') AS DOUBLE) AS volume_m3
FROM read_csv(
    '{{RAW_DIR}}/processamento-petroleo-m3-1990-2025.csv',
    delim = ';',
    header = TRUE,
    auto_detect = TRUE
)
WHERE "ANO" IS NOT NULL;

CREATE OR REPLACE TABLE trusted_derivados_refinaria AS
SELECT
    CAST("ANO" AS INTEGER) AS ano,
    trim("MÊS") AS mes_abrev,
    trim("UNIDADE DA FEDERAÇÃO") AS uf,
    trim("REFINARIA") AS refinaria,
    trim("PRODUTO") AS produto,
    TRY_CAST(replace(CAST("PRODUÇÃO" AS VARCHAR), ',', '.') AS DOUBLE) AS volume_m3
FROM read_csv(
    '{{RAW_DIR}}/producao-derivados-petroleo-por-refinaria-m3-1990-2025.csv',
    delim = ';',
    header = TRUE,
    auto_detect = TRUE
)
WHERE "ANO" IS NOT NULL;

COPY (SELECT * FROM trusted_processamento) TO '{{TRUSTED_DIR}}/processamento.parquet' (FORMAT PARQUET);
COPY (SELECT * FROM trusted_derivados_refinaria) TO '{{TRUSTED_DIR}}/derivados_refinaria.parquet' (FORMAT PARQUET);
