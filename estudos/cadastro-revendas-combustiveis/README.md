# Estudo: Dados Cadastrais dos Revendedores Varejistas de Combustíveis Automotivos

**Slug:** `cadastro-revendas-combustiveis`  
**Referência permanente:** [anp-data-atlas — cadastro-revendas-combustiveis.md](https://github.com/GabrielTrentino/anp-data-atlas/blob/main/docs/conjuntos/cadastro-revendas-combustiveis.md)

## Papel deste estudo

| Aqui (`anp-fuel-analytics`) | No atlas (`anp-data-atlas`) |
|-----------------------------|-----------------------------|
| Download + trusted `revendas.parquet` | Schema, chaves, cruzamentos documentados |
| Cruzamento CNPJ/nome com tancagem e movimentação | Inventário empírico e limitações de join |

**Objetivo principal:** fornecer **CNPJ** e geografia do **varejo** (postos) para joins com preços LPC, pontos de abastecimento e análises territoriais.

## Resumo do conjunto

| Item | Detalhe |
|------|---------|
| Página | https://www.gov.br/anp/pt-br/centrais-de-conteudo/dados-abertos/dados-cadastrais-dos-revendedores-varejistas-de-combustiveis-automoveis |
| Config | [`config/monorepo.yaml`](../../config/monorepo.yaml) — `studies.cadastro-revendas-combustiveis` |
| Raw | 1 CSV + PDF metadados |
| Periodicidade | Diária (snapshot cadastral) |

## Pipeline

```bash
py pipelines/run.py cadastro-revendas-combustiveis           # raw + trusted
py pipelines/run.py cadastro-revendas-combustiveis trusted
```

| Etapa | Script | Saída |
|-------|--------|-------|
| `raw` | `pipelines/python/download_cadastro_revendas_combustiveis.py` | `data/raw/cadastro-revendas-combustiveis/*.csv` |
| `trusted` | `pipelines/sql/cadastro-revendas-combustiveis/trusted.sql` | `revendas.parquet` |

Inventário raw:

```bash
py estudos/cadastro-revendas-combustiveis/export_inventario_raw.py
```

## Achados importantes

- **46.095** postos; **CNPJ** e **CODIGOISIMP** únicos (sem duplicata na extração atual)
- Separador **`;`**; leitura pandas com **`latin-1`**; DuckDB `read_csv` sem `encoding` forçado (UTF-8 auto)
- Colunas trusted: `codigo_isimp`, `cnpj`, `razao_social`, `uf`, `municipio`, `bandeira`, `data_publicacao`, `data_vinculacao`, …
- **~49%** Bandeira Branca; top marcas: Vibra, Ipiranga, Raízen

## Cruzamentos

Resultado: [cruzamento_resultado.md](cruzamento_resultado.md)

```bash
py estudos/cadastro-revendas-combustiveis/scripts/cruzamento_tancagem_movimentacao.py
```

| Alvo | Resultado | Interpretação |
|------|-----------|-----------------|
| Tancagem (CNPJ) | **0%** interseção | Tancagem cobre instalações com capacidade SIMP (TRR, bases, terminais); postos de rua raramente entram |
| Movimentação (agente → cadastro) | **~0,5%** | Agentes em `Liquidos_Vendas` são **distribuidores**; nomes ≠ razão social de postos |
| Uso esperado | Preços LPC, geo, fiscalização | Join por **CNPJ** quando o outro conjunto tiver posto |

## Status

| Item | Situação |
|------|----------|
| Download raw | ✓ |
| Trusted `revendas.parquet` | ✓ |
| Cruzamento tancagem / movimentação | ✓ |
| Notebook exploratório | pendente |
| Refined | pendente |

Detalhe: **[TODO.md](TODO.md)**
