-- O Evidence não aceita fonte vazia (gera um Parquet inválido). Sem relatórios,
-- devolve uma linha marcadora com status 'sem_relatorio', filtrada nas páginas.
select * from qualidade
union all
select null, null, null, null, 'sem_relatorio', 0, null, null
where not exists (select 1 from qualidade)
