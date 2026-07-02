-- Trusted: consolida CSVs brutos em um parquet unificado.
-- Variáveis: {{RAW_DIR}}, {{TRUSTED_PARQUET}}
--
-- _qualidade_snapshot:
--   'parcial'  — arquivos cujo escopo de cobertura é incompleto (nov/dez 2022:
--                ~211 instalações ausentes, sobretudo refinarias; confirmado
--                no portal ANP em jul/2026 — sem versão corrigida publicada).
--   'completo' — demais snapshots (cobertura normal).

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
        regexp_extract(_source_file, '([^/]+)\.csv$', 1) AS _source_period,
        CASE
            WHEN _source_file IN (
                '2022/tancagem_terminais_dados_abertos_novembro_2022.csv',
                '2022/tancagem_terminais_dados_abertos_dezembro_2022.csv'
            ) THEN 'parcial'
            ELSE 'completo'
        END AS _qualidade_snapshot
    FROM norm
)
SELECT * FROM final;

COPY (SELECT * FROM trusted) TO '{{TRUSTED_PARQUET}}' (FORMAT PARQUET);
