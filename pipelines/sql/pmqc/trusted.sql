-- Trusted: PMQC (microdados de ensaios analíticos, todos os anos baixados em data/raw/pmqc/AAAA/)
-- Variaveis: {{RAW_DIR}}, {{TRUSTED_PARQUET}}
--
-- Lê os CSVs mensais direto das pastas AAAA/ (todos os 123 arquivos 2016-2026 têm o mesmo cabeçalho),
-- sem o CSV intermediário de ~2 GB que o prepare_pmqc_raw.py gerava.
--
-- Anomalia da fonte: o mesmo ensaio (IdNumeric + Ensaio) aparece uma vez por
-- coordenada geocodificada do posto (ex.: 5 linhas iguais com lat/long diferentes).
-- Aqui as linhas idênticas exceto pela coordenada viram uma só, com a média das
-- coordenadas e `n_coordenadas` indicando quantas existiam.

CREATE OR REPLACE TABLE raw_pmqc AS
SELECT
    TRY_CAST("DataColeta" AS DATE) AS data_coleta,
    TRY_CAST("IdNumeric" AS BIGINT) AS id_numeric,
    trim("GrupoProduto") AS grupo_produto,
    trim("Produto") AS produto,
    trim("RazaoSocialPosto") AS razao_social,
    regexp_replace("CnpjPosto", '[^0-9]', '', 'g') AS cnpj,
    trim("Distribuidora") AS distribuidora,
    trim("Município") AS municipio,
    TRY_CAST(replace("Latitude", ',', '.') AS DOUBLE) AS latitude,
    TRY_CAST(replace("Longitude", ',', '.') AS DOUBLE) AS longitude,
    trim("Uf") AS uf,
    trim("RegiaoPolitica") AS regiao,
    trim("Ensaio") AS ensaio,
    trim("Resultado") AS resultado,
    trim("UnidadeEnsaio") AS unidade_ensaio,
    CASE WHEN lower(trim("Conforme")) IN ('sim', 's', 'true', '1') THEN TRUE
         WHEN lower(trim("Conforme")) IN ('não', 'nao', 'n', 'false', '0') THEN FALSE
         ELSE NULL END AS conforme,
    regexp_extract(filename, '([^/\\]+[/\\][^/\\]+)$', 1) AS _source_file
FROM read_csv(
    '{{RAW_DIR}}/2*/*.csv',
    delim = ';',
    header = TRUE,
    all_varchar = TRUE,
    union_by_name = TRUE,
    filename = TRUE
);

CREATE OR REPLACE TABLE trusted AS
SELECT
    data_coleta, id_numeric, grupo_produto, produto, razao_social, cnpj, distribuidora,
    municipio,
    avg(latitude) AS latitude,
    avg(longitude) AS longitude,
    uf, regiao, ensaio, resultado, unidade_ensaio, conforme,
    count(*) AS n_coordenadas,
    min(_source_file) AS _source_file
FROM raw_pmqc
WHERE data_coleta IS NOT NULL
GROUP BY ALL;

COPY (SELECT * FROM trusted ORDER BY data_coleta, id_numeric, ensaio) TO '{{TRUSTED_PARQUET}}' (FORMAT PARQUET);
