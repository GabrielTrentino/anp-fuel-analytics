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
| [01_perfil_exploratorio.ipynb](notebooks/01_perfil_exploratorio.ipynb) | Schema, nulos, cardinalidade, domínios categóricos | Tabela de valores de `Segmento`, `GrupoDeProdutos`, etc. |
| [02_qualidade_chave.ipynb](notebooks/02_qualidade_chave.ipynb) | Chave lógica, duplicatas, `TancagemM3`, CNPJ | Seção “granularidade e agregação” |
| [03_piloto_temporal.ipynb](notebooks/03_piloto_temporal.ipynb) | Inventário dos arquivos baixados, linhas por snapshot | Notas para pipeline de integração histórica no atlas |

## Download dos brutos

```bash
# na raiz de anp-fuel-analytics
py estudos/tancagem-abastecimento/pipelines/download_raw.py
```

## Análises recomendadas (escopo futuro)

Lista completa no atlas (ranking empresas, geografia, HHI, etc.). Este repo implementa primeiro a **exploração** que destrava a integração histórica; análises de negócio podem vir em notebooks adicionais ou em outros projetos.

## Status

| Item | Situação |
|------|----------|
| Download CSV | Script em `pipelines/download_raw.py` |
| Notebooks exploratórios | Iniciais em `notebooks/` |
| Integração histórica | Planejada no **anp-data-atlas** |
