---
title: Preços nos postos
---

Levantamento de preços da ANP (LPC), coletado semanalmente em postos de todo o país. Valores de venda ao consumidor.

```sql produtos
select produto, any_value(unidade) as unidade, count(distinct semana) as semanas
from anp.precos_semanais
group by produto
order by semanas desc, produto
```

<Dropdown data={produtos} name=produto value=produto title="Produto" defaultValue="GASOLINA" />

```sql ufs
select distinct uf from anp.precos_semanais order by uf
```

<Dropdown data={ufs} name=uf value=uf title="Estado" multiple=true selectAllByDefault=true />

```sql nacional
select semana,
       sum(preco_medio * coletas) / sum(coletas) as preco_medio,
       sum(coletas) as coletas,
       sum(postos) as postos
from anp.precos_semanais
where produto = '${inputs.produto.value}'
  and uf in ${inputs.uf.value}
group by semana
order by semana
```

```sql ultima_semana
select *,
       preco_medio - lag(preco_medio) over (order by semana) as variacao
from ${nacional}
qualify semana = max(semana) over ()
```

<BigValue data={ultima_semana} value=preco_medio title="Preço médio na última semana" fmt='"R$" #,##0.00' comparison=variacao comparisonFmt='"R$" #,##0.00' comparisonTitle="vs. semana anterior" downIsGood=true />
<BigValue data={ultima_semana} value=postos title="Postos pesquisados" fmt=num0 />

<LineChart data={nacional} x=semana y=preco_medio yFmt='"R$" #,##0.00' title="Preço médio semanal ({inputs.produto.value})" yAxisTitle="R$" />

```sql por_uf
select uf, regiao,
       sum(preco_medio * coletas) / sum(coletas) as preco_medio,
       min(preco_min) as preco_min,
       max(preco_max) as preco_max,
       sum(coletas) as coletas
from anp.precos_semanais
where produto = '${inputs.produto.value}'
  and semana > (select max(semana) from anp.precos_semanais where produto = '${inputs.produto.value}') - interval 28 day
  and uf in ${inputs.uf.value}
group by uf, regiao
order by preco_medio desc
```

## Por estado nas últimas 4 semanas

<BarChart data={por_uf} x=uf y=preco_medio series=regiao yFmt='"R$" #,##0.00' sort=false />

<DataTable data={por_uf} rows=27>
  <Column id=uf title="UF" />
  <Column id=regiao title="Região" />
  <Column id=preco_medio title="Preço médio" fmt='"R$" #,##0.00' contentType=colorscale />
  <Column id=preco_min title="Mínimo" fmt='"R$" #,##0.00' />
  <Column id=preco_max title="Máximo" fmt='"R$" #,##0.00' />
  <Column id=coletas fmt=num0 />
</DataTable>

## Por bandeira nas últimas 4 semanas

```sql bandeiras
select bandeira,
       sum(preco_medio * postos) / sum(postos) as preco_medio,
       sum(postos) as postos
from anp.precos_bandeira
where produto = '${inputs.produto.value}'
  and uf in ${inputs.uf.value}
group by bandeira
having sum(postos) >= 30
order by preco_medio
```

Bandeiras com pelo menos 30 postos pesquisados na seleção.

<BarChart data={bandeiras} x=bandeira y=preco_medio swapXY=true yFmt='"R$" #,##0.00' sort=false />

<Details title="Sobre os dados">

Fonte: série histórica de preços de combustíveis da ANP (`serie-historica-precos`, arquivo trusted `lpc_posto.parquet`).
O preço médio de cada semana é a média das coletas, ponderada pelo número de coletas de cada estado.
Diesel, GLP e GNV só têm as semanas mais recentes no arquivo baixado até agora.

</Details>
