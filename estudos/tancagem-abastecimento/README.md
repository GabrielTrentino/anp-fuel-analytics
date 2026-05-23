# Estudo: Tancagem do Abastecimento Nacional de Combustíveis

**Slug:** `tancagem-abastecimento`  
**Referência permanente:** [anp-data-atlas — tancagem-abastecimento.md](https://github.com/GabrielTrentino/anp-data-atlas/blob/main/docs/conjuntos/tancagem-abastecimento.md)

## Papel deste estudo

| Aqui (`anp-fuel-analytics`) | No atlas (`anp-data-atlas`) |
|-----------------------------|-----------------------------|
| Notebooks **exploratórios** (perfil, qualidade, piloto de série) | Documentação estável (schema, URLs, lacunas) |
| Protótipos de transformação | **Integração histórica** — consolidar jun/2022→hoje em pipeline reproduzível |
| Resultados úteis → atualizar o `.md` do atlas | Fonte de verdade para quem for baixar e integrar |

## Resumo do conjunto

**Tancagem** = capacidade de armazenagem (m³) autorizada pela ANP (SIMP), por instalação × unidade (`Tag`) × grupo de produto. Não é estoque físico.

| Item | Detalhe |
|------|---------|
| Página | https://www.gov.br/anp/pt-br/centrais-de-conteudo/dados-abertos/tancagem-do-abastecimento-nacional-de-combustiveis |
| Dados locais | `data/raw/tancagem-abastecimento/` |

## Notebooks

| Notebook | Objetivo exploratório | Pode alimentar o atlas |
|----------|----------------------|-------------------------|
| [01_perfil_exploratorio.ipynb](notebooks/01_perfil_exploratorio.ipynb) | Perfil raw, qualidade/chave e inventário temporal (unificado) | Domínios categóricos, granularidade, notas para integração histórica |
| [02_estrutura_trusted.ipynb](notebooks/02_estrutura_trusted.ipynb) | Estrutura trusted, nulos, ranking por UF e evolução em GO | Seção de qualidade / schema no atlas |

## Pipelines

```bash
# na raiz de anp-fuel-analytics

# 1. Brutos (portal ANP)
py estudos/tancagem-abastecimento/pipelines/download_raw.py

# 2. Trusted — união de todos os CSV/XLSX
py estudos/tancagem-abastecimento/pipelines/build_trusted.py
```

### Camada trusted

| Saída | Descrição |
|-------|-----------|
| `data/trusted/tancagem-abastecimento/tancagem.parquet` | Todos os snapshots empilhados (~492k linhas, 36 arquivos) |
| `data/trusted/tancagem-abastecimento/manifest.json` | Inventário por arquivo fonte |

Colunas originais + `_source_file`, `_source_year`, `_source_period`. Tipos normalizados (`Data` datetime, `TancagemM3` numérico).

```python
import pandas as pd
df = pd.read_parquet("data/trusted/tancagem-abastecimento/tancagem.parquet")
```

## Análises recomendadas (escopo futuro)

Lista completa no atlas (ranking empresas, geografia, HHI, etc.). Este repo implementa primeiro a **exploração** que destrava a integração histórica; análises de negócio podem vir em notebooks adicionais ou em outros projetos.

## TODOs / investigações abertas

- **[TODO.md](TODO.md)** — queda de tancagem em **nov/dez 2022** (~44% abaixo de jun–out/2022)

## Status

| Item | Situação |
|------|----------|
| Download raw | `pipelines/download_raw.py` |
| Camada trusted | `pipelines/build_trusted.py` — **concluído** |
| Notebooks exploratórios | `notebooks/` |
| Série mensal harmonizada (ref) | Planejada no **anp-data-atlas** |
