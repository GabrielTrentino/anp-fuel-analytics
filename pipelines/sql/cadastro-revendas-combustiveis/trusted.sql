-- Trusted: cadastro revendas combustiveis automotivos (snapshot diario)
-- Variaveis: {{RAW_DIR}}, {{TRUSTED_PARQUET}}

CREATE OR REPLACE TABLE trusted AS
WITH raw AS (
    SELECT *
    FROM read_csv(
        '{{RAW_DIR}}/dados-cadastrais-revendedores-varejistas-combustiveis-automoveis.csv',
        delim = ';',
        header = TRUE
    )
),
norm AS (
    SELECT
        regexp_replace(CAST("CODIGOISIMP" AS VARCHAR), '\.0$', '', 'g') AS codigo_isimp,
        trim("AUTORIZACAO") AS autorizacao,
        COALESCE(
            TRY_CAST("DATAPUBLICACAO" AS DATE),
            try_strptime(trim(CAST("DATAPUBLICACAO" AS VARCHAR)), '%d/%m/%Y')::DATE
        ) AS data_publicacao,
        trim("RAZAOSOCIAL") AS razao_social,
        regexp_replace(CAST("CNPJ" AS VARCHAR), '\.0$', '', 'g') AS cnpj,
        trim("ENDERECO") AS endereco,
        nullif(trim("COMPLEMENTO"), 'NaN') AS complemento,
        trim("BAIRRO") AS bairro,
        regexp_replace(CAST("CEP" AS VARCHAR), '\.0$', '', 'g') AS cep,
        upper(trim("UF")) AS uf,
        trim("MUNICIPIO") AS municipio,
        trim("BANDEIRA") AS bandeira,
        COALESCE(
            TRY_CAST("DATAVINCULACAO" AS DATE),
            try_strptime(trim(CAST("DATAVINCULACAO" AS VARCHAR)), '%d/%m/%Y')::DATE
        ) AS data_vinculacao,
        'dados-cadastrais-revendedores-varejistas-combustiveis-automoveis.csv' AS _source_file
    FROM raw
)
SELECT * FROM norm;

COPY (SELECT * FROM trusted) TO '{{TRUSTED_PARQUET}}' (FORMAT PARQUET);
