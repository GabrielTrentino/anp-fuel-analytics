# TODO — cadastro-revendas-combustiveis

**Legenda:** `—` pendente · `◐` em andamento · `✓` concluído

## Pipeline

| Item | Status |
|------|--------|
| Download raw (portal) | ✓ |
| `config/monorepo.yaml` | ✓ |
| Trusted `revendas.parquet` | ✓ |
| Refined / agregações | — |
| Notebook `01_perfil_exploratorio.ipynb` | — |

## Cruzamentos

| Alvo | Status | Nota |
|------|--------|------|
| Tancagem (CNPJ) | ✓ | **0%** — universos distintos (varejo vs instalações com tancagem >230 L) |
| Tancagem (CODIGOISIMP) | ✓ | 0% na amostra atual |
| Movimentação (agente → CNPJ) | ✓ | ~0,5% — agentes SIMP são distribuidores, não postos |
| Série histórica preços (CNPJ) | — | próximo conjunto prioritário |
| Pontos abastecimento | — | |

## Próximas análises

| Prioridade | Tema |
|:----------:|------|
| 1 | Mapa UF/município — densidade postos, bandeira branca vs marcas |
| 2 | Série entradas/saídas cadastro (`data_publicacao`, `data_vinculacao`) |
| 3 | Join preços LPC por CNPJ + geo |
| 4 | Pontos abastecimento × cadastro (endereço/CEP) |
| 5 | Cruzamento movimentação via **cadeia** distribuidor (não posto direto) |

Regenerar cruzamento:

```bash
py estudos/cadastro-revendas-combustiveis/scripts/cruzamento_tancagem_movimentacao.py
```
