# TODO — estudos anp-fuel-analytics

Rastreio alinhado ao [TODO do atlas](https://github.com/GabrielTrentino/anp-data-atlas/blob/main/TODO.md).

**Legenda:** `—` pendente · `◐` em andamento · `✓` concluído

## Prioridade combustíveis / abastecimento

| Slug | Doc atlas | Estudo local | Pipeline |
|------|-----------|--------------|----------|
| `tancagem-abastecimento` | ✓ | ✓ | ◐ |
| `movimentacao-derivados` | ✓ | ✓ | ◐ |
| `cadastro-revendas-combustiveis` | ✓ | ✓ | ◐ |
| `cadastro-revendas-glp` | ✓ | ✓ | ◐ |
| `pontos-abastecimento` | ✓ | ◐ | — (sem CSV público) |
| `distribuidores-combustiveis-liquidos` | ✓ | ✓ | ◐ |
| `pmqc` | ✓ | ✓ | ◐ |
| `pml` | ✓ | ✓ | ◐ |
| `serie-historica-precos` | ✓ | ✓ | ◐ |
| `vendas-derivados` | ✓ | ✓ | ◐ |
| `fiscalizacao-abastecimento` | ✓ | ✓ | ◐ |
| `capacidade-armazenagem-terminais` | ✓ | ✓ | ◐ |
| `movimentacao-terminais-aquaviarios` | ✓ | ✓ | ◐ |
| `registro-lubrificantes` | ✓ | ✓ | ◐ |

## Contexto oferta / macro

| Slug | Doc atlas | Estudo local | Pipeline |
|------|-----------|--------------|----------|
| `processamento-petroleo-derivados` | ✓ | ✓ | ◐ |
| `producao-biocombustiveis` | ✓ | ✓ | ◐ |
| `producao-por-estado` | ✓ | ✓ | ◐ |
| `producao-por-poco` | ✓ | ✓ | ◐ |
| `importacoes-exportacoes` | ✓ | ✓ | ◐ |
| `anuario-estatistico` | ✓ | — | — (sem CSV público) |

---

## Sugestões de análises futuras (refined layers / notebooks)

### 1. Balanço oferta-demanda nacional

**Datasets:** processamento + importacoes-exportacoes + vendas-derivados  
**Objetivo:** Para cada derivado (gasolina, diesel, QAV, GLP), calcular:  
`produção_refino + importação − exportação − vendas = estoque/perda`  
**Valor:** Identificar gargalos logísticos e dependência externa por produto.

### 2. Mapa de qualidade vs fiscalização

**Datasets:** pmqc + fiscalizacao-abastecimento + cadastro-revendas-combustiveis  
**Objetivo:** Correlacionar taxa de não-conformidade (PMQC) com frequência de fiscalizações por município/UF.  
**Valor:** Detectar regiões com alta não-conformidade e baixa fiscalização (risco).

### 3. Eficiência logística costeira

**Datasets:** movimentacao-terminais-aquaviarios + capacidade-armazenagem-terminais + vendas-derivados  
**Objetivo:** Taxa de utilização de terminais (volume movimentado / capacidade) e correlação com vendas regionais.  
**Valor:** Mapear terminais subutilizados ou sobrecarregados.

### 4. Cadeia do etanol: produção → venda

**Datasets:** producao-biocombustiveis + vendas-derivados + importacoes-exportacoes  
**Objetivo:** Tracking regional: onde se produz etanol (anidro/hidratado) e onde se consome.  
**Valor:** Analisar autossuficiência por UF e fluxos interregionais implícitos.

### 5. Preço vs qualidade no varejo

**Datasets:** serie-historica-precos + pmqc + cadastro-revendas-combustiveis  
**Objetivo:** Postos com preço muito abaixo da média têm mais não-conformidades no PMQC?  
**Valor:** Indicador de adulteração potencial baseado em padrão estatístico.

### 6. Evolução do parque refinador

**Datasets:** processamento-petroleo-derivados + producao-por-estado  
**Objetivo:** Série temporal do mix de derivados por refinaria, vs evolução da produção primária (petróleo).  
**Valor:** Avaliar tendências de desinvestimento/expansão do parque refinador.

### 7. Concentração de mercado por segmento

**Datasets:** distribuidores-combustiveis-liquidos + cadastro-revendas-combustiveis + cadastro-revendas-glp  
**Objetivo:** HHI (Índice Herfindahl) por UF/município para distribuidores e revendedores.  
**Valor:** Mapear concentração de mercado e potencial poder de mercado.

### 8. Declínio de produção por poço/campo

**Datasets:** producao-por-poco (série completa 2005-2023)  
**Objetivo:** Curva de declínio por campo, classificação de maturidade.  
**Valor:** Projeção de produção futura e identificação de campos em depleção avançada.

### 9. Lubrificantes: registro vs qualidade

**Datasets:** registro-lubrificantes + pml  
**Objetivo:** Marcas registradas mas não amostradas no PML; marcas com alta reprovação.  
**Valor:** Identificar gaps de monitoramento e detentores com recorrência de não-conformidade.

### 10. Sazonalidade integrada

**Datasets:** vendas-derivados + serie-historica-precos + producao-biocombustiveis  
**Objetivo:** Padrões sazonais coordenados: preço sobe quando vendas sobem? Produção etanol cai na entressafra?  
**Valor:** Modelar ciclos de mercado para planejamento de estoque e precificação.

---

## Pendências técnicas

- [ ] Trusted layer para `ce-cr.csv` (contratos de cessão — distribuidores-combustiveis-liquidos)
- [ ] Download histórico completo producao-por-poco (2005-2022)
- [ ] Importação de gás natural: trusted separado (importacao-gas-natural.csv)
- [ ] Notebooks exploratórios (`01_perfil_exploratorio.ipynb`) para todos os estudos
- [ ] Refined layers: implementar ao menos 3 das análises sugeridas acima
