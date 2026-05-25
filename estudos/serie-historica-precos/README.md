# Estudo: Série Histórica de Preços de Combustíveis

**Slug:** `serie-historica-precos`  
**Referência:** [anp-data-atlas — serie-historica-precos.md](https://github.com/GabrielTrentino/anp-data-atlas/blob/main/docs/conjuntos/serie-historica-precos.md)

## Papel deste estudo

Série **LPC** em nível de **posto** (`CNPJ da Revenda`), cruzamento principal com [cadastro revendas](../cadastro-revendas-combustiveis/).

## Pipeline

```bash
py pipelines/python/download_serie_historica_precos.py --years 2024,2025
py pipelines/run.py serie-historica-precos trusted_lpc_posto
```

| Etapa | Saída |
|-------|-------|
| `raw` | `qus/` + `dsan/2024|2025/` (gasolina, diesel, GLP) |
| `trusted_qus_gasolina` | janela 4 semanas |
| `trusted_dsan_gasolina` | ~1,17 M linhas (2024–2025) |
| `trusted_lpc_posto` | qus + dsan gasolina/etanol (~1,24 M linhas) |

## Achados (trusted)

| Métrica | Valor |
|---------|------:|
| Linhas `dsan_gasolina_etanol_2024_2025` | 1.166.580 |
| CNPJs distintos (2 anos) | 12.369 |
| Período | 2024-01-01 – 2025-12-31 |
| Cadastro com preço no período | **~24,9%** dos 46k postos |

Janela `qus` (4 sem): **97,7%** dos CNPJs em preços batem cadastro — amostra semanal recente.

## Cruzamento cadastro

```bash
py estudos/serie-historica-precos/scripts/cruzamento_cadastro_revendas.py
```

[ cruzamento_cadastro_resultado.md](cruzamento_cadastro_resultado.md)

## Status

| Item | Situação |
|------|----------|
| Download dsan 2024–2025 | ✓ |
| Trusted consolidado gasolina | ✓ |
| Join CNPJ cadastro | ✓ |
| Diesel/GLP trusted | pendente |

**[TODO.md](TODO.md)**
