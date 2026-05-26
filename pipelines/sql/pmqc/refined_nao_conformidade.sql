-- Refined: taxa de não-conformidade mensal por UF e grupo de produto.
-- Variáveis: {{TRUSTED_PARQUET}}, {{REFINED_DIR}}

CREATE OR REPLACE TABLE nao_conformidade AS
WITH base AS (
    SELECT
        date_trunc('month', data_coleta) AS mes,
        uf,
        grupo_produto,
        conforme
    FROM read_parquet('{{TRUSTED_PARQUET}}')
    WHERE data_coleta IS NOT NULL
      AND uf IS NOT NULL
      AND grupo_produto IS NOT NULL
      AND conforme IS NOT NULL
)
SELECT
    CAST(mes AS DATE) AS mes,
    uf,
    grupo_produto,
    count(*) AS total_ensaios,
    sum(CASE WHEN conforme THEN 1 ELSE 0 END) AS conformes,
    sum(CASE WHEN NOT conforme THEN 1 ELSE 0 END) AS nao_conformes,
    round(sum(CASE WHEN NOT conforme THEN 1 ELSE 0 END) * 100.0 / count(*), 4) AS pct_nao_conforme
FROM base
GROUP BY 1, 2, 3
ORDER BY 1, 2, 3;

COPY (SELECT * FROM nao_conformidade) TO '{{REFINED_DIR}}/nao_conformidade_uf_produto.parquet' (FORMAT PARQUET);
