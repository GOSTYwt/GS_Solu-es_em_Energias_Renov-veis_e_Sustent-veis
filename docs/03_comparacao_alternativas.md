# 3. Comparação das alternativas (mesma necessidade, horizonte de 10 anos)

Dados em [`../data/comparacao_alternativas.csv`](../data/comparacao_alternativas.csv). Custo total em 10 anos = capex + 10 × (energia + operação), **sem** reajuste tarifário, financiamento ou desconto (simplificação declarada).

| Alt. | Descrição | Rede (kWh/mês) | Economia | Renovável | Capex (R$) | Custo 10 anos (R$) | Payback | Emissões evitadas (kg CO₂e/ano) |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| A0 | Convencional VSAP (base) | 1.241,0 | - | 0% | 0 | 131.582 | - | - |
| A1 | LED 60 W | 438,0 | 64,7% | 0% | 9.900 | 55.576 | 1,2 anos | 238,0 |
| A2 | LED + dimerização + monitoramento | 262,8 | 78,8% | 0% | 16.720 | 44.526 | 1,6 anos | 289,9 |
| **A3** | **A2 + FV on-grid 2,6 kWp** | **0 (líquido, após compensação)** | **100%** | **100%** | **28.420** | **30.590** | **2,2 anos** | **367,8** |
| A4 | Luminárias solares autônomas | 0 | 100% | 100% | 78.980 | 104.980 | 7,5 anos | 367,8 |

## Análise qualitativa
| Alt. | Viabilidade técnica | Impacto ambiental | Benefícios | Limitações |
|---|---|---|---|---|
| A0 | Já instalada | Maior consumo; reatores e lâmpadas com Hg/Na descartados | Nenhum além do status quo | Maior custo, sem dados de consumo |
| A1 | Troca simples (retrofit) | Menor consumo, vida longa (~50.000 h) | Retorno rápido, baixa complexidade | Sem adaptação à presença, sem monitoramento |
| A2 | Requer sensores, driver dimerizável e conectividade | Maior economia sem geração | Gera os dados do dashboard | Depende de conectividade e de manutenção dos sensores |
| A3 | Requer área de telhado/estrutura próxima e aprovação da distribuidora (SCEE) | Energia solar sem emissões na operação; descarte de módulos no fim da vida | Menor custo total; participação renovável de 100% (anual) | Compensação sujeita a regras tarifárias (fio B); investimento inicial maior |
| A4 | Cada poste precisa de sol sem sombra; baterias | Baterias (reciclagem necessária) | Independe da rede, útil onde não há rede | Capex ~2,8× o de A3; troca de baterias; autonomia em dias nublados |

## Recomendação
**A3** tem o menor custo total em 10 anos e atende ao requisito de fonte renovável, além de ser a única que combina **eficiência (A2) + geração renovável**. A4 só se justificaria em praças **sem acesso à rede**.

### Sensibilidade (a testar editando `data/premissas.csv` e rodando `python src/calculos.py`)
Tarifa, custo do Wp e horas de iluminação alteram o payback, mas a **ordem de A0 > A1 > A2 > A3 em custo total** é robusta, pois depende mais da redução de consumo. O resultado de A4 é sensível ao custo da luminária solar e das baterias.
