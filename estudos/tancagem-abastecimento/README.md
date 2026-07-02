# Estudo: Tancagem do Abastecimento Nacional de Combustíveis

**Slug:** `tancagem-abastecimento`  
**Referência permanente:** [anp-data-atlas — tancagem-abastecimento.md](https://github.com/GabrielTrentino/anp-data-atlas/blob/main/docs/conjuntos/tancagem-abastecimento.md)

## Papel deste estudo

| Aqui (`anp-fuel-analytics`) | No atlas (`anp-data-atlas`) |
|-----------------------------|-----------------------------|
| Notebooks **exploratórios** (perfil, qualidade, piloto de série) | Documentação estável (schema, URLs, lacunas) |
| Pipelines raw (Python) + trusted/refined (SQL) | **Integração histórica** — consolidar jun/2022→hoje |
| Resultados úteis → atualizar o `.md` do atlas | Fonte de verdade para quem for baixar e integrar |

## Resumo do conjunto

**Tancagem** = capacidade de armazenagem (m³) autorizada pela ANP (SIMP), por instalação × unidade (`Tag`) × grupo de produto. Não é estoque físico.

| Item | Detalhe |
|------|---------|
| Página | https://www.gov.br/anp/pt-br/centrais-de-conteudo/dados-abertos/tancagem-do-abastecimento-nacional-de-combustiveis |
| Config | [`config/monorepo.yaml`](../../config/monorepo.yaml) — seção `studies.tancagem-abastecimento` |

## Notebooks

| Notebook | Objetivo exploratório |
|----------|----------------------|
| [01_perfil_exploratorio.ipynb](notebooks/01_perfil_exploratorio.ipynb) | Perfil raw, qualidade/chave e inventário temporal |
| [02_estrutura_trusted.ipynb](notebooks/02_estrutura_trusted.ipynb) | Estrutura trusted, nulos, ranking por UF e evolução em GO |

## Pipeline

Na **raiz** do monorepo:

```bash
py pipelines/run.py tancagem-abastecimento          # todas as etapas
py pipelines/run.py tancagem-abastecimento trusted  # só trusted (SQL)
```

| Etapa | Engine | Script |
|-------|--------|--------|
| `raw` | Python | `pipelines/python/download_tancagem.py` |
| `raw_prepare` | Python | `pipelines/python/prepare_tancagem_raw.py` |
| `trusted` | SQL | `pipelines/sql/tancagem-abastecimento/trusted.sql` |
| `trusted_uf` | SQL | `pipelines/sql/tancagem-abastecimento/split_trusted_ufs.sql` |
| `refined` | SQL | `pipelines/sql/tancagem-abastecimento/refined.sql` |

### Camadas de dados

| Camada | Saída | Descrição |
|--------|-------|-----------|
| raw | `data/raw/tancagem-abastecimento/` | CSVs/XLSX do portal ANP |
| trusted | `data/trusted/.../tancagem.parquet` | Snapshots empilhados + `_source_*` |
| trusted (UF) | `data/trusted/.../uf/{GO,TO,DF}.parquet` | Recorte Centro-Oeste |
| refined | `data/refined/.../tancagem_por_mes_uf_grupo_tag.parquet` | Agregado mês × UF × grupo × tag |

```python
import pandas as pd
df = pd.read_parquet("data/trusted/tancagem-abastecimento/tancagem.parquet")
refined = pd.read_parquet("data/refined/tancagem-abastecimento/tancagem_por_mes_uf_grupo_tag.parquet")
```

## Notas conhecidas

| Nota | Detalhe |
|------|---------|
| **nov/dez 2022 — cobertura parcial** | Os arquivos publicados pela ANP para nov e dez/2022 contêm ~211 instalações a menos (sobretudo refinarias, ~19 M m³). O portal **não corrigiu** esses arquivos (verificado jul/2026). Não usar esses snapshots em séries nacionais nem em cálculos YoY que cruzem esse período. Ver seção 4.1 do `02_estrutura_trusted.ipynb`. |

## TODOs / investigações abertas

- **[TODO.md](TODO.md)** — itens pendentes: flag `_qualidade_snapshot` no pipeline, atualização no atlas

## Status

| Item | Situação |
|------|----------|
| Download raw | `pipelines/python/download_tancagem.py` |
| Camada trusted | SQL (`trusted.sql`) |
| Camada refined | SQL (`refined.sql`) |
| Notebooks exploratórios | `notebooks/` |
