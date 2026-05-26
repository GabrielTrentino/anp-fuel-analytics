CREATE OR REPLACE TABLE trusted_biodiesel AS
SELECT
    CAST("ANO" AS INTEGER) AS ano,
    trim("MÊS") AS mes_abrev,
    trim("GRANDE REGIÃO") AS grande_regiao,
    TRY_CAST(replace(CAST("PRODUÇÃO" AS VARCHAR), ',', '.') AS DOUBLE) AS producao_m3
FROM read_csv(
    '{{RAW_DIR}}/producao-biodiesel-m3-2005-2023.csv',
    delim = ';',
    header = TRUE,
    auto_detect = TRUE
)
WHERE "ANO" IS NOT NULL
UNION ALL
SELECT
    CAST("ANO" AS INTEGER) AS ano,
    trim("MÊS") AS mes_abrev,
    trim("GRANDE REGIÃO") AS grande_regiao,
    TRY_CAST(replace(CAST("PRODUÇÃO" AS VARCHAR), ',', '.') AS DOUBLE) AS producao_m3
FROM read_csv(
    '{{RAW_DIR}}/producao-biodiesel-m3-2024-2026.csv',
    delim = ';',
    header = TRUE,
    auto_detect = TRUE
)
WHERE "ANO" IS NOT NULL;

CREATE OR REPLACE TABLE trusted_etanol AS
SELECT
    CAST("ANO" AS INTEGER) AS ano,
    trim("MÊS") AS mes_abrev,
    trim("GRANDE REGIÃO") AS grande_regiao,
    trim("UNIDADE DA FEDERAÇÃO") AS uf,
    trim("PRODUTO") AS produto,
    TRY_CAST(replace(CAST("PRODUÇÃO" AS VARCHAR), ',', '.') AS DOUBLE) AS producao_m3
FROM read_csv(
    '{{RAW_DIR}}/producao-etanol-anidro-hidratado-m3-2012-2026.csv',
    delim = ';',
    header = TRUE,
    auto_detect = TRUE
)
WHERE "ANO" IS NOT NULL;

COPY (SELECT * FROM trusted_biodiesel) TO '{{TRUSTED_DIR}}/producao_biodiesel.parquet' (FORMAT PARQUET);
COPY (SELECT * FROM trusted_etanol) TO '{{TRUSTED_DIR}}/producao_etanol.parquet' (FORMAT PARQUET);
