# Cruzamento PML

Base: `pml.parquet` — **13.726** amostras de lubrificantes, 2016–2026.

## Perfil

- Detentores (fabricantes): 158 distintos
- Marcas comerciais: 1.579
- Grau SAE: 38 tipos (15W40, 5W30 mais comuns)
- Nível desempenho API: 22 tipos (SL, CI-4, SN, etc.)
- UFs amostradas: 21
- Anos: 2016–2026

## Resultados

- Resultado Final: maioria "Conforme"; 4 categorias
- Resultado Qualidade: 6 categorias
- Resultado Registro: 4 categorias

## Cruzamentos possíveis

| Dataset parceiro | Chave | Observação |
|------------------|-------|------------|
| `registro-lubrificantes` | `registro` / `cnpj_detentor` | Validar produto registrado vs monitorado |
| `movimentacao-derivados` | limitado | PML é sobre qualidade, não volume |
| `distribuidores-combustiveis-liquidos` | `cnpj_detentor` | Detentores que também são distribuidores |

> PML é primariamente um dataset de qualidade analítica (como PMQC para combustíveis).
> Join direto com combustíveis é limitado — relevância indireta via detentores.
