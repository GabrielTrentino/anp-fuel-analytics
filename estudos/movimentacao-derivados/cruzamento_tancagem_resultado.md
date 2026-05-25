# Cruzamento movimentacao x tancagem

Amostra: `liquidos/Liquidos_Vendas_Atual.csv` x `tancagem.parquet` (trusted).
Normalizacao: nome sem acento/pontuacao + UF.

| Metrica | Valor |
|---------|------:|
| Agentes unicos movimentacao (nome+UF origem) | 701 |
| Empresas unicas tancagem (nome+UF instalacao) | 1,550 |
| Match exato nome+UF | 213 (30.4% dos agentes mov) |
| Match so por nome (ignora UF) | 122 (57.0% dos 214 nomes mov) |
| Nome mov presente em tancagem (qualquer UF) | 122 (57.0%) |

## Interpretacao

- Movimentacao usa **UF Origem** do fluxo; tancagem usa **UF da instalacao** — por isso match nome+UF e moderado (~30%).
- Para join operacional: priorizar **nome normalizado** + validar UF; ou aguardar **cadastro revendas** (CNPJ).

## Amostra sem match (nome+UF)

- `TOBRAS DISTRIBUIDORA DE COMBUSTIVEIS LTDA|MG`
- `RUFF CJ DISTRIBUIDORA DE PETROLEO LTDA|MS`
- `SETTA COMBUSTIVEIS LTDA|MG`
- `INTEGRACAO COMBUSTIVEIS LTDA|MA`
- `FAN DISTRIBUIDORA DE PETROLEO LTDA|CE`
- `DISTRIBUIDORA DE COMBUSTIVEL TORRAO LTDA|PE`
- `DISLUB COMBUSTIVEIS S A|PB`
- `TOWER BRASIL PETROLEO LTDA|MT`
