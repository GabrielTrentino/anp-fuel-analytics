# Cruzamento cadastro revendas x tancagem e movimentacao

Base: **46,095** postos (`revendas.parquet`), CNPJ e CODIGOISIMP unicos.

## Tancagem (por CNPJ)

| Metrica | Valor |
|---------|------:|
| CNPJs cadastro revendas | 46,095 |
| CNPJs distintos tancagem (snapshots) | 2,563 |
| **Intersecao CNPJ** | **0** (0.0% revendas) |

| CODIGOISIMP cadastro x CodInstalacao tancagem | 0 |

Tancagem agrega instalacoes com **tancagem autorizada** (bases TRR, terminais, refinarias).
Postos de rua no cadastro em geral **nao aparecem** na tancagem aberta — intersecao CNPJ nula e esperada.

## Movimentacao liquidos (agente -> CNPJ via cadastro)

| Metrica | Valor |
|---------|------:|
| Nomes agente unicos movimentacao | 214 |
| Nomes com match razao social no cadastro | **1** (0.5%) |

Agentes em movimentacao sao em geral **distribuidores** (SIMP); o cadastro lista **postos de varejo**.
Join direto agente -> posto e raro; o valor do cadastro e CNPJ para **precos LPC**, geo e fiscalizacao.
