-- Trusted: distribuidores de combustiveis liquidos (AEA + contratos CE/CR)
-- Variaveis: {{RAW_DIR}}, {{TRUSTED_PARQUET}}
-- Requer: prepare_distribuidores_raw.py (gera _prepared/distribuidores_aea.csv)

CREATE OR REPLACE TABLE trusted_aea AS
SELECT
    CAST(#1 AS VARCHAR) AS codigo_agente,
    CAST(#2 AS VARCHAR) AS codigo_simp,
    regexp_replace(CAST(#3 AS VARCHAR), '[^0-9]', '', 'g') AS cnpj,
    trim(CAST(#4 AS VARCHAR)) AS nome_reduzido,
    trim(CAST(#5 AS VARCHAR)) AS razao_social,
    trim(CAST(#6 AS VARCHAR)) AS endereco,
    trim(CAST(#7 AS VARCHAR)) AS bairro,
    trim(CAST(#8 AS VARCHAR)) AS municipio,
    trim(CAST(#9 AS VARCHAR)) AS uf,
    CAST(#10 AS VARCHAR) AS cep,
    trim(CAST(#11 AS VARCHAR)) AS situacao,
    trim(CAST(#12 AS VARCHAR)) AS inicio_situacao,
    trim(CAST(#13 AS VARCHAR)) AS data_publicacao,
    trim(CAST(#14 AS VARCHAR)) AS tipo_ato,
    trim(CAST(#15 AS VARCHAR)) AS tipo_autorizacao,
    trim(CAST(#16 AS VARCHAR)) AS numero_autorizacao
FROM read_csv(
    '{{RAW_DIR}}/_prepared/distribuidores_aea.csv',
    header = TRUE,
    auto_detect = TRUE
)
WHERE #3 IS NOT NULL;

COPY (SELECT * FROM trusted_aea) TO '{{TRUSTED_PARQUET}}' (FORMAT PARQUET);
