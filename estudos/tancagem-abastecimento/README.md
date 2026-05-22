# Estudo: Tancagem do Abastecimento Nacional de Combustíveis

**Slug:** `tancagem-abastecimento`  
**Título oficial (ANP):** Tancagem Autorizada a Operar  
**Documentação de referência:** [anp-data-atlas — tancagem-abastecimento.md](https://github.com/GabrielTrentino/anp-data-atlas/blob/main/docs/conjuntos/tancagem-abastecimento.md)

## Resumo

Este estudo trata da **capacidade de armazenagem** (tancagem, em m³) das instalações autorizadas pela ANP — tanques, vasos de pressão e esferas cadastrados no **SIMP**. Os CSV publicados mensalmente (desde jun/2022) permitem analisar quanto volume as instalações estão autorizadas a operar, por empresa, segmento, grupo de produto e localidade.

**Não é estoque físico nem ocupação em tempo real** — é capacidade operacional cadastrada.

| Item | Detalhe |
|------|---------|
| Fonte | [Dados abertos — Tancagem](https://www.gov.br/anp/pt-br/centrais-de-conteudo/dados-abertos/tancagem-do-abastecimento-nacional-de-combustiveis) |
| Formato | CSV (+ PDF de metadados) |
| Frequência | Mensal (com blocos e lacunas documentados no atlas) |
| Métrica base | Soma de `TancagemM3` |
| Granularidade | `CodInstalacao` × `Tag` × `GrupoDeProdutos` por snapshot |
| Dados locais | `data/raw/tancagem-abastecimento/` e `data/processed/tancagem-abastecimento/` |

## Objetivo do estudo

1. Construir pipeline de **ingestão e transformação** (harmonizar série temporal, qualidade, agregações).  
2. Executar as **análises recomendadas** abaixo sobre a série consolidada.  
3. Deixar notebooks e scripts reproduzíveis para reutilização em outros projetos.

## Transformações previstas

| Etapa | Descrição |
|-------|-----------|
| Download | CSVs por ano/mês conforme matriz de arquivos no atlas |
| Harmonização temporal | Blocos multi-mês (`marco-julho`, `maio-junho`, …); lacunas (abr/2025, jul/2023) |
| Série 2022 | Padronizar colunas; tratar out/2022 (XLSX) |
| Enriquecimento | `ano`, `mes_referencia`, macro-região a partir de `Uf` |
| Qualidade | Chave lógica, duplicatas, CNPJ, nulos, outliers |
| Saídas | Snapshots limpos; agregados mensais (Brasil, UF, empresa, município) |

**Regra de agregação:** somar `TancagemM3` no nível desejado sem contar a mesma `Tag` duas vezes no mesmo snapshot. A coluna `Data` reflete a **publicação** na página da ANP — usar nome do arquivo e regras do ETL para o mês de referência.

## Análises recomendadas

Métrica base: **soma de `TancagemM3`**. Granularidade fonte: **unidade (`Tag`) × instalação × grupo de produto**.

### Visão nacional e evolução histórica

- Tancagem total do Brasil por mês (jun/2022 → hoje), em m³ (e conversões documentadas, se aplicável)
- Evolução por `GrupoDeProdutos` — derivados/biocombustíveis, GLP, petróleo, outros
- Evolução por `Segmento` — distribuidores, TRR, produtores, terminais, etc.
- Sazonalidade e rupturas — mudanças regulatórias, crises, novos agentes no SIMP
- Crescimento acumulado — variação % em 12 meses, 24 meses e desde 2022

### Empresas e mercado

- Ranking de empresas (`Cnpj` / `NomeEmpresarial`) por tancagem total e por grupo de produto
- Desenvolvimento da tancagem por empresa — série temporal por CNPJ
- Entrada e saída de players — CNPJs ou `CodInstalacao` que surgem ou deixam a base
- Concentração do setor — HHI ou participação dos top 5 / top 10 por segmento
- Expansão por instalação — novas `Tag`, aumento de `TancagemM3`, mudança de `DetalheInstalacao`

### Geografia: município, UF e região

- Tancagem por UF — ranking e evolução temporal
- Tancagem por município — principais cidades; capacidade per capita (cruzamento IBGE, fase futura)
- Tancagem por macro-região — Norte, Nordeste, Centro-Oeste, Sudeste, Sul
- Dependência local — municípios com baixa vs. alta capacidade relativa
- Hotspots — municípios com muitas instalações de terminal ou base TRR

### Instalações e infraestrutura

- Capacidade média por tanque — média/mediana de `TancagemM3` por `Tag` ou instalação
- Número de unidades — contagem de `Tag` por instalação, segmento ou UF
- Mix de `TipoDaUnidade` — tanque vs. vaso de pressão vs. esfera (relevante para GLP)
- Instalações de grande porte — top `CodInstalacao` por soma de m³; outliers (ex. > 100 mil m³)

### Recortes temáticos

- GLP vs. derivados — dinâmica comparada de capacidade autorizada
- TRR e bases de distribuição — `Segmento` TRR e `DetalheInstalacao` (exclusiva/compartilhada)
- Terminais vs. revenda — validação cruzada com [Capacidade de Armazenagem de Terminais](https://www.gov.br/anp/pt-br/centrais-de-conteudo/dados-abertos/capacidade-de-armazenagem-de-terminais)

### Cruzamentos (fases futuras)

- Revendas e postos — cadastro de revendas / pontos de abastecimento
- Movimentação de derivados — capacidade instalada vs. volume movimentado
- Preços — série histórica de preços vs. expansão regional de tancagem
- População e frota — IBGE, DENATRAN para normalização per capita / por km²

### Qualidade e método

- Harmonizar lacunas e blocos multi-mês ao montar painéis mensais
- ETL dedicado para arquivos de 2022 antes de concatenar a série
- Deixar explícito: `TancagemM3` = capacidade cadastrada, não estoque físico
- Padronizar `Municipio` antes de agregações geográficas

## Estrutura deste estudo (a implementar)

```
estudos/tancagem-abastecimento/
├── README.md           # este arquivo
├── pipelines/
├── notebooks/
└── src/                # opcional

data/                   # na raiz do monorepo — não versionado
├── raw/tancagem-abastecimento/
└── processed/tancagem-abastecimento/
```

## Status

| Item | Situação |
|------|----------|
| Documentação de referência (atlas) | Disponível |
| Pipeline de download | A implementar |
| Série consolidada | A implementar |
| Análises da lista acima | A implementar |
