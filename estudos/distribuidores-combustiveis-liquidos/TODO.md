# TODO — distribuidores-combustiveis-liquidos

## Concluído

- [x] Download raw (planilha-aea-filiais, ce-cr, inutilizadores + metadados)
- [x] Profile (3 CSVs: AEA 713 linhas, CE-CR 1.888, Inutilizadores 36)
- [x] Prepare (parser report-style → distribuidores_aea.csv)
- [x] Trusted (`distribuidores.parquet` — 713 distribuidores)
- [x] Config `monorepo.yaml`
- [x] Cruzamento com movimentação
- [x] Documentação README + TODO

## Pendente

- [ ] Trusted contratos cessão (ce-cr.csv — resolver encoding)
- [ ] Notebook exploratório (mapa distribuidores por UF, timeline autorizações)
- [ ] Refined: join distribuidores × movimentação por CNPJ
- [ ] Análise: distribuidores cancelados/revogados vs ativos (timeline)
