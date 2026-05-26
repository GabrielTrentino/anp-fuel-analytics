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

- [x] Trusted diesel por tipo (`vendas_diesel_tipo.parquet` — 21.465 linhas, 2013–2025)
- [x] Trusted GLP por vasilhame (`vendas_glp_vasilhame.parquet` — 12.474 linhas, 2007–2025)
- [x] Trusted biodiesel B100 (`vendas_biodiesel.parquet` — 1.852 linhas, origem×destino regional)
- [x] Trusted municipal (`vendas_municipal.parquet` — 666.699 linhas, 4 produtos, 1990–2024)
- [x] Notebook `01_perfil_exploratorio.ipynb` (9 seções: evolução, top 5, sazonalidade, diesel tipo, GLP, biodiesel, municipal, UF, segmento)
- [ ] Refined: join vendas × movimentação (comparar volumes SDC vs SIMP por UF/mês)
- [ ] Refined: join vendas × preços médios (receita estimada m³ × R$/L)
