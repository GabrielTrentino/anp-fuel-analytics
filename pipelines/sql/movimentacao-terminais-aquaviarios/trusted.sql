CREATE OR REPLACE TABLE trusted AS
SELECT
    CAST("mes_de_referencia" AS DATE) AS mes_referencia,
    CAST("codigo_anp_do_terminal" AS VARCHAR) AS codigo_terminal,
    trim("nome_do_terminal") AS nome_terminal,
    trim("municipio_do_terminal") AS municipio,
    trim("uf") AS uf,
    CAST("sentido_da_operacao" AS INTEGER) AS sentido_operacao,
    CAST("tipo_da_operacao" AS INTEGER) AS tipo_operacao,
    CAST("modo_de_transporte" AS INTEGER) AS modo_transporte,
    CAST("codigo_anp_do_produto" AS VARCHAR) AS codigo_produto,
    trim("descricao_do_produto") AS produto,
    trim("sentido_modal") AS sentido_modal,
    CAST("volume_m3" AS DOUBLE) AS volume_m3,
    trim("nome_da_instalacao") AS nome_instalacao
FROM read_csv(
    '{{RAW_DIR}}/_prepared/movimentacao_terminais.csv',
    delim = ';',
    header = TRUE,
    auto_detect = TRUE
)
WHERE "uf" IS NOT NULL;

COPY (SELECT * FROM trusted) TO '{{TRUSTED_PARQUET}}' (FORMAT PARQUET);
