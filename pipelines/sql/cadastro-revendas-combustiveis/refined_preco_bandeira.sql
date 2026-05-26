-- Refined: preço médio de venda por bandeira e UF (gasolina + diesel)
-- Join cadastro × série histórica preços (LPC + diesel/GNV dsan)

CREATE OR REPLACE TABLE cadastro AS
SELECT cnpj, bandeira, uf, municipio
FROM read_parquet('{{TRUSTED_CADASTRO}}');

CREATE OR REPLACE TABLE precos AS
SELECT cnpj, produto, data_coleta, valor_venda, valor_compra, uf
FROM read_parquet('{{TRUSTED_LPC}}')
WHERE valor_venda IS NOT NULL
UNION ALL
SELECT cnpj, produto, data_coleta, valor_venda, valor_compra, uf
FROM read_parquet('{{TRUSTED_DIESEL}}')
WHERE valor_venda IS NOT NULL;

CREATE OR REPLACE TABLE preco_bandeira AS
SELECT
    c.bandeira,
    c.uf,
    p.produto,
    date_trunc('month', p.data_coleta) AS mes,
    count(*) AS coletas,
    avg(p.valor_venda) AS preco_medio_venda,
    median(p.valor_venda) AS preco_mediano_venda,
    avg(p.valor_compra) AS preco_medio_compra
FROM precos p
INNER JOIN cadastro c ON p.cnpj = c.cnpj
GROUP BY 1, 2, 3, 4;

COPY (SELECT * FROM preco_bandeira ORDER BY mes, uf, bandeira, produto)
TO '{{REFINED_DIR}}/preco_por_bandeira_uf.parquet' (FORMAT PARQUET);
