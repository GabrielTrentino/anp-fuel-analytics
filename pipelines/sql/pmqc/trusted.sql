-- Trusted: PMQC (microdados de ensaios analíticos, 2024-2026)
-- Variaveis: {{RAW_DIR}}, {{TRUSTED_PARQUET}}
-- Requer: prepare_pmqc_raw.py (gera _prepared/pmqc_all.csv)

CREATE OR REPLACE TABLE trusted AS
SELECT
    TRY_CAST(data_coleta AS DATE) AS data_coleta,
    CAST(id_numeric AS BIGINT) AS id_numeric,
    trim(grupo_produto) AS grupo_produto,
    trim(produto) AS produto,
    trim(razao_social) AS razao_social,
    regexp_replace(cnpj, '[^0-9]', '', 'g') AS cnpj,
    trim(distribuidora) AS distribuidora,
    trim(municipio) AS municipio,
    TRY_CAST(replace(CAST(latitude AS VARCHAR), ',', '.') AS DOUBLE) AS latitude,
    TRY_CAST(replace(CAST(longitude AS VARCHAR), ',', '.') AS DOUBLE) AS longitude,
    trim(uf) AS uf,
    trim(regiao) AS regiao,
    trim(ensaio) AS ensaio,
    trim(resultado) AS resultado,
    trim(unidade_ensaio) AS unidade_ensaio,
    CASE WHEN lower(trim(conforme)) IN ('sim', 's', 'true', '1') THEN TRUE
         WHEN lower(trim(conforme)) IN ('não', 'nao', 'n', 'false', '0') THEN FALSE
         ELSE NULL END AS conforme
FROM read_csv(
    '{{RAW_DIR}}/_prepared/pmqc_all.csv',
    header = TRUE,
    auto_detect = TRUE
)
WHERE data_coleta IS NOT NULL;

COPY (SELECT * FROM trusted) TO '{{TRUSTED_PARQUET}}' (FORMAT PARQUET);
