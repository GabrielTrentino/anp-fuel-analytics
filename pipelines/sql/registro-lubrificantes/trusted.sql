CREATE OR REPLACE TABLE trusted AS
SELECT
    CAST("REG" AS INTEGER) AS registro,
    trim("SITUACAO") AS situacao,
    trim("PROCESSO") AS processo,
    CAST("ANO" AS INTEGER) AS ano,
    trim("MARCA_COMERCIAL") AS marca_comercial,
    trim("DETENTOR") AS detentor,
    regexp_replace(CAST("CNPJ_DETENTOR" AS VARCHAR), '[^0-9]', '', 'g') AS cnpj_detentor,
    trim("TIPO_EMPRESA") AS tipo_empresa,
    trim("TIPO_PRODUTO") AS tipo_produto,
    trim("FINALIDADE") AS finalidade,
    trim("APLICACAO") AS aplicacao,
    trim("PRODUTOR") AS produtor,
    trim("ORIGEM") AS origem,
    trim("SAE") AS sae,
    trim("ISO") AS iso,
    trim("NLGI") AS nlgi,
    trim("ND") AS nivel_desempenho,
    trim("COMPOSICAO") AS composicao,
    trim("ACONDICIONAMENTO") AS acondicionamento
FROM read_csv(
    '{{RAW_DIR}}/dados-abertos-registro-produtos.csv',
    delim = ';',
    header = TRUE,
    auto_detect = TRUE
)
WHERE "REG" IS NOT NULL;

COPY (SELECT * FROM trusted) TO '{{TRUSTED_PARQUET}}' (FORMAT PARQUET);
