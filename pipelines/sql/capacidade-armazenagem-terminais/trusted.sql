CREATE OR REPLACE TABLE trusted AS
SELECT
    trim("Tipo") AS tipo,
    trim("Municipio") AS municipio,
    trim("UF") AS uf,
    trim("Operador") AS operador,
    CAST("Numero_de_tanques" AS INTEGER) AS numero_tanques,
    CAST("Capacidade_nominal_petroleo" AS INTEGER) AS capacidade_petroleo_m3,
    CAST("Capacidade_nominal_derivados_biocombustiveis" AS INTEGER) AS capacidade_derivados_m3,
    CAST("Capacidade_nominal_GLP" AS INTEGER) AS capacidade_glp_m3
FROM read_csv(
    '{{RAW_DIR}}/capacidade-armazenagem-terminais.csv',
    delim = ',',
    header = TRUE,
    auto_detect = TRUE
)
WHERE "UF" IS NOT NULL;

COPY (SELECT * FROM trusted) TO '{{TRUSTED_PARQUET}}' (FORMAT PARQUET);
