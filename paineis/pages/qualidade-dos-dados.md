---
title: Qualidade dos dados
---

Resultado dos testes automáticos que rodam no fim de cada pipeline (`py pipelines/run.py <estudo> check`).
"aviso" marca uma anomalia conhecida da fonte, que não interrompe o pipeline; "FALHA" interrompe.

```sql resumo
select estudo,
       count(*) as testes,
       count(*) filter (where status = 'ok') as ok,
       count(*) filter (where status = 'aviso') as avisos,
       count(*) filter (where status = 'FALHA') as falhas,
       max(gerado_em) as gerado_em
from anp.qualidade
where status <> 'sem_relatorio'
group by estudo
order by falhas desc, avisos desc, estudo
```

{#if resumo.length === 0}

Os relatórios de qualidade ainda não foram gerados nesta versão dos extratos. Rode `py pipelines/run.py all --skip-raw`
e depois `py pipelines/run.py paineis`.

{:else}

<DataTable data={resumo} rows=30>
  <Column id=estudo />
  <Column id=testes fmt=num0 />
  <Column id=ok fmt=num0 />
  <Column id=avisos fmt=num0 />
  <Column id=falhas fmt=num0 />
  <Column id=gerado_em title="Gerado em" />
</DataTable>

```sql problemas
select estudo, tabela, regra, detalhe, status, falhas, nota
from anp.qualidade
where status not in ('ok', 'sem_relatorio')
order by status, estudo, tabela
```

## Avisos e falhas

<DataTable data={problemas} search=true rows=50>
  <Column id=estudo />
  <Column id=tabela />
  <Column id=regra />
  <Column id=detalhe />
  <Column id=status />
  <Column id=falhas title="Linhas" fmt=num0 />
  <Column id=nota />
</DataTable>

{/if}

As anomalias conhecidas de cada conjunto estão descritas no
[anp-data-atlas](https://github.com/GabrielTrentino/anp-data-atlas/blob/main/docs/anomalias-conhecidas.md).
