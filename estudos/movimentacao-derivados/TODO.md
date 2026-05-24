# TODOs — movimentacao-derivados

## Validar ligação com tancagem e cadastros

**Observado na exploração raw (2026-05):** os CSVs SIMP de movimentação **não trazem** `Cnpj` nem `CodInstalacao` — o agente aparece como **`Agente Regulado`** (razão social) ou **`Código do Regulado - ANP`** / **`Código Agente Regulado`** (em sub-bases específicas).

| Hipótese | Próximo passo |
|----------|---------------|
| Join com tancagem via nome empresarial | Normalizar `Agente Regulado` ↔ `NomeEmpresarial`; medir taxa de match |
| Join via código ANP do regulado | Mapear `Código do Regulado - ANP` (lubrificante Anexo B) com cadastro i-SIMP |
| Join geo | `UF Origem`/`UF Destino` + `Produto` + `Ano`/`Mês` — agregado, não instalação |

- [ ] Cruzar amostra `Liquidos_Vendas_Atual` com `tancagem.parquet` por nome + UF
- [ ] Verificar se cadastro revendas traz código ANP além de CNPJ
- [ ] Documentar conclusão no atlas (`movimentacao-derivados.md`)

---

## Arquivo histórico sem cabeçalho

`liquidos/Liquidos_Vendas_Historico_2007_a_2017.csv` — **710.831 linhas sem linha de cabeçalho** (primeira linha já é dado).

- [ ] Confirmar layout oficial no PDF `metadado-unificado-logistica.pdf`
- [ ] Definir schema fixo na ingestão (Ano, Mês, Agente, Código Produto, …)
- [ ] Validar totais contra `Liquidos_Vendas_Atual` no overlap 2017

---

## Unidades de volume

| Família | Coluna típica | Unidade declarada |
|---------|---------------|-------------------|
| Líquidos, GLP (maioria), TRR, aviação | `Quantidade de Produto (mil m³)` | mil m³ |
| GLP (parte) | `Quantidade de Produto(mil ton)` | mil ton |
| Lubrificantes | `Volume(L)` / `Volume(mil m³)` | litros ou mil m³ |
| Logística | `Qtd Produto Líquido` | **validar** (valores brutos altos — possível litros) |

- [ ] Ler metadados PDF e harmonizar unidade na camada trusted
- [ ] Não somar lubrificante (L) com líquidos (mil m³) sem conversão

---

## Pipeline trusted/refined

- [ ] `prepare_movimentacao_raw.py` — empilhar por produto/tipo de tabela
- [ ] `trusted.sql` — schema unificado mínimo: `periodo`, `produto`, `agente`, `uf_origem`, `uf_destino`, `volume_m3`, `_source_file`
- [ ] Entrada em `pipelines/run.py` / `monorepo.yaml` (steps trusted+)

---

**Prioridade sugerida:** ligação agente → tancagem/cadastro → histórico sem header → unidades → pipeline

**Aberto em:** 2026-05-24
