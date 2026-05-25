# Cruzamento precos LPC x cadastro revendas (CNPJ)

Precos: `qus_gasolina_etanol.parquet` · Cadastro: `revendas.parquet`

| Metrica | Valor |
|---------|------:|
| CNPJs distintos precos (amostra qus) | 6,147 |
| CNPJs cadastro revendas | 46,095 |
| **Intersecao CNPJ** | **6,008** (97.7% precos · 13.0% cadastro) |
| Linhas precos com CNPJ no cadastro | 44,596 / 45,211 |

Join recomendado: `precos.cnpj = revendas.cnpj` para enriquecer preco com bandeira/endereco cadastral.
