---
title: Postos revendedores
---

Postos revendedores de combustíveis automotivos com autorização da ANP, pelo cadastro mais recente baixado.

```sql por_uf
select uf, sum(postos) as postos,
       sum(postos) filter (where bandeira = 'BANDEIRA BRANCA') / sum(postos) as pct_bandeira_branca
from anp.revendas_uf_bandeira
group by uf
order by postos desc
```

<BarChart data={por_uf} x=uf y=postos yFmt=num0 sort=false title="Postos por estado" />

```sql bandeiras
select bandeira, sum(postos) as postos, sum(postos) / (select sum(postos) from anp.revendas_uf_bandeira) as participacao
from anp.revendas_uf_bandeira
group by bandeira
order by postos desc
```

## Bandeiras

<DataTable data={bandeiras} search=true>
  <Column id=bandeira />
  <Column id=postos fmt=num0 />
  <Column id=participacao title="Participação" fmt=pct1 contentType=bar />
</DataTable>

## Por estado

<DataTable data={por_uf} rows=27>
  <Column id=uf title="UF" />
  <Column id=postos fmt=num0 />
  <Column id=pct_bandeira_branca title="% bandeira branca" fmt=pct1 contentType=colorscale />
</DataTable>

<Details title="Sobre os dados">

Fonte: cadastro de revendedores varejistas de combustíveis automotivos da ANP (`cadastro-revendas-combustiveis`,
arquivo trusted `revendas.parquet`). Cada posto é contado uma vez por CNPJ.

</Details>
