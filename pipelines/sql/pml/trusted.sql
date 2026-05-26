-- Trusted: PML (Programa de Monitoramento dos Lubrificantes)
-- Variaveis: {{RAW_DIR}}, {{TRUSTED_PARQUET}}

CREATE OR REPLACE TABLE trusted AS
SELECT
    trim(CAST(#1 AS VARCHAR)) AS amostra,
    trim(CAST(#2 AS VARCHAR)) AS detentor,
    regexp_replace(CAST(#3 AS VARCHAR), '[^0-9]', '', 'g') AS cnpj_detentor,
    trim(CAST(#4 AS VARCHAR)) AS marca_comercial,
    trim(CAST(#5 AS VARCHAR)) AS grau_sae,
    trim(CAST(#6 AS VARCHAR)) AS registro,
    trim(CAST(#7 AS VARCHAR)) AS nivel_desempenho,
    trim(CAST(#8 AS VARCHAR)) AS lote,
    trim(CAST(#9 AS VARCHAR)) AS data_fabricacao,
    trim(CAST(#10 AS VARCHAR)) AS resultado_final,
    trim(CAST(#11 AS VARCHAR)) AS resultado_registro,
    trim(CAST(#12 AS VARCHAR)) AS resultado_qualidade,
    trim(CAST(#14 AS VARCHAR)) AS municipio,
    trim(CAST(#15 AS VARCHAR)) AS uf,
    trim(CAST(#16 AS VARCHAR)) AS boletim,
    CAST(#17 AS INTEGER) AS ano
FROM read_csv(
    '{{RAW_DIR}}/dados-abertos-pml.csv',
    delim = ';',
    header = TRUE,
    auto_detect = TRUE
)
WHERE #17 IS NOT NULL;

COPY (SELECT * FROM trusted) TO '{{TRUSTED_PARQUET}}' (FORMAT PARQUET);
