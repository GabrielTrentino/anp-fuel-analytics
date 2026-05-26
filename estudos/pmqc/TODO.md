# TODO — pmqc

## Concluído

- [x] Download raw (26 CSVs, 2024–2026, nomes inconsistentes por ano)
- [x] Profile (19 colunas, schema consistente, UTF-8-sig, sep `;`)
- [x] Prepare (concat 26 arquivos → `_prepared/pmqc_all.csv`)
- [x] Trusted (`pmqc.parquet` — 2.231.308 ensaios)
- [x] Config `monorepo.yaml`
- [x] Cruzamento preços LPC (29,3% overlap) e não-conformidades
- [x] Documentação README + TODO
- [x] Download anos anteriores (2016–2023) via `--years` — 100 arquivos, 0 falhas
- [x] Rebuild trusted (8.424.805 ensaios, 48.249 CNPJs, 2016-01 a 2026-04)
- [x] Notebook `01_perfil_exploratorio.ipynb` (8 seções: evolução, NC por UF/produto, cruzamento cadastro)
- [x] Refined: série temporal taxa não-conformidade por UF/produto (`nao_conformidade_uf_produto.parquet`)
- [x] Refined: join PMQC × preços (`pmqc_precos_join.parquet` + `resumo_preco_conformidade.parquet`)
- [x] Análise: postos PMQC que NÃO constam no cadastro (11.407 = 23,6% dos CNPJs)

## Resultados-chave

- **8,4M ensaios** — série 2016-01 a 2026-04
- **Taxa NC média:** 0,017% por UF/mês/produto (muito baixa por ensaio)
- **Overlap PMQC × Cadastro:** 76,4% (36.842 CNPJs)
- **Postos fora do cadastro:** 11.407 — concentrados em SP, MG, RS
- **PMQC × Preços (LPC):** 4.459 CNPJs em comum; postos NC → preço ligeiramente menor
