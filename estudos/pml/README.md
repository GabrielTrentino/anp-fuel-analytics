# Estudo: PML — Programa de Monitoramento dos Lubrificantes

**Slug:** `pml`  
**Status:** pipeline operacional (trusted completo).

**Referência:** [anp-data-atlas — pml.md](https://github.com/GabrielTrentino/anp-data-atlas/blob/main/docs/conjuntos/pml.md)

## Dados

| Métrica | Valor |
|---------|-------|
| Amostras | 13.726 |
| Período | 2016–2026 |
| Detentores (fabricantes) | 158 |
| Marcas comerciais | 1.579 |
| UFs amostradas | 21 |
| Graus SAE | 38 |

## Pipeline

```
raw (download CSV único)
  -> trusted.sql -> pml.parquet (13.726 linhas)
```

## Cruzamentos

| Dataset parceiro | Chave | Observação |
|------------------|-------|------------|
| `registro-lubrificantes` | `registro` / `cnpj_detentor` | Produto registrado vs monitorado |
| `distribuidores-combustiveis-liquidos` | `cnpj_detentor` | Detentores = distribuidores? |

## Relevância

Monitoramento de qualidade de lubrificantes; complementar ao segmento de combustíveis via detentores.
