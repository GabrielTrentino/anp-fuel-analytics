# Estudo: Movimentação de derivados de petróleo, gás natural e biocombustíveis

**Slug:** `movimentacao-derivados`  
**Referência permanente:** [anp-data-atlas — movimentacao-derivados.md](https://github.com/GabrielTrentino/anp-data-atlas/blob/main/docs/conjuntos/movimentacao-derivados.md)

## Papel deste estudo

| Aqui (`anp-fuel-analytics`) | No atlas (`anp-data-atlas`) |
|-----------------------------|-----------------------------|
| Notebooks exploratórios (perfil, inventário, ligação com tancagem) | Documentação estável (sub-bases, schema, lacunas) |
| Download raw + prepare + trusted (MVP líquidos) | Matriz de ZIPs/CSVs e chaves de cruzamento |
| Pipeline trusted/refined | MVP líquidos ✓ · demais produtos pendentes |

## Resumo do conjunto

Volumes movimentados no **SIMP** (Res. ANP 729/2018), publicados como **9 ZIPs por família de produto** + PDF de metadados. Complementa [tancagem-abastecimento](../tancagem-abastecimento/) (capacidade autorizada).

| Item | Detalhe |
|------|---------|
| Página | https://www.gov.br/anp/pt-br/centrais-de-conteudo/dados-abertos/dados-abertos-movimentacao-de-derivados-de-petroleo |
| Config | [`config/monorepo.yaml`](../../config/monorepo.yaml) — seção `studies.movimentacao-derivados` |
| Metadados | `data/raw/movimentacao-derivados/metadado-unificado-logistica.pdf` |

## Pipeline

```bash
py pipelines/run.py movimentacao-derivados              # raw + prepare + trusted_liquidos
py pipelines/run.py movimentacao-derivados trusted_liquidos
```

| Etapa | Script | Saída |
|-------|--------|-------|
| `raw` | `pipelines/python/download_movimentacao_derivados.py` | ZIPs extraídos em `data/raw/...` |
| `raw_prepare` | `pipelines/python/prepare_movimentacao_raw.py` | histórico 2007–2017 normalizado |
| `trusted_liquidos` | `pipelines/sql/movimentacao-derivados/trusted_liquidos_vendas.sql` | `liquidos_vendas_atual.parquet` |

## Cruzamento com tancagem

Resultado: [cruzamento_tancagem_resultado.md](cruzamento_tancagem_resultado.md)

```bash
py estudos/movimentacao-derivados/scripts/cruzamento_tancagem.py
```

- Match nome+UF: **30%** dos agentes movimentação
- Match só nome: **57%** — join via razão social normalizada; CNPJ virá do cadastro revendas

## Achados importantes

- CSVs SIMP usam separador **`;`** (não vírgula)
- Sem `Cnpj`/`CodInstalacao` — agente = `Agente Regulado`
- Histórico 2007–2017 sem cabeçalho → `*_normalizado.csv`

Ver **[TODO.md](TODO.md)**.

## Status

| Item | Situação |
|------|----------|
| Download raw | ✓ |
| Prepare (histórico) | ✓ |
| Trusted líquidos vendas atual | ✓ |
| Cruzamento tancagem | ✓ |
| Demais produtos / refined | pendente |
