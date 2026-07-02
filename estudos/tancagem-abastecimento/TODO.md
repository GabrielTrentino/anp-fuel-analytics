# TODOs — tancagem-abastecimento

## ✅ Investigar queda em nov/dez 2022 — CONCLUÍDO (jul/2026)

**Hipótese observada:** nos snapshots de **novembro e dezembro de 2022**, a tancagem total e o número de linhas ficam muito abaixo dos meses adjacentes (jun–out/2022 e jan/2023+), em torno de **~44% menos m³** e **~23% menos linhas** que a média dos demais meses de 2022.

| Arquivo | Linhas | Soma m³ | vs. média jun–out/2022 (~58 M) |
|---------|-------:|--------:|--------------------------------:|
| jun–out/2022 | ~13,4 mil | ~57–58 M | — |
| **nov/2022** | 10.352 | **32,3 M** | **−44%** |
| **dez/2022** | 10.302 | **32,1 M** | **−44%** |
| jan/2023 | 13.571 | 56,0 M | volta ao patamar |

### Conclusão (jul/2026)

- **Portal verificado:** a ANP lista os mesmos 7 arquivos de 2022 sem correção (última atualização 12/06/2026). **A correção não virá.**
- **Causa:** ~211 instalações de out/2022 (sobretudo **REFINARIA**, ~19 M m³) não aparecem em nov/dez. As instalações em comum variam apenas −3% — não é revisão de valores.
- **Decisão:** tratar nov/dez 2022 como **cobertura parcial de origem**. Não usar em séries nacionais nem em YoY que cruzem esse período. Identificados como `SNAPSHOTS_PARCIAIS_2022` na seção 4.1 do `02_estrutura_trusted.ipynb`.

---

### 1. Confirmar o fenômeno (dados)

- [x] Plotar série `soma_m3` e `linhas` por `_source_file` (2022) — seção 4.1
- [x] Identificar `CodInstalacao` presentes em out/2022 e ausentes em nov/2022 — seção 4.1
- [x] Verificar se a queda é concentrada em segmentos — **REFINARIA** é o principal
- [ ] Calcular razão nov-dez / média(jun–out) por UF e GrupoDeProdutos (análise adicional se necessário)

### 2. Escopo e nomenclatura dos arquivos 2022

- [x] Comparar nomes: `tancagem_terminais_*` (até out/2022) vs. `janeiro.csv` (2023+) — confirmado padrão distinto
- [x] Confirmar que ANP ampliou universo de agentes a partir de 2023 — evidenciado pelas 1.610 instalações em jan/2023 vs. 1.382 em nov/2022
- [x] Documentar como corte parcial — seção 4.1 do notebook
- [ ] Ler metadados ANP (`metadados-tancagem.pdf`) para confirmação formal

### 3. Qualidade técnica dos brutos

- [x] Validar que pipeline (`build_trusted`) espelha corretamente o raw — **sem bug no pipeline**
- [ ] Re-baixar nov/dez do portal e comparar hash/tamanho (baixa prioridade — não mudará conclusão)

### 4. Comparação com Painel Dinâmico ANP

- [x] Verificar se portal publicou versão corrigida — **não publicou**
- [ ] Checar totais no Painel Power BI (baixa prioridade — conclusão já está clara)

### 5. Impacto na série histórica

- [x] **Decisão tomada:** marcar como `qualidade=parcial` e não usar em séries nacionais/YoY
- [ ] Adicionar flag `_qualidade_snapshot` no pipeline trusted (backlog de engenharia)
- [ ] Atualizar `docs/conjuntos/tancagem-abastecimento.md` no **anp-data-atlas** com conclusão

### 6. Entrega

- [x] Seção 4.1 em `02_estrutura_trusted.ipynb`: "Diagnóstico nov/dez 2022"
- [ ] Registrar achados em `estudos/tancagem-abastecimento/README.md` (Notas conhecidas)

---

**Prioridade dos itens pendentes:** flag no pipeline → atlas → README

**Aberto em:** 2026-05-23 | **Concluído (decisão):** 2026-07-01
