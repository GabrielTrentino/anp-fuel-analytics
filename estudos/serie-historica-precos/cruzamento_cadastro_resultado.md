# Cruzamento precos LPC x cadastro revendas (CNPJ)

Precos: `lpc_posto.parquet` · Cadastro: `revendas.parquet`

| Metrica | Valor |
|---------|------:|
| CNPJs distintos precos | 15,832 |
| CNPJs cadastro revendas | 46,095 |
| **Intersecao CNPJ** | **11,472** (72.5% precos · 24.9% cadastro) |
| Linhas precos com CNPJ no cadastro | 1,143,006 / 1,244,835 |

Join recomendado: `precos.cnpj = revendas.cnpj` para enriquecer preco com bandeira/endereco cadastral.
