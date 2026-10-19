---
title: Qualidade dos combustíveis (PMQC)
---

O Programa de Monitoramento da Qualidade dos Combustíveis (PMQC) coleta amostras em postos e analisa uma lista de
ensaios por produto. Cada amostra é identificada pelo `id_numeric` da ANP.

<Alert status=warning>

**Atenção à coluna "Conforme" da fonte.** Nos arquivos abertos, só 948 de 8,4 milhões de resultados vêm marcados
como não conformes, e todos no ensaio de aspecto. Resultados numéricos fora da especificação (por exemplo, teor de
etanol de 15% na gasolina, quando o padrão é 27% a 30%) aparecem como conformes. Por isso, as taxas abaixo
mostram o que a ANP marcou, e não devem ser lidas como taxa real de não conformidade.

</Alert>

```sql grupos
select distinct grupo_produto from anp.pmqc_mensal order by 1
```

<Dropdown data={grupos} name=grupo value=grupo_produto title="Produto" multiple=true selectAllByDefault=true />

```sql anual
select year(mes) as ano, grupo_produto,
       sum(amostras) as amostras,
       sum(amostras_nao_conformes) as amostras_nao_conformes,
       sum(amostras_nao_conformes) / sum(amostras) as pct_nao_conforme
from anp.pmqc_mensal
where grupo_produto in ${inputs.grupo.value}
group by all
order by ano
```

<BarChart data={anual} x=ano y=amostras series=grupo_produto title="Amostras analisadas por ano" yFmt=num0 />

<LineChart data={anual} x=ano y=pct_nao_conforme series=grupo_produto yFmt=pct2 title="Amostras com algum ensaio marcado como não conforme" />

## Por estado

```sql por_uf
select uf, regiao,
       sum(amostras) as amostras,
       sum(amostras_nao_conformes) as amostras_nao_conformes,
       sum(amostras_nao_conformes) / sum(amostras) as pct_nao_conforme
from anp.pmqc_mensal
where grupo_produto in ${inputs.grupo.value}
group by all
order by amostras desc
```

<DataTable data={por_uf} rows=27>
  <Column id=uf title="UF" />
  <Column id=regiao title="Região" />
  <Column id=amostras fmt=num0 />
  <Column id=amostras_nao_conformes title="Não conformes" fmt=num0 />
  <Column id=pct_nao_conforme title="% não conforme" fmt=pct2 contentType=colorscale />
</DataTable>

## Ensaios

```sql ensaios
select grupo_produto, ensaio,
       sum(amostras) as amostras,
       sum(amostras_nao_conformes) as amostras_nao_conformes
from anp.pmqc_ensaios
where grupo_produto in ${inputs.grupo.value}
group by all
order by amostras desc
```

<DataTable data={ensaios} search=true>
  <Column id=grupo_produto title="Produto" />
  <Column id=ensaio />
  <Column id=amostras title="Amostras com o ensaio" fmt=num0 />
  <Column id=amostras_nao_conformes title="Marcadas não conformes" fmt=num0 />
</DataTable>

<Details title="Sobre os dados">

Fonte: PMQC da ANP (`pmqc`, arquivo trusted `pmqc.parquet`), com os arquivos mensais disponíveis para download.
A fonte repete cada ensaio uma vez por coordenada do posto; o pipeline junta essas repetições antes de contar.
Uma amostra conta como não conforme quando pelo menos um dos seus ensaios vem marcado assim.

</Details>
