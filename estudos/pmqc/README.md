# Estudo: PMQC — Programa de Monitoramento da Qualidade dos Combustíveis

**Slug:** `pmqc`  
**Status:** pipeline operacional (trusted 2024–2026).

**Referência:** [anp-data-atlas — pmqc.md](https://github.com/GabrielTrentino/anp-data-atlas/blob/main/docs/conjuntos/pmqc.md)

## Dados

| Métrica | Valor |
|---------|-------|
| Período | 2024-01 a 2026-04 (26 meses) |
| Total de ensaios | 2.231.308 |
| Postos distintos (CNPJ) | 26.466 |
| UFs amostradas | 19 |
| Ensaios distintos | 27 |
| Taxa não-conformidade | 0,01% (234 ensaios) |

## Grupos de produto

| Grupo | Ensaios | Não-conforme |
|-------|--------:|:------------:|
| Gasolina | 959.294 | 0 |
| Óleo Diesel | 742.178 | 224 (0,03%) |
| Etanol | 529.836 | 10 (0,002%) |

## Pipeline

```
raw (download mensal — nomes inconsistentes por ano)
  -> raw_prepare (concat + normaliza headers)
    -> trusted.sql -> pmqc.parquet (2.2M linhas)
```

## Cruzamentos

| Dataset parceiro | Chave | Sobreposição |
|------------------|-------|--------------|
| `serie-historica-precos` | `cnpj` | 7.757 postos (29,3%) |
| `cadastro-revendas-combustiveis` | `cnpj` | pendente (trusted cadastro não gerado) |

## Relevância

Qualidade regulatória; identifica postos com não-conformidade para análise cruzada com preços e fiscalização.
