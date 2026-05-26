# TODO — pmqc

## Concluído

- [x] Download raw (26 CSVs, 2024–2026, nomes inconsistentes por ano)
- [x] Profile (19 colunas, schema consistente, UTF-8-sig, sep `;`)
- [x] Prepare (concat 26 arquivos → `_prepared/pmqc_all.csv`)
- [x] Trusted (`pmqc.parquet` — 2.231.308 ensaios)
- [x] Config `monorepo.yaml`
- [x] Cruzamento preços LPC (29,3% overlap) e não-conformidades
- [x] Documentação README + TODO

## Pendente

- [ ] Download anos anteriores (2016–2023) via `--years`
- [ ] Trusted cadastro-revendas para cruzamento CNPJ completo
- [ ] Notebook `01_perfil_exploratorio.ipynb` (distribuição geográfica, sazonalidade não-conformidade)
- [ ] Refined: join PMQC × preços (postos não-conformes praticam preço diferente?)
- [ ] Refined: série temporal taxa não-conformidade por UF/produto
- [ ] Análise: postos amostrados no PMQC que NÃO constam no cadastro
