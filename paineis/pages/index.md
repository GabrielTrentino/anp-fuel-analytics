---
title: Combustíveis no Brasil com dados abertos da ANP
---

Painéis construídos a partir dos dados abertos da [ANP](https://www.gov.br/anp/pt-br/centrais-de-conteudo/dados-abertos),
processados pelo [anp-fuel-analytics](https://github.com/GabrielTrentino/anp-fuel-analytics). A documentação de
cada conjunto (origem, colunas, anomalias conhecidas) fica no [anp-data-atlas](https://github.com/GabrielTrentino/anp-data-atlas).

```sql resumo
select
  (select sum(postos) from anp.revendas_uf_bandeira) as postos,
  (select sum(amostras) from anp.pmqc_mensal) as amostras_pmqc,
  (select sum(vendas_m3) / 1e6 from anp.vendas_mensal where ano = (select max(ano) - 1 from anp.vendas_mensal)) as vendas_ultimo_ano,
  (select max(ano) - 1 from anp.vendas_mensal) as ano_vendas
```

<BigValue data={resumo} value=postos title="Postos no cadastro" fmt=num0 />
<BigValue data={resumo} value=amostras_pmqc title="Amostras analisadas pelo PMQC" fmt=num0 />
<BigValue data={resumo} value=vendas_ultimo_ano title="Vendas em {resumo[0].ano_vendas} (milhões de m³)" fmt=num1 />

## Painéis

- [Preços nos postos](/precos): preço médio semanal por produto e estado, e comparação entre bandeiras.
- [Qualidade dos combustíveis (PMQC)](/pmqc): amostras coletadas e resultados do monitoramento de qualidade.
- [Vendas das distribuidoras](/vendas): volume vendido por produto e estado desde 1990.
- [Postos revendedores](/revendas): postos autorizados por estado e bandeira.
- [Qualidade dos dados](/qualidade-dos-dados): resultado dos testes automáticos do pipeline.

## Fontes e período

```sql fontes
select insumo, arquivo, linhas, inicio, fim from anp.fontes
```

<DataTable data={fontes}>
  <Column id=insumo />
  <Column id=arquivo />
  <Column id=linhas fmt=num0 />
  <Column id=inicio title="Início" fmt="dd/mm/yyyy" />
  <Column id=fim fmt="dd/mm/yyyy" />
</DataTable>

```sql sobre
select gerado_em from anp.sobre
```

Extratos gerados em <Value data={sobre} column=gerado_em fmt="dd/mm/yyyy" />. Os números refletem os arquivos disponíveis para
download no portal da ANP na data em que o pipeline rodou.
