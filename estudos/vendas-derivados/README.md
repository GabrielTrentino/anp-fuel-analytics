# Estudo: Vendas de derivados de petróleo e biocombustíveis

**Slug:** `vendas-derivados`  
**Status:** pipeline operacional (mensal + segmento).

**Referência:** [anp-data-atlas — vendas-derivados.md](https://github.com/GabrielTrentino/anp-data-atlas/blob/main/docs/conjuntos/vendas-derivados.md)

## Dados disponíveis

| Subconjunto | Arquivo raw | Período | Trusted |
|-------------|-------------|---------|---------|
| Série principal (mensal, m³) | `vendas-combustiveis-m3-1990-2025.csv` | 1990–2026 | `vendas_mensal.parquet` |
| Por segmento (mensal, m³) | `segmento/vendas-combustiveis-segmento-m3-2012-2025.csv` | 2012–2026 | `vendas_segmento.parquet` |
| Diesel por tipo | `tipo/vendas-oleo-diesel-tipo-m3-2013-2025.csv` | 2013–2025 | pendente |
| GLP por vasilhame | `tipo/vendas-glp-tipo-vasilhame-m3-2007-2025.csv` | 2007–2025 | pendente |
| Biodiesel B100 | `biodiesel/vendas-biodiesel-b100-m3.csv` | mensal | pendente |
| Anual por município | `municipio/*.csv` (gasolina, diesel, etanol, GLP) | 1990–2024 | pendente |

## Pipeline

```
raw (download)
  -> raw_prepare (normaliza headers UTF-8-sig, converte mês abreviado)
    -> trusted_mensal.sql   -> vendas_mensal.parquet
    -> trusted_segmento.sql -> vendas_segmento.parquet
```

## Produtos (série principal)

Etanol Hidratado, Gasolina C, Gasolina de Aviação, GLP, Querosene de Aviação, Querosene Iluminante, Óleo Combustível, Óleo Diesel.

## Segmentos (vendas_segmento)

POSTO REVENDEDOR, CONSUMIDOR FINAL, TRR.

## Cruzamentos

| Dataset parceiro | Chave | Sobreposição |
|------------------|-------|--------------|
| `movimentacao-derivados` | `uf` + `data_referencia` (mês) | 111 meses sobrepostos (2017-01–2026-03) |
| `serie-historica-precos` | `produto` + `uf` + mês (precisa mapear nomes) | gasolina, etanol, diesel, GLP |

## Relevância

Demanda aparente por produto e região; complementa movimentação e produção.
