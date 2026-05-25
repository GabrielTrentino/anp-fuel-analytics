-- Trusted MVP: ultimas 4 semanas gasolina/etanol (posto x produto x coleta)
-- Variaveis: {{RAW_DIR}}, {{TRUSTED_PARQUET}}

CREATE OR REPLACE TABLE trusted AS
WITH raw AS (
    SELECT *
    FROM read_csv(
        '{{RAW_DIR}}/qus/ultimas-4-semanas-gasolina-etanol.csv',
        delim = ';',
        header = TRUE
    )
),
norm AS (
    SELECT
        trim("Regiao - Sigla") AS regiao,
        upper(trim("Estado - Sigla")) AS uf,
        trim("Municipio") AS municipio,
        trim("Revenda") AS revenda,
        regexp_replace(CAST("CNPJ da Revenda" AS VARCHAR), '[^0-9]', '', 'g') AS cnpj,
        trim("Produto") AS produto,
        COALESCE(
            TRY_CAST("Data da Coleta" AS DATE),
            try_strptime(trim(CAST("Data da Coleta" AS VARCHAR)), '%d/%m/%Y')::DATE
        ) AS data_coleta,
        try_cast(replace(trim(CAST("Valor de Venda" AS VARCHAR)), ',', '.') AS DOUBLE) AS valor_venda,
        try_cast(replace(trim(CAST("Valor de Compra" AS VARCHAR)), ',', '.') AS DOUBLE) AS valor_compra,
        trim("Unidade de Medida") AS unidade,
        trim("Bandeira") AS bandeira,
        'qus/ultimas-4-semanas-gasolina-etanol.csv' AS _source_file
    FROM raw
)
SELECT * FROM norm
WHERE cnpj IS NOT NULL AND length(cnpj) >= 11;

COPY (SELECT * FROM trusted) TO '{{TRUSTED_PARQUET}}' (FORMAT PARQUET);
