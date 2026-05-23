# TODOs — tancagem-abastecimento

## Investigar queda em nov/dez 2022

**Hipótese observada:** nos snapshots de **novembro e dezembro de 2022**, a tancagem total e o número de linhas ficam muito abaixo dos meses adjacentes (jun–out/2022 e jan/2023+), em torno de **~44% menos m³** e **~23% menos linhas** que a média dos demais meses de 2022.

| Arquivo | Linhas | Soma m³ | vs. média jun–out/2022 (~58 M) |
|---------|-------:|--------:|--------------------------------:|
| jun–out/2022 | ~13,4 mil | ~57–58 M | — |
| **nov/2022** | 10.352 | **32,3 M** | **−44%** |
| **dez/2022** | 10.302 | **32,1 M** | **−44%** |
| jan/2023 | 13.571 | 56,0 M | volta ao patamar |

Fonte: `data/trusted/tancagem-abastecimento/manifest.json` (gerado por `build_trusted.py`).

---

### 1. Confirmar o fenômeno (dados)

- [ ] Plotar série `soma_m3` e `linhas` por `_source_file` (2022) no notebook ou novo script
- [ ] Calcular razão nov-dez / média(jun–out) por **UF**, **Segmento** e **GrupoDeProdutos**
- [ ] Identificar **CNPJs** ou **`CodInstalacao`** presentes em out/2022 e ausentes em nov/2022 (e vice-versa)
- [ ] Verificar se a queda é uniforme ou concentrada em segmentos (ex.: só terminais, só TRR)

### 2. Escopo e nomenclatura dos arquivos 2022

- [ ] Ler metadados ANP (`metadados-tancagem.pdf`) e notas da página publicada em **jun/2022** — série iniciou nesse mês
- [ ] Comparar nomes: arquivos até out/2022 usam prefixo `tancagem_terminais_*` — **nov/dez também?** Escopo era só terminais?
- [ ] Conferir se a ANP ampliou o universo de agentes reportados a partir de **2023** (quando nomes passam a `janeiro.csv`, etc.)
- [ ] Documentar no atlas se nov/dez/2022 representam **corte parcial** da base, não queda real de capacidade

### 3. Qualidade técnica dos brutos

- [ ] Abrir CSV nov/dez 2022 lado a lado com out/2022: mesmo header, mesmas colunas, encoding
- [ ] Contar linhas vazias / mal parseadas (comparar com as **52+41 linhas** totalmente nulas já vistas em outros arquivos)
- [ ] Validar se out/2022 (`.xlsx`) e nov/dez (`.csv`) têm regras de ingestão diferentes no `build_trusted.py`
- [ ] Re-baixar nov/dez do portal e comparar hash/tamanho com cópia local

### 4. Comparação com Painel Dinâmico ANP

- [ ] No [Painel de Tancagem](https://www.gov.br/anp/pt-br/centrais-de-conteudo/paineis-dinamicos-da-anp/painel-dinamico-da-tancagem-do-abastecimento-nacional-de-combustiveis), checar totais nacionais em nov/dez 2022 vs. out/2022
- [ ] Se o painel mostrar patamar estável, tratar nov/dez CSV como **publicação incompleta**
- [ ] Se o painel também cair, investigar mudança regulatória ou operacional na época

### 5. Impacto na série histórica

- [ ] Decidir tratamento para integração histórica:
  - excluir nov/dez 2022 da série agregada;
  - marcar como `qualidade=parcial`;
  - ou interpolar / carry-forward (documentar risco)
- [ ] Avaliar efeito em análises por UF (ex.: evolução GO) — nov/dez 2022 aparecem como “degrau” artificial?
- [ ] Atualizar `docs/conjuntos/tancagem-abastecimento.md` no **anp-data-atlas** com conclusão

### 6. Entrega

- [ ] Notebook ou seção em `02_estrutura_trusted.ipynb`: “Diagnóstico nov/dez 2022”
- [ ] Registrar achados em `estudos/tancagem-abastecimento/README.md` (Status / Notas conhecidas)
- [ ] Se confirmado bug da ANP, considerar issue ou contato via `faleconosco@anp.gov.br` (metadados)

---

**Prioridade sugerida:** 1 → 2 → 3 → 4 → 5 → 6

**Responsável:** _a definir_

**Aberto em:** 2026-05-23
