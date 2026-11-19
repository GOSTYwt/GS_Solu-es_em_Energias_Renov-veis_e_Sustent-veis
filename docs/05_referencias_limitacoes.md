# 5. Referências, fontes e limitações

## Fontes
1. MCTI - SIRENE, *Fatores de emissão de CO₂ do SIN* (médias mensais jan-abr/2025: 23,7; 24,8; 21,5; 28,9 kg/MWh), conforme divulgado em https://canalsolar.com.br/emissoes-de-co₂-geracao-eletrica-mcti/ e nota técnica do MCTI (jun/2025). Dados oficiais: https://www.gov.br/mcti/pt-br/acompanhe-o-mcti/sirene/dados-e-ferramentas/fatores-de-emissao
2. TRT-15, *Plano de Descarbonização 2025* (fator SIN média anual 2021 = 0,1264 tCO₂e/MWh, usado como cenário de sensibilidade).
3. CRESESB/CEPEL - *SunData* e *Atlas Brasileiro de Energia Solar* (INPE) - irradiação solar (HSP) do estado de SP; **valores mensais aproximados, devem ser conferidos para a coordenada exata**.
4. ANEEL - tarifas de distribuidoras e Resolução Normativa 1.000/2021; Lei 14.300/2022 (microgeração distribuída e SCEE).
5. ABNT NBR 5101 - Iluminação pública (requisitos de iluminância).
6. Potências, vidas úteis e custos de equipamentos: **premissas** baseadas em faixas típicas de mercado brasileiro; devem ser substituídas por cotações.

## Limitações
- Estudo **simulado**: não há medição real; todos os dados de equipamentos e custos são premissas em `data/premissas.csv`.
- Tarifa, custo do Wp e HSP variam por distribuidora, município e ano; **atualizar antes de qualquer decisão**.
- Equivalência de iluminância entre VSAP 150 W e LED 60 W (e a redução a 40%) precisa de **projeto luminotécnico** (NBR 5101).
- Custo total sem reajuste de tarifa, inflação, financiamento ou valor do dinheiro no tempo.
- A compensação de créditos (SCEE) depende de regras da distribuidora (incl. cobrança do fio B) e de enquadramento da unidade consumidora; o resultado de "0 kWh líquido" é uma média anual.
- Emissões evitadas são baixas em kg porque o SIN brasileiro já tem fator de emissão baixo.
- Não inclui impacto de fabricação/descarte de módulos, baterias e luminárias.
- Estimativas de economia e de geração são **projeções condicionadas às premissas**, não resultados garantidos.
