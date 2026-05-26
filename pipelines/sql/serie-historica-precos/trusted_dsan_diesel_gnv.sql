-- Trusted: dsan mensal diesel/GNV (2024-2025)
-- Mesmo schema de gasolina/etanol. Produtos: DIESEL, DIESEL S10, GNV

CREATE OR REPLACE TABLE trusted AS
WITH raw AS (
    SELECT
        *,
        replace(filename, '\', '/') AS _filename
    FROM read_csv(
        ['{{RAW_DIR}}/dsan/2024/precos-diesel-gnv-*.csv', '{{RAW_DIR}}/dsan/2025/precos-diesel-gnv-*.csv'],
        filename = TRUE,
        header = TRUE,
        union_by_name = TRUE
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
        _filename AS _source_file
    FROM raw
)
SELECT * FROM norm
WHERE cnpj IS NOT NULL AND length(cnpj) >= 11;

COPY (SELECT * FROM trusted) TO '{{TRUSTED_PARQUET}}' (FORMAT PARQUET);
