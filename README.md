# anp-fuel-analytics

Monorepo de **estudos** sobre dados abertos de combustíveis da ANP, com foco em **transformação de dados** (ingestão, limpeza, harmonização) e análises derivadas. Cada estudo vive em sua própria pasta, com pipelines, notebooks e artefatos locais.

Complementa o [anp-data-atlas](https://github.com/GabrielTrentino/anp-data-atlas): o atlas documenta fontes, metadados e contexto; **este repositório implementa o trabalho analítico**.

## Objetivo

Reunir, de forma reproduzível, o caminho desde os **CSV brutos** da ANP até **métricas e visões** úteis para entender o abastecimento nacional — começando pela **tancagem autorizada a operar**, sem misturar documentação de referência com código de transformação.

Em cada estudo buscamos:

1. **Ingerir** os arquivos publicados no portal da ANP  
2. **Transformar** (tempo, qualidade, agregações) em camadas utilizáveis  
3. **Analisar** conforme um roteiro explícito de perguntas de negócio  

Dados brutos e processados permanecem **fora do Git** (`data/` local). O que versionamos é código, notebooks e documentação do estudo.

## Estudos

| Estudo | Pasta | Status |
|--------|-------|--------|
| Tancagem do Abastecimento Nacional de Combustíveis | [estudos/tancagem-abastecimento/](estudos/tancagem-abastecimento/) | Em andamento |

Novos conjuntos da ANP entram como pastas em `estudos/{slug}/`, após estarem catalogados no atlas.

## Estrutura do monorepo

```
anp-fuel-analytics/
├── estudos/
│   └── tancagem-abastecimento/   # README do estudo + pipelines + notebooks
├── data/                         # local — não versionado (por estudo, sob data/)
└── README.md
```

Padrão sugerido dentro de cada estudo:

```
estudos/{slug}/
├── README.md
├── pipelines/
├── notebooks/
└── src/              # opcional
```

## Repositórios relacionados

| Repositório | Papel |
|-------------|--------|
| [anp-data-atlas](https://github.com/GabrielTrentino/anp-data-atlas) | Referência: catálogo, dicionários, URLs, lacunas |
| **anp-fuel-analytics** | Monorepo de estudos: transformação e análise |

## Licença

Código sob [MIT](LICENSE). Dados originais da ANP sujeitos aos termos da agência.

https://github.com/GabrielTrentino/anp-fuel-analytics
