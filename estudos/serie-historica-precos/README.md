# Estudo: Série Histórica de Preços de Combustíveis

**Slug:** `serie-historica-precos`  
**Referência:** [anp-data-atlas — serie-historica-precos.md](https://github.com/GabrielTrentino/anp-data-atlas/blob/main/docs/conjuntos/serie-historica-precos.md)

## Papel deste estudo

Série **LPC** (Levantamento de Preços de Combustíveis) em nível de **posto** (`CNPJ da Revenda`), para cruzar com [cadastro revendas](../cadastro-revendas-combustiveis/) e análises territoriais.

## Pipeline

```bash
py pipelines/run.py serie-historica-precos
py pipelines/run.py serie-historica-precos trusted_qus_gasolina
```

| Etapa | Saída |
|-------|-------|
| `raw` | `data/raw/serie-historica-precos/` (MVP: qus + amostras dsan/dsas) |
| `trusted_qus_gasolina` | `qus_gasolina_etanol.parquet` |

Perfil brutos:

```bash
py estudos/serie-historica-precos/scripts/perfil_raw_mvp.py
```

## Schema (posto — confirmado)

Separador **`;`** · UTF-8 · colunas principais:

`Regiao`, `Estado`, `Municipio`, `Revenda`, **`CNPJ da Revenda`**, `Produto`, `Data da Coleta`, `Valor de Venda`, `Valor de Compra`, `Bandeira`

## Cruzamento cadastro

```bash
py estudos/serie-historica-precos/scripts/cruzamento_cadastro_revendas.py
```

Resultado: [cruzamento_cadastro_resultado.md](cruzamento_cadastro_resultado.md)

## Status

| Item | Situação |
|------|----------|
| Download MVP | ◐ |
| Trusted qus gasolina/etanol | ✓ |
| Join CNPJ cadastro | ✓ |
| Histórico dsan/dsas completo | pendente |

Detalhe: **[TODO.md](TODO.md)**
