-- Trusted: cadastro de revendas de GLP
-- Variaveis: {{RAW_DIR}}, {{TRUSTED_PARQUET}}

CREATE OR REPLACE TABLE trusted AS
SELECT
    CAST("CODIGOISIMP" AS VARCHAR) AS codigo_simp,
    trim("AUTORIZACAO") AS autorizacao,
    regexp_replace("CNPJ", '[^0-9]', '', 'g') AS cnpj,
    trim("RAZAOSOCIAL") AS razao_social,
    trim("ENDERECO") AS endereco,
    trim("COMPLEMENTO") AS complemento,
    trim("BAIRRO") AS bairro,
    CAST("CEP" AS VARCHAR) AS cep,
    trim("UF") AS uf,
    trim("MUNICIPIO") AS municipio,
    trim("DISTRIBUIDORA") AS distribuidora,
    trim("CLASSE") AS classe,
    COALESCE(
        TRY_CAST("DATAPUBLICACAO" AS DATE),
        try_strptime(trim(CAST("DATAPUBLICACAO" AS VARCHAR)), '%d/%m/%Y')::DATE
    ) AS data_publicacao,
    COALESCE(
        TRY_CAST("DATAVINCULACAO" AS DATE),
        try_strptime(trim(CAST("DATAVINCULACAO" AS VARCHAR)), '%d/%m/%Y')::DATE
    ) AS data_vinculacao
FROM read_csv(
    '{{RAW_DIR}}/cadastro-revendas-glp.csv',
    delim = ';',
    header = TRUE,
    auto_detect = TRUE
)
WHERE "CNPJ" IS NOT NULL;

COPY (SELECT * FROM trusted) TO '{{TRUSTED_PARQUET}}' (FORMAT PARQUET);
