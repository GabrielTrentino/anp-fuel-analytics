-- Refined: join PMQC x preços LPC — postos não-conformes praticam preço diferente?
-- Variáveis: {{TRUSTED_PARQUET}}, {{REFINED_DIR}}
-- Depende: data/trusted/serie-historica-precos/lpc_posto.parquet

CREATE OR REPLACE TABLE pmqc_resumo AS
SELECT
    cnpj,
    date_trunc('month', data_coleta) AS mes,
    grupo_produto,
    count(*) AS total_ensaios,
    sum(CASE WHEN NOT conforme THEN 1 ELSE 0 END) AS nao_conformes,
    CASE WHEN sum(CASE WHEN NOT conforme THEN 1 ELSE 0 END) > 0 THEN TRUE ELSE FALSE END AS teve_nc
FROM read_parquet('{{TRUSTED_PARQUET}}')
WHERE cnpj IS NOT NULL
  AND data_coleta IS NOT NULL
  AND conforme IS NOT NULL
GROUP BY 1, 2, 3;

CREATE OR REPLACE TABLE precos AS
SELECT
    cnpj,
    date_trunc('month', data_coleta) AS mes,
    produto,
    avg(valor_venda) AS preco_medio_venda,
    count(*) AS coletas_preco
FROM read_parquet('data/trusted/serie-historica-precos/lpc_posto.parquet')
WHERE cnpj IS NOT NULL
  AND data_coleta IS NOT NULL
  AND valor_venda IS NOT NULL
GROUP BY 1, 2, 3;

CREATE OR REPLACE TABLE pmqc_precos AS
SELECT
    p.cnpj,
    p.mes,
    p.grupo_produto,
    p.total_ensaios,
    p.nao_conformes,
    p.teve_nc,
    pr.produto AS produto_preco,
    pr.preco_medio_venda,
    pr.coletas_preco
FROM pmqc_resumo p
INNER JOIN precos pr
    ON p.cnpj = pr.cnpj
    AND p.mes = pr.mes
ORDER BY p.mes, p.cnpj;

COPY (SELECT * FROM pmqc_precos) TO '{{REFINED_DIR}}/pmqc_precos_join.parquet' (FORMAT PARQUET);

-- Resumo agregado: preço médio por grupo (conformes vs não-conformes)
CREATE OR REPLACE TABLE resumo_preco_conformidade AS
SELECT
    p.grupo_produto,
    p.teve_nc,
    count(DISTINCT p.cnpj) AS postos,
    avg(pr.preco_medio_venda) AS preco_medio,
    median(pr.preco_medio_venda) AS preco_mediano,
    count(*) AS observacoes
FROM pmqc_resumo p
INNER JOIN precos pr
    ON p.cnpj = pr.cnpj
    AND p.mes = pr.mes
GROUP BY 1, 2
ORDER BY 1, 2;

COPY (SELECT * FROM resumo_preco_conformidade) TO '{{REFINED_DIR}}/resumo_preco_conformidade.parquet' (FORMAT PARQUET);
