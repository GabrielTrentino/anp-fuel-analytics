-- Refined: agrega por mês (snapshot), UF, GrupoDeProdutos e Tag.
-- Variáveis: {{TRUSTED_PARQUET}}, {{REFINED_DIR}}, {{REFINED_PARQUET}}
--
-- Snapshots com _qualidade_snapshot = 'parcial' (nov/dez 2022) são excluídos
-- por padrão — cobertura incompleta confirmada no portal ANP (jul/2026).

CREATE OR REPLACE TABLE refined AS
WITH base AS (
    SELECT
        *,
        lower(_source_period) AS _period_lc,
        CASE
            WHEN regexp_matches(lower(_source_period), 'janeiro') THEN _source_year || '-01'
            WHEN regexp_matches(lower(_source_period), 'fevereiro') THEN _source_year || '-02'
            WHEN regexp_matches(lower(_source_period), 'marco') THEN _source_year || '-03'
            WHEN regexp_matches(lower(_source_period), 'abril') THEN _source_year || '-04'
            WHEN regexp_matches(lower(_source_period), 'maio') THEN _source_year || '-05'
            WHEN regexp_matches(lower(_source_period), 'junho') THEN _source_year || '-06'
            WHEN regexp_matches(lower(_source_period), 'julho') THEN _source_year || '-07'
            WHEN regexp_matches(lower(_source_period), 'agosto') THEN _source_year || '-08'
            WHEN regexp_matches(lower(_source_period), 'setembro') THEN _source_year || '-09'
            WHEN regexp_matches(lower(_source_period), 'outubro') THEN _source_year || '-10'
            WHEN regexp_matches(lower(_source_period), 'novembro') THEN _source_year || '-11'
            WHEN regexp_matches(lower(_source_period), 'dezembro') THEN _source_year || '-12'
            WHEN regexp_matches(_source_period, '2022_09_01') THEN '2022-09'
            WHEN _source_year IS NOT NULL THEN _source_year || '-' || _source_period
            ELSE _source_period
        END AS mes
    FROM read_parquet('{{TRUSTED_PARQUET}}')
    WHERE "Uf" IS NOT NULL
      AND "GrupoDeProdutos" IS NOT NULL
      AND "Tag" IS NOT NULL
      AND "TancagemM3" IS NOT NULL
      AND coalesce(_qualidade_snapshot, 'completo') = 'completo'
)
SELECT
    mes,
    "Uf",
    "GrupoDeProdutos",
    "Tag",
    sum("TancagemM3") AS tancagem_m3,
    count(*) AS linhas_origem
FROM base
GROUP BY 1, 2, 3, 4
ORDER BY 1, 2, 3, 4;

COPY (SELECT * FROM refined) TO '{{REFINED_PARQUET}}' (FORMAT PARQUET);
