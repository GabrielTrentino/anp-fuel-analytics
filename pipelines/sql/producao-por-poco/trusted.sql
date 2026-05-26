CREATE OR REPLACE TABLE trusted AS
SELECT
    trim("estado") AS estado,
    trim("bacia") AS bacia,
    trim("campo") AS campo,
    trim("operador") AS operador,
    trim("numero_do_contrato") AS contrato,
    trim("periodo") AS periodo,
    TRY_CAST(replace(CAST("oleo_bbl_dia" AS VARCHAR), ',', '.') AS DOUBLE) AS oleo_bbl_dia,
    TRY_CAST(replace(CAST("condensado_bbl_dia" AS VARCHAR), ',', '.') AS DOUBLE) AS condensado_bbl_dia,
    TRY_CAST(replace(CAST("petroleo_bbl_dia" AS VARCHAR), ',', '.') AS DOUBLE) AS petroleo_bbl_dia,
    TRY_CAST(replace(CAST("agua_bbl_dia" AS VARCHAR), ',', '.') AS DOUBLE) AS agua_bbl_dia,
    trim("instalacao_destino") AS instalacao_destino,
    trim("tipo_instalacao") AS tipo_instalacao,
    TRY_CAST(replace(CAST("tempo_de_producao_hs_por_mes" AS VARCHAR), ',', '.') AS DOUBLE) AS horas_producao_mes
FROM read_csv(
    '{{RAW_DIR}}/_prepared/producao_poco.csv',
    delim = ';',
    header = TRUE,
    auto_detect = TRUE
)
WHERE "estado" IS NOT NULL;

COPY (SELECT * FROM trusted) TO '{{TRUSTED_PARQUET}}' (FORMAT PARQUET);
