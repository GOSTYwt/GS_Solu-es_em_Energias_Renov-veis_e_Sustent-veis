"""SERS - Neighborhood Action Dashboard | Praça Solar Inteligente
Calcula consumo, comparação de alternativas e indicadores.
Uso: python src/calculos.py   (gera data/*.csv, data/resultados.json e dashboard/data.js)
Fórmula base: E (kWh) = P (W) x t (h) / 1000
"""
import csv, json, math, pathlib

RAIZ = pathlib.Path(__file__).resolve().parent.parent
P = {r["parametro"]: float(r["valor"]) for r in csv.DictReader(open(RAIZ / "data/premissas.csv", encoding="utf-8"))}
HSP_MES = list(csv.DictReader(open(RAIZ / "data/hsp_mensal.csv", encoding="utf-8")))

N, H, D = int(P["n_postes"]), P["horas_noite"], P["dias_mes"]
TARIFA, FE, FE_ALTO, ANOS = P["tarifa"], P["fator_emissao"], P["fator_emissao_cenario_alto"], int(P["horizonte"])


def kwh_dia(potencia_w, horas, qtd=N):
    return qtd * potencia_w * horas / 1000  # E = P x t / 1000


# --- Consumo por alternativa (kWh/dia) -------------------------------------
h_pleno = P["dimer_horas_pleno"]
h_red = H - h_pleno
dia = {
    "A0": kwh_dia(P["potencia_sodio_total"], H),
    "A1": kwh_dia(P["potencia_led"], H),
    "A2": kwh_dia(P["potencia_led"], h_pleno) + kwh_dia(P["potencia_led"] * P["dimer_nivel_reduzido"], h_red),
}
dia["A3"] = dia["A2"]  # mesma demanda de A2; parte/tudo compensado pela geração FV
dia["A4"] = 0.0        # luminárias autônomas: nenhuma energia da rede

# --- Dimensionamento FV (A3) ------------------------------------------------
kwp_min = dia["A2"] / (P["hsp"] * P["performance_ratio"])
n_modulos = math.ceil(kwp_min * 1000 / P["modulo_fv"])
kwp = n_modulos * P["modulo_fv"] / 1000
ger_mes = kwp * P["hsp"] * P["performance_ratio"] * D

# --- Capex e Opex ------------------------------------------------------------
inst = 1 + P["instalacao_pct"]
capex_fv = kwp * 1000 * P["custo_fv"]
capex = {
    "A0": 0.0,
    "A1": N * P["custo_luminaria_led"] * inst,
    "A2": (N * (P["custo_luminaria_led_dimer"] + P["custo_sensor_presenca"]) + P["custo_gateway_medidor"]) * inst,
}
capex["A3"] = capex["A2"] + capex_fv
capex["A4"] = N * P["custo_luminaria_solar"] * inst + P["custo_gateway_medidor"] * inst
opex_ano = {
    "A0": N * P["opex_sodio"], "A1": N * P["opex_led"], "A2": N * P["opex_led"],
    "A3": N * P["opex_led"] + P["opex_fv_pct"] * capex_fv, "A4": N * P["opex_solar_autonoma"],
}
nomes = {
    "A0": "Convencional (VSAP 150 W) - linha de base",
    "A1": "LED 60 W (retrofit simples)",
    "A2": "LED + dimerização por sensores + monitoramento",
    "A3": "LED + dimerização + microgeração FV (recomendada)",
    "A4": "Luminárias solares autônomas (off-grid)",
}
renovavel = {"A0": 0, "A1": 0, "A2": 0, "A3": 1, "A4": 1}

res = {}
for k in nomes:
    cons_mes = dia[k] * D
    if k == "A3":
        liquido = max(0.0, cons_mes - ger_mes)         # kWh/mês faturados após compensação
        part_ren = min(1.0, ger_mes / cons_mes)
    elif k == "A4":
        liquido, part_ren = 0.0, 1.0
    else:
        liquido, part_ren = cons_mes, 0.0
    base_mes = dia["A0"] * D
    eco_kwh = base_mes - liquido                        # economia de energia da rede vs. A0
    custo_en_mes = liquido * TARIFA
    custo_ano = custo_en_mes * 12 + opex_ano[k]
    base_custo_ano = base_mes * TARIFA * 12 + opex_ano["A0"]
    eco_rs_ano = base_custo_ano - custo_ano
    res[k] = dict(
        nome=nomes[k], renovavel=bool(renovavel[k]),
        demanda_iluminacao_kwh_mes=round(cons_mes, 1),
        energia_da_rede_kwh_mes=round(liquido, 1),
        economia_kwh_mes=round(eco_kwh, 1),
        economia_pct=round(100 * eco_kwh / base_mes, 1),
        participacao_renovavel_pct=round(100 * part_ren, 1),
        capex_rs=round(capex[k]), opex_rs_ano=round(opex_ano[k]),
        custo_energia_rs_mes=round(custo_en_mes, 2),
        economia_rs_mes=round(eco_rs_ano / 12, 2),
        emissoes_kg_ano=round(liquido * 12 * FE, 1),
        emissoes_evitadas_kg_ano=round(eco_kwh * 12 * FE, 1),
        emissoes_evitadas_cenario_alto_kg_ano=round(eco_kwh * 12 * FE_ALTO, 1),
        custo_total_10a_rs=round(capex[k] + custo_ano * ANOS),
        payback_anos=(round(capex[k] / eco_rs_ano, 1) if eco_rs_ano > 0 and k != "A0" else None),
    )

# --- Série mensal simulada (A3): geração FV x demanda ------------------------
serie = []
for m in HSP_MES:
    d, hsp = int(m["dias"]), float(m["hsp_kwh_m2_dia"])
    ger = kwp * hsp * P["performance_ratio"] * d
    dem = dia["A2"] * d
    serie.append(dict(mes=m["mes"], demanda_kwh=round(dem, 1), geracao_fv_kwh=round(ger, 1),
                      saldo_creditos_kwh=round(ger - dem, 1), baseline_kwh=round(dia["A0"] * d, 1),
                      participacao_renovavel_pct=round(100 * min(1, ger / dem), 1)))

saida = dict(
    projeto="Praça Solar Inteligente", referencia="mês médio = 365/12 dias; horizonte 10 anos",
    dimensionamento_fv=dict(kwp_minimo=round(kwp_min, 2), modulos=n_modulos, kwp_instalado=round(kwp, 2),
                            geracao_kwh_mes=round(ger_mes, 1), capex_fv_rs=round(capex_fv)),
    alternativas=res, serie_mensal_A3=serie,
    premissas={k: v for k, v in P.items()},
    aviso="Projeções condicionadas às premissas; não são resultados garantidos.",
)
(RAIZ / "data/resultados.json").write_text(json.dumps(saida, ensure_ascii=False, indent=2), encoding="utf-8")
(RAIZ / "dashboard/data.js").write_text("window.SERS_DATA = " + json.dumps(saida, ensure_ascii=False) + ";", encoding="utf-8")

cols = list(next(iter(res.values())).keys())
with open(RAIZ / "data/comparacao_alternativas.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f); w.writerow(["id"] + cols)
    for k, v in res.items(): w.writerow([k] + [v[c] for c in cols])
with open(RAIZ / "data/indicadores_mensais.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(serie[0].keys())); w.writeheader(); w.writerows(serie)

if __name__ == "__main__":
    print(f"FV: min {kwp_min:.2f} kWp -> {n_modulos} módulos = {kwp:.2f} kWp; geração {ger_mes:.1f} kWh/mês")
    for k, v in res.items():
        print(k, {c: v[c] for c in cols if c != "nome"})
