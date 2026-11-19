# Praça Solar Inteligente - Contribuição de SERS ao Neighborhood Action Dashboard (CitizenTech)

**Global Solution 2026.2 · Ciência da Computação · Soluções em Energias Renováveis e Sustentáveis (SERS)**

> **Contribuição de SERS:** todo o conteúdo deste repositório (pastas `docs/`, `data/`, `src/` e `dashboard/`) corresponde à disciplina SERS. Se o repositório for compartilhado com outras disciplinas, esta contribuição está identificada por este README.

## Integrantes
| Nome completo | RM |
|---|---|
| _preencher_ | _preencher_ |
| _preencher_ | _preencher_ |
| _preencher_ | _preencher_ |

## Problema
Uma praça comunitária com 20 postes de iluminação de vapor de sódio (150 W) acesos 12 h por noite, sempre na intensidade máxima e sem nenhum dado de consumo: **~1.241 kWh/mês e ~R$ 1.055/mês de energia**. Detalhes em [`docs/01_diagnostico.md`](docs/01_diagnostico.md).

## Solução
Comparação de 5 alternativas para a **mesma necessidade** (iluminar 20 postes por 12 h/noite, horizonte de 10 anos):

| Alt. | Descrição | Rede (kWh/mês) | Capex (R$) | Custo 10 anos (R$) | Renovável |
|---|---|---:|---:|---:|---|
| A0 | Convencional (base) | 1.241,0 | 0 | 131.582 | Não |
| A1 | LED 60 W | 438,0 | 9.900 | 55.576 | Não |
| A2 | LED + dimerização/sensores + monitoramento | 262,8 | 16.720 | 44.526 | Não |
| **A3** | **A2 + microgeração FV 2,6 kWp (recomendada)** | **0 líquido** | **28.420** | **30.590** | **Sim** |
| A4 | Luminárias solares autônomas | 0 | 78.980 | 104.980 | Sim |

A **A3** reduz o custo total em ~77% frente à base, com ~100% de participação renovável (média anual) e payback simples de ~2,2 anos, **sob as premissas adotadas**.

## Indicadores no dashboard
Consumo (kWh/mês), economia (kWh/mês e %), redução de custos (R$/mês), participação renovável (%), emissões evitadas (kg CO₂e/ano), tempo de funcionamento eficiente (h/dia) e payback. Definições e fórmulas em [`docs/04_diagrama_e_indicadores.md`](docs/04_diagrama_e_indicadores.md), que também contém o **diagrama de blocos** da solução.

## Como executar
Requer apenas **Python 3.8+** (sem dependências externas).
```bash
python src/calculos.py        # recalcula tudo a partir de data/premissas.csv
# abra dashboard/index.html no navegador (duplo clique)
```
Para testar outro cenário, altere `data/premissas.csv` e rode o script novamente.

## Estrutura do repositório
```
.
├── README.md
├── ENTREGA.txt                  # modelo do arquivo .txt de entrega
├── data/
│   ├── premissas.csv            # dados de entrada, unidades e fontes
│   ├── hsp_mensal.csv           # irradiação solar mensal (aproximada)
│   ├── comparacao_alternativas.csv
│   ├── indicadores_mensais.csv
│   └── resultados.json          # contrato de dados p/ o dashboard integrador
├── docs/
│   ├── 01_diagnostico.md
│   ├── 02_consumo_calculos.md
│   ├── 03_comparacao_alternativas.md
│   ├── 04_diagrama_e_indicadores.md
│   └── 05_referencias_limitacoes.md
├── src/calculos.py              # cálculos, comparação e geração de indicadores
└── dashboard/
    ├── index.html               # componente de dashboard SERS
    └── data.js                  # dados gerados por calculos.py
```

## Referências e limitações
Ver [`docs/05_referencias_limitacoes.md`](docs/05_referencias_limitacoes.md). Os valores são **projeções condicionadas às premissas**, não resultados garantidos; os dados de equipamentos e custos são estimativas e devem ser substituídos por cotações e medições reais.
