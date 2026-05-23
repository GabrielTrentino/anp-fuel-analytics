-- Recorte trusted por UF: GO, TO, DF.
-- Variáveis: {{TRUSTED_PARQUET}}, {{TRUSTED_UF_DIR}}, {{UF_GO}}, {{UF_TO}}, {{UF_DF}}

COPY (
    SELECT * FROM read_parquet('{{TRUSTED_PARQUET}}') WHERE "Uf" = 'GO'
) TO '{{UF_GO}}' (FORMAT PARQUET);

COPY (
    SELECT * FROM read_parquet('{{TRUSTED_PARQUET}}') WHERE "Uf" = 'TO'
) TO '{{UF_TO}}' (FORMAT PARQUET);

COPY (
    SELECT * FROM read_parquet('{{TRUSTED_PARQUET}}') WHERE "Uf" = 'DF'
) TO '{{UF_DF}}' (FORMAT PARQUET);
