# Estudo: Dados Cadastrais das Revendas de GLP

**Slug:** `cadastro-revendas-glp`  
**Status:** pipeline operacional (trusted completo).

**Referência:** [anp-data-atlas — cadastro-revendas-glp.md](https://github.com/GabrielTrentino/anp-data-atlas/blob/main/docs/conjuntos/cadastro-revendas-glp.md)

## Dados

| Métrica | Valor |
|---------|-------|
| Revendas | 59.349 |
| UFs | 27 |
| Municípios | 5.163 |
| Distribuidoras | 19 |
| Schema | 14 colunas (CNPJ, razão social, endereço, distribuidora, classe, datas) |

## Pipeline

```
raw (download CSV único)
  -> trusted.sql -> cadastro_revendas_glp.parquet
```

## Distribuidoras (top-5)

| Distribuidora | Revendas | % |
|---------------|---------|---|
| INDEPENDENTE | 16.207 | 27,3% |
| SUPERGASBRAS ENERGIA | 8.735 | 14,7% |
| NACIONAL GAS BUTANO | 8.315 | 14,0% |
| LIQUIGAS | 6.556 | 11,0% |
| ULTRAGAZ | 5.938 | 10,0% |

## Cruzamentos

| Dataset parceiro | Chave | Observação |
|------------------|-------|------------|
| `vendas-derivados` (GLP) | `uf` | 27 UFs, 1990–2026: densidade revendas vs volume |
| `tancagem-abastecimento` | `uf` / distribuidora | capacidade armazenamento GLP |
| `serie-historica-precos` | — | LPC não cobre GLP P13 no nível CNPJ |

## Relevância

Mercado de gás engarrafado; complementa movimentação GLP e tancagem.
