# Estudo: Movimentação de derivados de petróleo, gás natural e biocombustíveis

**Slug:** `movimentacao-derivados`  
**Referência permanente:** [anp-data-atlas — movimentacao-derivados.md](https://github.com/GabrielTrentino/anp-data-atlas/blob/main/docs/conjuntos/movimentacao-derivados.md)

## Papel deste estudo

| Aqui (`anp-fuel-analytics`) | No atlas (`anp-data-atlas`) |
|-----------------------------|-----------------------------|
| Notebooks exploratórios (perfil, inventário, ligação com tancagem) | Documentação estável (sub-bases, schema, lacunas) |
| Download raw (Python) | Matriz de ZIPs/CSVs e chaves de cruzamento |
| Pipeline trusted/refined | **Pendente** — após validar unidades e join keys |

## Resumo do conjunto

Volumes movimentados no **SIMP** (Res. ANP 729/2018), publicados como **9 ZIPs por família de produto** + PDF de metadados. Complementa [tancagem-abastecimento](../tancagem-abastecimento/) (capacidade autorizada).

| Item | Detalhe |
|------|---------|
| Página | https://www.gov.br/anp/pt-br/centrais-de-conteudo/dados-abertos/dados-abertos-movimentacao-de-derivados-de-petroleo |
| Config | [`config/monorepo.yaml`](../../config/monorepo.yaml) — seção `studies.movimentacao-derivados` |
| Metadados | `data/raw/movimentacao-derivados/metadado-unificado-logistica.pdf` |

## Notebooks

| Notebook | Objetivo |
|----------|----------|
| [01_perfil_exploratorio.ipynb](notebooks/01_perfil_exploratorio.ipynb) | Perfil raw, sub-bases por produto, inventário |

## Download raw

```bash
py estudos/movimentacao-derivados/pipelines/download_raw.py
# ou
py pipelines/run.py movimentacao-derivados raw
```

Extrai cada ZIP em `data/raw/movimentacao-derivados/{produto}/`.

## Inventário empírico

```bash
py estudos/movimentacao-derivados/export_inventario_raw.py
```

**47 CSVs** inventariados (extração 2026-05-24) — detalhes no atlas.

## Achados iniciais (exploração)

- **Sem `Cnpj`/`CodInstalacao`** na maioria das tabelas SIMP — agente por **razão social** ou **código regulado ANP** (sub-bases lubrificante).
- **`Liquidos_Vendas_Historico_2007_a_2017.csv`** sem cabeçalho — tratar na ingestão.
- **Logística** (`movimentacaologistica/`) — 3 CSVs agregados com `Período`, `UF`, `Produto`, `Operação` (desde 2022/01).

Ver **[TODO.md](TODO.md)** — join com tancagem, unidades, pipeline trusted.

## Status

| Item | Situação |
|------|----------|
| Download raw | `pipelines/python/download_movimentacao_derivados.py` ✓ |
| Inventário empírico | `export_inventario_raw.py` ✓ |
| Notebook exploratório | `notebooks/01_perfil_exploratorio.ipynb` ✓ |
| Camada trusted/refined | pendente |
