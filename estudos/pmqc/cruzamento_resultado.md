# Cruzamento PMQC x cadastro-revendas e precos

Base: `pmqc.parquet` — **2,231,308** ensaios, 2024-01-02 – 2026-04-30.
Postos distintos (CNPJ): **26,466**

## Serie historica precos (LPC)

| Metrica | PMQC | Precos | Sobreposição |
|---------|------|--------|--------------|
| CNPJs distintos | 26,466 | 15,832 | **7,757** (29.3%) |

Join: `cnpj` + `data_coleta` (semana) — correlacionar qualidade e preço.

## Nao-conformidades

Total nao conforme: **234** (0.010%)

| Grupo produto | Nao conforme | % do grupo |
|---------------|-------------|------------|
| Gasolina | 0 | 0.000% |
| Óleo Diesel | 224 | 0.030% |
| Etanol | 10 | 0.002% |
