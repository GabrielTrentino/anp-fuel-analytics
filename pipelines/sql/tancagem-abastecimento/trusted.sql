-- Trusted: consolida CSVs brutos em um parquet unificado.
-- Variáveis: {{RAW_DIR}}, {{TRUSTED_PARQUET}}

CREATE OR REPLACE TABLE trusted AS
WITH raw AS (
    SELECT
        *,
        replace(filename, '\', '/') AS _filename
    FROM read_csv(
        '{{RAW_DIR}}/**/*.csv',
        filename = TRUE,
        header = TRUE,
        union_by_name = TRUE,
        ignore_errors = TRUE
    )
),
norm AS (
    SELECT
        try_cast("Data" AS DATE) AS "Data",
        "NomeEmpresarial",
        "Uf",
        "Municipio",
        regexp_replace(CAST("Cnpj" AS VARCHAR), '\.0$', '', 'g') AS "Cnpj",
        regexp_replace(CAST("CodInstalacao" AS VARCHAR), '\.0$', '', 'g') AS "CodInstalacao",
        "Segmento",
        "DetalheInstalacao",
        "Tag",
        "TipoDaUnidade",
        "GrupoDeProdutos",
        try_cast("TancagemM3" AS DOUBLE) AS "TancagemM3",
        regexp_replace(_filename, '.*[/\\]tancagem-abastecimento[/\\]', '') AS _source_file,
        regexp_extract(_filename, '/(20[0-9]{2})/', 1) AS _source_year
    FROM raw
),
final AS (
    SELECT
        *,
        regexp_extract(_source_file, '([^/]+)\.csv$', 1) AS _source_period
    FROM norm
)
SELECT * FROM final;

COPY (SELECT * FROM trusted) TO '{{TRUSTED_PARQUET}}' (FORMAT PARQUET);
