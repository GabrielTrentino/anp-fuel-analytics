-- Trusted (MVP): Liquidos_Vendas_Atual — movimentacao derivados
-- Variaveis: {{RAW_DIR}}, {{TRUSTED_PARQUET}}

CREATE OR REPLACE TABLE trusted AS
WITH raw AS (
    SELECT
        *,
        replace(filename, '\', '/') AS _filename
    FROM read_csv(
        '{{RAW_DIR}}/liquidos/Liquidos_Vendas_Atual.csv',
        delim = ';',
        header = TRUE,
        encoding = 'latin-1'
    )
),
norm AS (
    SELECT
        make_date(
            try_cast("Ano" AS INTEGER),
            try_cast("Mês" AS INTEGER),
            1
        ) AS data_referencia,
        try_cast("Ano" AS INTEGER) AS ano,
        try_cast("Mês" AS INTEGER) AS mes,
        "Agente Regulado" AS agente_regulado,
        regexp_replace(CAST("Código do Produto" AS VARCHAR), '\.0$', '', 'g') AS codigo_produto,
        "Nome do Produto" AS nome_produto,
        "Descrição do Produto" AS descricao_produto,
        "Região Origem" AS regiao_origem,
        upper(trim("UF Origem")) AS uf_origem,
        "Região Destinatário" AS regiao_destinatario,
        upper(trim("UF Destino")) AS uf_destino,
        "Mercado Destinatário" AS mercado_destinatario,
        try_cast(
            replace(CAST("Quantidade de Produto (mil m³)" AS VARCHAR), ',', '.')
            AS DOUBLE
        ) AS volume_mil_m3,
        'liquidos' AS produto_familia,
        'vendas_atual' AS tipo_tabela,
        'liquidos/Liquidos_Vendas_Atual.csv' AS _source_file
    FROM raw
)
SELECT * FROM norm;

COPY (SELECT * FROM trusted) TO '{{TRUSTED_PARQUET}}' (FORMAT PARQUET);
