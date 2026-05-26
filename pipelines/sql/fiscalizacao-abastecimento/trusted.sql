CREATE OR REPLACE TABLE trusted AS
SELECT
    trim("uf") AS uf,
    trim("municipio") AS municipio,
    trim("bairro") AS bairro,
    trim("endereco") AS endereco,
    regexp_replace(CAST("cnpj_cpf" AS VARCHAR), '[^0-9]', '', 'g') AS cnpj_cpf,
    trim("agente_economico") AS agente_economico,
    trim("segmento_fiscalizado") AS segmento,
    TRY_CAST("data_do_df" AS DATE) AS data_fiscalizacao,
    trim(CAST("numero_do_documento" AS VARCHAR)) AS numero_documento,
    trim("procedimento_de_fiscalizacao") AS procedimento,
    trim("resultado") AS resultado
FROM read_csv(
    '{{RAW_DIR}}/_prepared/fiscalizacao.csv',
    delim = ';',
    header = TRUE,
    auto_detect = TRUE
)
WHERE "uf" IS NOT NULL;

COPY (SELECT * FROM trusted) TO '{{TRUSTED_PARQUET}}' (FORMAT PARQUET);
