CREATE OR REPLACE TABLE trusted_petroleo AS
SELECT
    CAST("ANO" AS INTEGER) AS ano,
    trim("MÊS") AS mes_abrev,
    trim("GRANDE REGIÃO") AS grande_regiao,
    trim("UNIDADE DA FEDERAÇÃO") AS uf,
    trim("PRODUTO") AS produto,
    trim("LOCALIZAÇÃO") AS localizacao,
    TRY_CAST(replace(CAST("PRODUÇÃO" AS VARCHAR), ',', '.') AS DOUBLE) AS producao_m3
FROM read_csv(
    '{{RAW_DIR}}/producao-petroleo-m3.csv',
    delim = ';',
    header = TRUE,
    auto_detect = TRUE
)
WHERE "ANO" IS NOT NULL;

CREATE OR REPLACE TABLE trusted_gas_natural AS
SELECT
    CAST("ANO" AS INTEGER) AS ano,
    trim("MÊS") AS mes_abrev,
    trim("GRANDE REGIÃO") AS grande_regiao,
    trim("UNIDADE DA FEDERAÇÃO") AS uf,
    trim("PRODUTO") AS produto,
    trim("LOCALIZAÇÃO") AS localizacao,
    TRY_CAST(replace(CAST("PRODUÇÃO" AS VARCHAR), ',', '.') AS DOUBLE) AS producao_1000m3
FROM read_csv(
    '{{RAW_DIR}}/producao-gas-natural-1000m3.csv',
    delim = ';',
    header = TRUE,
    auto_detect = TRUE
)
WHERE "ANO" IS NOT NULL;

COPY (SELECT * FROM trusted_petroleo) TO '{{TRUSTED_DIR}}/producao_petroleo.parquet' (FORMAT PARQUET);
COPY (SELECT * FROM trusted_gas_natural) TO '{{TRUSTED_DIR}}/producao_gas_natural.parquet' (FORMAT PARQUET);
