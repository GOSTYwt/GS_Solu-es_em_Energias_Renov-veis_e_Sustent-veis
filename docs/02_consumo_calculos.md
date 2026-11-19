# 2. Análise de consumo energético e cálculos

**Expressão base:** `E (kWh) = P (W) × t (h) / 1000`
**Período de referência:** mês médio = 365/12 = **30,4167 dias**. Todas as alternativas atendem à **mesma necessidade**: iluminar 20 postes por 12 h/noite. Premissas completas e fontes em [`../data/premissas.csv`](../data/premissas.csv); código em [`../src/calculos.py`](../src/calculos.py).

## Linha de base (A0) - vapor de sódio
- P por poste = 150 W (lâmpada) + ~13% (reator) ≈ **170 W**
- E_dia = 20 × 170 W × 12 h / 1000 = **40,8 kWh/dia**
- E_mês = 40,8 × 30,4167 = **1.241,0 kWh/mês** (≈ 14.892 kWh/ano)
- Custo de energia = 1.241,0 × R$ 0,85 = **R$ 1.054,85/mês**

## LED simples (A1)
- E_dia = 20 × 60 W × 12 h / 1000 = 14,4 kWh/dia → **438,0 kWh/mês**

## LED + dimerização por sensores (A2)
- Pleno (4 h): 20 × 60 W × 4 h / 1000 = 4,80 kWh
- Reduzido (8 h a 40% = 24 W): 20 × 24 W × 8 h / 1000 = 3,84 kWh
- E_dia = **8,64 kWh/dia** → **262,8 kWh/mês**

## Dimensionamento FV (A3)
- kWp mínimo = E_dia / (HSP × PR) = 8,64 / (4,5 × 0,78) = **2,46 kWp**
- Módulos de 650 Wp: ⌈2,46 / 0,65⌉ = **4 módulos = 2,60 kWp**
- Geração = 2,60 × 4,5 × 0,78 × 30,4167 ≈ **277,6 kWh/mês** (≈ 106% da demanda de A2, em média anual)
- Em meses de baixa irradiação (jun-jul) a geração fica ~20% abaixo da demanda; o déficit é coberto por **créditos** de meses excedentes (ver `data/indicadores_mensais.csv`).

## Emissões
`kg CO₂e = kWh × fator de emissão`. Fator adotado: **0,0247 kg CO₂e/kWh** (média jan-abr/2025 do SIN, MCTI/SIRENE). Como a matriz elétrica brasileira já é muito renovável, **as emissões evitadas em kg são pequenas**; por isso é apresentado também um cenário de sensibilidade com 0,1264 kg/kWh (SIN médio de 2021). O ganho principal do projeto é **econômico e de gestão**, e o ambiental é complementar.

> Todos os valores são **projeções condicionadas às premissas**, não resultados garantidos.
