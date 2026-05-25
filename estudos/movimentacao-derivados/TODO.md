# TODOs — movimentacao-derivados

Rastreio técnico e fila de análises. Sugestões temáticas completas: [atlas — movimentacao-derivados.md](https://github.com/GabrielTrentino/anp-data-atlas/blob/main/docs/conjuntos/movimentacao-derivados.md#sugestões-de-análises).

---

## Validar ligação com tancagem e cadastros

**Observado (2026-05):** CSVs SIMP **sem** `Cnpj`/`CodInstalacao` — agente = **`Agente Regulado`** ou **`Código do Regulado - ANP`**.

| Hipótese | Status |
|----------|--------|
| Join tancagem via nome + UF | ✓ 30,4% match — [cruzamento_tancagem_resultado.md](cruzamento_tancagem_resultado.md) |
| Join via código ANP (lubrificante) | pendente |
| Join via cadastro revendas (CNPJ) | **próximo conjunto** |

- [x] Cruzar `Liquidos_Vendas_Atual` × `tancagem.parquet`
- [ ] Fuzzy match nome (Levenshtein / alias) — subir taxa além de 57% só-nome
- [ ] Verificar cadastro revendas: `Cnpj` + razão social + código instalação
- [x] Documentar no atlas

---

## Arquivo histórico sem cabeçalho

`liquidos/Liquidos_Vendas_Historico_2007_a_2017.csv` — 710.831 linhas, separador `;`, sem header.

- [x] Schema fixo → `*_normalizado.csv` (`prepare_movimentacao_raw.py`)
- [ ] Validar totais 2017: histórico normalizado vs `Liquidos_Vendas_Atual`
- [ ] Confirmar campos no PDF `metadado-unificado-logistica.pdf`

---

## Unidades de volume

| Família | Coluna | Unidade |
|---------|--------|---------|
| Líquidos, TRR, aviação | `Quantidade de Produto (mil m³)` | mil m³ |
| GLP (parte) | `Quantidade de Produto(mil ton)` | mil ton |
| Lubrificantes | `Volume(L)` | litros |
| Logística | `Qtd Produto Líquido` | validar (possível litros) |

- [ ] Ler PDF e documentar fator de conversão
- [x] Manter famílias separadas no trusted (não somar L + mil m³)

---

## Pipeline trusted/refined

- [x] `prepare_movimentacao_raw.py`
- [x] `trusted_liquidos_vendas.sql` → `liquidos_vendas_atual.parquet`
- [ ] Trusted: entregas + importação (líquidos)
- [ ] Trusted: GLP, TRR, lubrificante, logística
- [ ] Refined: agregado mês × UF origem × produto × agente

---

## Próximas análises

Fila priorizada (espelha [Sugestões de análises](https://github.com/GabrielTrentino/anp-data-atlas/blob/main/docs/conjuntos/movimentacao-derivados.md#sugestões-de-análises) no atlas). Métrica base: **volume** na unidade correta da família.

### 1. Série temporal e qualidade da base

- [ ] Plotar volume mensal total — `liquidos_vendas_atual.parquet` (2017–2026)
- [ ] Comparar soma 2017: histórico normalizado vs vendas atual (evitar dupla contagem 2023–24)
- [ ] Listar produtos (`codigo_produto`) com maior volume e maior variação YoY
- [ ] Detectar meses com queda abrupta de linhas ou volume (outliers regulatórios)

### 2. Geografia e fluxos (líquidos)

- [ ] Heatmap **UF origem × UF destino** — gasolina C e diesel (top fluxos)
- [ ] Ranking UF destino por `Mercado Destinatário` = consumidor final
- [ ] Série por UF origem — quais estados mais exportam volume (proxy produção/refino)
- [ ] Cruzar `Liquidos_Importacao_de_Distribuidores` com matriz origem-destino

### 3. Agentes e concentração

- [ ] Top 20 `agente_regulado` por volume (últimos 12 meses)
- [ ] HHI ou share top 5 por produto (gasolina C, diesel S10, etanol)
- [ ] Agentes presentes em movimentação mas **sem** match tancagem (lista dos 488 nome+UF)
- [ ] Após cadastro revendas: join CNPJ e recalcular match tancagem

### 4. Capacidade vs movimentação (com tancagem)

- [ ] Para os 213 matches nome+UF: razão `volume_mil_m3` / `TancagemM3` por mês (proxy intensidade)
- [ ] Outliers: alto volume com baixa tancagem (ou vice-versa) — validar sigilo/agregação
- [ ] Por segmento tancagem (TRR, distribuidor…) vs produto movimentado

### 5. Outras famílias de produto

- [ ] GLP: série vendas atual vs histórico (mil ton → m³ se fator conhecido)
- [ ] TRR: volume por `TRR_Vendas_TRR_Atual` vs distribuidor
- [ ] Lubrificante Anexo B: explorar `Código do Regulado - ANP` + volume(L)
- [ ] Logística 01–03: validar unidade e comparar totais com líquidos agregados

### 6. Cruzamentos externos (após cadastro / vendas / preços)

- [ ] Movimentação × **vendas-derivados** — mesmo mês, UF, produto (divergência SIMP vs SDC)
- [ ] Movimentação × **série histórica preços** — correlação volume UF destino vs preço regional
- [ ] Movimentação × **cadastro postos** — densidade de revendas vs volume destino no município (quando geo disponível)

### 7. Entrega

- [ ] Seção em `01_perfil_exploratorio.ipynb` ou `02_fluxos_liquidos.ipynb` por tema acima
- [ ] Promover conclusões estáveis para `docs/conjuntos/movimentacao-derivados.md` (atlas)
- [ ] Atualizar [variaveis-conjuntos.md](https://github.com/GabrielTrentino/anp-data-atlas/blob/main/docs/variaveis-conjuntos.md) se novas chaves forem confirmadas

---

**Prioridade sugerida:** 1 → 3 → 4 → 2 → 5 → 6 → 7

**Dependências:** análise 4 e 6(b) melhoram após **cadastro-revendas-combustiveis**; análise 5(e) após trusted logística.

**Aberto em:** 2026-05-24 · **Atualizado:** 2026-05-24
