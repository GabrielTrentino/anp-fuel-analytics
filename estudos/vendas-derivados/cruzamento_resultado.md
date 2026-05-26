# Cruzamento vendas-derivados x movimentacao e precos

Base: `vendas_mensal.parquet` — **93,960** linhas, 1990–2026.

## Movimentacao liquidos

| Metrica | Vendas | Movimentacao |
|---------|--------|--------------|
| Periodo | 1990-01-01 – 2026-03-01 | 2017-01-01 – 2026-04-01 |
| UFs | 27 | 27 |
| Meses sobrepostos | **111** |

Join: `uf` + `data_referencia` (mês) — comparar vendas SDC vs movimentação SIMP.

## Precos LPC

| Metrica | Vendas | Precos |
|---------|--------|--------|
| Produtos vendas | ['ETANOL HIDRATADO', 'GASOLINA C', 'GASOLINA DE AVIAÇÃO', 'GLP', 'QUEROSENE DE AVIAÇÃO', 'QUEROSENE ILUMINANTE', 'ÓLEO COMBUSTÍVEL', 'ÓLEO DIESEL'] |
| Produtos precos (upper) | ['DIESEL', 'DIESEL S10', 'ETANOL', 'GASOLINA', 'GASOLINA ADITIVADA', 'GLP', 'GNV'] |

Produtos LPC (gasolina, etanol, diesel) estao cobertos nas vendas.
Join: agregado por `produto` + `uf` + mes.
