# TODO — serie-historica-precos

**Legenda:** `—` pendente · `◐` em andamento · `✓` concluído

## Pipeline

| Item | Status |
|------|--------|
| Download raw MVP (qus + dsan + semestral) | ◐ |
| `config/monorepo.yaml` | ✓ |
| Trusted `qus_gasolina_etanol.parquet` | ✓ |
| Trusted dsan mensal / semestral CA completo | — |
| Cruzamento cadastro (CNPJ) | ✓ |
| Notebook `01_perfil_exploratorio.ipynb` | — |

## Familias de arquivo (portal)

| Pasta | Conteudo | Granularidade |
|-------|----------|---------------|
| `qus/` | Ultimas 4 semanas | Posto (CNPJ) x produto x coleta |
| `dsan/YYYY/` | Mensal por produto | Posto (CNPJ) |
| `dsas/ca/` | Semestral combustiveis automotivos | Posto (CNPJ) |
| `dsas/glp/` | Semestral GLP | Posto (CNPJ) |

## Próximas análises

| Prioridade | Tema |
|:----------:|------|
| 1 | Expandir download dsan 2024–2025 (12 meses x 3 familias) |
| 2 | Série temporal por produto/UF (gasolina C, etanol, diesel) |
| 3 | Spread compra/venda por bandeira |
| 4 | × cadastro: postos com preço mas fora do cadastro (e vice-versa) |
| 5 | × vendas-derivados agregado UF |
