# Estudo: Distribuidores de Combustíveis Líquidos

**Slug:** `distribuidores-combustiveis-liquidos`  
**Status:** pipeline operacional (trusted AEA completo).

**Referência:** [anp-data-atlas — distribuidores-combustiveis-liquidos.md](https://github.com/GabrielTrentino/anp-data-atlas/blob/main/docs/conjuntos/distribuidores-combustiveis-liquidos.md)

## Dados

| Métrica | Valor |
|---------|-------|
| Distribuidores (AEA) | 713 |
| UFs | 25 |
| Autorizados ativos | 181 |
| Cancelados/Revogados | 516 |
| Contratos cessão (ce-cr) | 1.888 |
| Inutilizadores | 36 |

## Pipeline

```
raw (download: 3 CSVs + 3 PDFs metadados)
  -> prepare (parser report-style -> distribuidores_aea.csv)
    -> trusted.sql -> distribuidores.parquet (713 linhas)
```

## Situação das distribuidoras

| Status | Qtd |
|--------|----:|
| CANCELADA | 346 |
| AUTORIZADA | 181 |
| AUTORIZAÇÃO REVOGADA | 147 |
| Outros | 39 |

## Cruzamentos

| Dataset parceiro | Chave | Observação |
|------------------|-------|------------|
| `movimentacao-derivados` | `cnpj` | Movimentação por distribuidora |
| `serie-historica-precos` | distribuidora (nome) | Bandeiras nos postos |
| `cadastro-revendas-combustiveis` | distribuidora (nome) | Vinculação postos |

## Relevância

Atacado/distribuição — elos entre refinaria/terminal e varejo. Identifica quem opera e quem perdeu autorização.
