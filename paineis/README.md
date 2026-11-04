# Painéis públicos (Evidence)

Site estático com os dados abertos da ANP processados por este repositório, feito com
[Evidence](https://github.com/evidence-dev/evidence) (SQL + Markdown) e publicado no GitHub Pages.

| Página | Fonte (trusted) |
|---|---|
| `pages/precos.md` | `serie-historica-precos/lpc_posto.parquet` |
| `pages/pmqc.md` | `pmqc/pmqc.parquet` |
| `pages/vendas.md` | `vendas-derivados/vendas_mensal.parquet` |
| `pages/revendas.md` | `cadastro-revendas-combustiveis/revendas.parquet` |
| `pages/qualidade-dos-dados.md` | `data/quality/*.json` |

## Como os dados chegam ao site

Os Parquets do pipeline têm milhões de linhas e não vão para o git. `exportar.py` agrega as saídas em tabelas
pequenas e grava um único arquivo, `sources/anp/anp_paineis.duckdb` (poucos MB), que é versionado. O site só lê
esse arquivo.

```bash
py pipelines/run.py all --skip-raw     # atualiza trusted/refined e os relatórios de qualidade
py pipelines/run.py paineis            # regera sources/anp/anp_paineis.duckdb
git add paineis/sources/anp/anp_paineis.duckdb && git commit -m "dados: atualiza painéis"
```

Ao chegar na `main`, o workflow `.github/workflows/paineis.yml` monta o site e publica em
`https://gabrieltrentino.github.io/anp-fuel-analytics/`. Em PR ele só valida o build.

## Rodar localmente

```bash
cd paineis
npm ci
npm run sources     # lê o .duckdb e prepara os dados das páginas
npm run dev         # abre http://localhost:3000
```

Para criar uma página nova: acrescente o agregado em `EXTRATOS` (`exportar.py`), um `sources/anp/<tabela>.sql`
com `select * from <tabela>` e a página em `pages/`. O teste `tests/test_paineis.py` confere que toda tabela
usada pelas páginas existe no extrato.

Observação: este é o framework aberto do Evidence (`@evidence-dev/evidence` 40.x). A empresa passou a focar no
Evidence Studio (hospedado); o framework aberto segue funcionando para sites estáticos, mas recebe menos
atualizações.
