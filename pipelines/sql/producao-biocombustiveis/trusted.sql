-- Trusted: produção de biodiesel e etanol.
--
-- Biodiesel vem em dois arquivos com granularidades diferentes:
--   2005-2023: por produtor (usina) e UF, mês abreviado (JAN, FEV, ...)
--   2024-2026: só por grande região, mês por extenso (Janeiro, Fevereiro, ...)
-- `nivel` diz qual é a granularidade da linha; `uf`/`produtor` ficam nulos em 2024+.
-- `mes` (1-12) normaliza os dois formatos; `mes_abrev` mantém o texto original.

CREATE OR REPLACE TABLE meses AS
SELECT * FROM (VALUES
    ('JAN', 1), ('FEV', 2), ('MAR', 3), ('ABR', 4), ('MAI', 5), ('JUN', 6),
    ('JUL', 7), ('AGO', 8), ('SET', 9), ('OUT', 10), ('NOV', 11), ('DEZ', 12)
) AS t(abrev, mes);

CREATE OR REPLACE TABLE trusted_biodiesel AS
WITH unioned AS (
    SELECT
        CAST("ANO" AS INTEGER) AS ano,
        trim("MÊS") AS mes_abrev,
        trim("GRANDE REGIÃO") AS grande_regiao,
        trim("UNIDADE DA FEDERAÇÃO") AS uf,
        trim("PRODUTOR") AS produtor,
        'produtor' AS nivel,
        TRY_CAST(replace(CAST("PRODUÇÃO" AS VARCHAR), ',', '.') AS DOUBLE) AS producao_m3
    FROM read_csv(
        '{{RAW_DIR}}/producao-biodiesel-m3-2005-2023.csv',
        delim = ';',
        header = TRUE,
        auto_detect = TRUE
    )
    WHERE "ANO" IS NOT NULL
    UNION ALL
    SELECT
        CAST("ANO" AS INTEGER) AS ano,
        trim("MÊS") AS mes_abrev,
        trim("GRANDE REGIÃO") AS grande_regiao,
        NULL AS uf,
        NULL AS produtor,
        'regiao' AS nivel,
        TRY_CAST(replace(CAST("PRODUÇÃO" AS VARCHAR), ',', '.') AS DOUBLE) AS producao_m3
    FROM read_csv(
        '{{RAW_DIR}}/producao-biodiesel-m3-2024-2026.csv',
        delim = ';',
        header = TRUE,
        auto_detect = TRUE
    )
    WHERE "ANO" IS NOT NULL
)
SELECT
    u.ano,
    m.mes,
    u.mes_abrev,
    u.grande_regiao,
    u.uf,
    u.produtor,
    u.nivel,
    u.producao_m3
FROM unioned u
LEFT JOIN meses m ON m.abrev = upper(left(strip_accents(u.mes_abrev), 3));

CREATE OR REPLACE TABLE trusted_etanol AS
SELECT
    CAST("ANO" AS INTEGER) AS ano,
    trim("MÊS") AS mes_abrev,
    trim("GRANDE REGIÃO") AS grande_regiao,
    trim("UNIDADE DA FEDERAÇÃO") AS uf,
    trim("PRODUTO") AS produto,
    TRY_CAST(replace(CAST("PRODUÇÃO" AS VARCHAR), ',', '.') AS DOUBLE) AS producao_m3
FROM read_csv(
    '{{RAW_DIR}}/producao-etanol-anidro-hidratado-m3-2012-2026.csv',
    delim = ';',
    header = TRUE,
    auto_detect = TRUE
)
WHERE "ANO" IS NOT NULL;

COPY (SELECT * FROM trusted_biodiesel) TO '{{TRUSTED_DIR}}/producao_biodiesel.parquet' (FORMAT PARQUET);
COPY (SELECT * FROM trusted_etanol) TO '{{TRUSTED_DIR}}/producao_etanol.parquet' (FORMAT PARQUET);
