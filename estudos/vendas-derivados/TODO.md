# TODO — vendas-derivados

## Concluído

- [x] Download raw (14 arquivos: série principal, segmento, tipo, biodiesel, município)
- [x] Prepare (normalização headers + mês abreviado → numérico)
- [x] Trusted mensal (`vendas_mensal.parquet` — 93.960 linhas, 1990–2026)
- [x] Trusted segmento (`vendas_segmento.parquet` — 41.553 linhas, 2012–2026)
- [x] Config `monorepo.yaml`
- [x] Cruzamento movimentação e preços (ver `cruzamento_resultado.md`)
- [x] Documentação README + TODO

## Pendente

- [ ] Trusted diesel por tipo
- [ ] Trusted GLP por vasilhame
- [ ] Trusted biodiesel B100
- [ ] Trusted municipal (gasolina, diesel, etanol, GLP)
- [ ] Notebook `01_perfil_exploratorio.ipynb` (evolução temporal, sazonalidade)
- [ ] Refined: join vendas × movimentação (comparar volumes SDC vs SIMP por UF/mês)
- [ ] Refined: join vendas × preços médios (receita estimada m³ × R$/L)
