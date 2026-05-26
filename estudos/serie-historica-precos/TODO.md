# TODO — serie-historica-precos

**Legenda:** `—` pendente · `◐` em andamento · `✓` concluído

## Pipeline

| Item | Status |
|------|--------|
| Download raw MVP (qus + metadados) | ✓ |
| Download dsan 2024–2025 (71 CSVs) | ✓ |
| `config/monorepo.yaml` | ✓ |
| Trusted `qus_gasolina_etanol.parquet` | ✓ |
| Trusted `dsan_gasolina_etanol_2024_2025.parquet` | ✓ |
| Trusted `lpc_posto.parquet` (qus + dsan gasolina) | ✓ |
| Trusted dsan diesel/GNV (`dsan_diesel_gnv_2024_2025.parquet` — 536.534 linhas, 10.532 CNPJs) | ✓ |
| Cruzamento cadastro (CNPJ) | ✓ |
| Notebook `01_perfil_exploratorio.ipynb` (10 seções: evolução, spread, UF, diesel gap, bandeira, volatilidade, GNV, paridade etanol, dispersão municipal, resumo) | ✓ |

## Famílias no portal (`shpc/`)

Glossário **qus / dsan / dsas**: [atlas — estrutura shpc](https://github.com/GabrielTrentino/anp-data-atlas/blob/main/docs/conjuntos/serie-historica-precos.md#estrutura-do-portal-shpc).

## Download

```bash
py pipelines/python/download_serie_historica_precos.py              # MVP
py pipelines/python/download_serie_historica_precos.py --years 2024,2025
```

## Próximas análises

| Prioridade | Tema |
|:----------:|------|
| 1 | Série média venda por produto/UF (dsan 2024–2025) |
| 2 | Spread compra/venda × bandeira |
| 3 | Postos no cadastro sem preço LPC no período |
| 4 | Trusted diesel + GLP (mesmo schema) |
| 5 | × vendas-derivados agregado UF |
