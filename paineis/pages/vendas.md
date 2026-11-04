---
title: Vendas das distribuidoras
---

Volume de derivados vendido pelas distribuidoras, por mês, estado e produto, desde 1990.

```sql produtos
select produto, sum(vendas_m3) as total from anp.vendas_mensal group by 1 order by total desc
```

<Dropdown data={produtos} name=produto value=produto title="Produto" multiple=true selectAllByDefault=true />

```sql ufs
select distinct uf from anp.vendas_mensal order by uf
```

<Dropdown data={ufs} name=uf value=uf title="Estado" multiple=true selectAllByDefault=true />

```sql anual
select ano, produto, sum(vendas_m3) / 1e6 as vendas_milhoes_m3
from anp.vendas_mensal
where produto in ${inputs.produto.value}
  and uf in ${inputs.uf.value}
  and ano < (select max(ano) from anp.vendas_mensal)
group by all
order by ano
```

<AreaChart data={anual} x=ano y=vendas_milhoes_m3 series=produto title="Vendas por ano (milhões de m³)" yFmt=num1 />

O ano corrente fica de fora do gráfico anual porque ainda está incompleto.

```sql mensal
select mes, produto, sum(vendas_m3) / 1e3 as vendas_mil_m3
from anp.vendas_mensal
where produto in ${inputs.produto.value}
  and uf in ${inputs.uf.value}
  and mes >= (select max(mes) from anp.vendas_mensal) - interval 36 month
group by all
order by mes
```

<LineChart data={mensal} x=mes y=vendas_mil_m3 series=produto title="Últimos 36 meses (mil m³)" yFmt=num0 />

## Por estado no último ano completo

```sql por_uf
select uf, regiao, sum(vendas_m3) / 1e3 as vendas_mil_m3
from anp.vendas_mensal
where produto in ${inputs.produto.value}
  and uf in ${inputs.uf.value}
  and ano = (select max(ano) - 1 from anp.vendas_mensal)
group by all
order by vendas_mil_m3 desc
```

<BarChart data={por_uf} x=uf y=vendas_mil_m3 series=regiao yFmt=num0 sort=false />

<Details title="Sobre os dados">

Fonte: vendas de derivados de petróleo e biocombustíveis da ANP (`vendas-derivados`, arquivo trusted `vendas_mensal.parquet`).

</Details>
