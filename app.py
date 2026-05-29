import streamlit as st
import requests
import pandas as pd
import time
from datetime import datetime


# =====================================================
# CONFIG APP
# =====================================================

st.set_page_config(
    page_title="Esportivo PRO IA",
    layout="wide"
)

# =====================================================
# AUTO REFRESH
# =====================================================

(interval=30000, key="0354050b6f24a03a655e05cl268ef291")

# =====================================================
# API CONFIG
# =====================================================

API_KEY = "0354050b6f24a03a655e05cl268ef291"

HEADERS = {
    "x-apisports-key": API_KEY
}

# =====================================================
# FUNÇÕES API
# =====================================================

def buscar_jogos_ao_vivo():

    url = "https://v3.football.api-sports.io/fixtures?live=all"

    response = requests.get(url, headers=HEADERS)

    if response.status_code == 200:
        return response.json()["response"]

    return []

# =====================================================
# BUSCAR ESTATÍSTICAS
# =====================================================

def buscar_estatisticas(fixture_id):

    url = f"https://v3.football.api-sports.io/fixtures/statistics?fixture={fixture_id}"

    response = requests.get(url, headers=HEADERS)

    if response.status_code == 200:
        return response.json()["response"]

    return []

# =====================================================
# EXTRAIR ESTATÍSTICAS
# =====================================================

def extrair_valor(stats, tipo):

    for item in stats:

        if item["type"] == tipo:

            valor = item["value"]

            if valor is None:
                return 0

            if isinstance(valor, str):

                valor = valor.replace("%", "")

                try:
                    return float(valor)
                except:
                    return 0

            return valor

    return 0

# =====================================================
# MOTOR IA
# =====================================================

def calcular_pressao(
    posse,
    ataques,
    finalizacoes,
    finalizacoes_gol,
    escanteios
):

    score = (
        posse * 0.15 +
        ataques * 0.30 +
        finalizacoes * 4 +
        finalizacoes_gol * 6 +
        escanteios * 2
    )

    return round(score, 2)

# =====================================================
# PROBABILIDADE GOL
# =====================================================

def probabilidade_gol(score):

    if score >= 90:
        return "🔥 EXTREMAMENTE FORTE"

    elif score >= 70:
        return "🔥 FORTE CHANCE DE GOL"

    elif score >= 50:
        return "⚠️ PRESSÃO MODERADA"

    else:
        return "❄️ BAIXA PRESSÃO"

# =====================================================
# TÍTULO
# =====================================================

st.title("⚽ Esportivo PRO IA")

st.markdown("---")

# =====================================================
# BUSCAR JOGOS
# =====================================================

jogos = buscar_jogos_ao_vivo()

# =====================================================
# SEM JOGOS
# =====================================================

if len(jogos) == 0:

    st.warning("Nenhum jogo ao vivo encontrado.")

# =====================================================
# LOOP JOGOS
# =====================================================

for jogo in jogos:

    fixture_id = jogo["fixture"]["id"]

    minuto = jogo["fixture"]["status"]["elapsed"]

    liga = jogo["league"]["name"]

    time_casa = jogo["teams"]["home"]["name"]

    time_fora = jogo["teams"]["away"]["name"]

    gols_casa = jogo["goals"]["home"]

    gols_fora = jogo["goals"]["away"]

    # =================================================
    # HEADER JOGO
    # =================================================

    st.markdown("---")

    st.subheader(
        f"⚽ {time_casa} {gols_casa} x {gols_fora} {time_fora}"
    )

    st.write(f"🏆 Liga: {liga}")

    st.write(f"⏱️ Minuto: {minuto}")

    # =================================================
    # ESTATÍSTICAS
    # =================================================

    estatisticas = buscar_estatisticas(fixture_id)

    if len(estatisticas) < 2:

        st.warning("Sem estatísticas disponíveis.")

        continue

    home_stats = estatisticas[0]["statistics"]

    away_stats = estatisticas[1]["statistics"]

    # =================================================
    # CASA
    # =================================================

    posse_casa = extrair_valor(home_stats, "Ball Possession")

    ataques_casa = extrair_valor(home_stats, "Dangerous Attacks")

    finalizacoes_casa = extrair_valor(home_stats, "Total Shots")

    finalizacoes_gol_casa = extrair_valor(home_stats, "Shots on Goal")

    escanteios_casa = extrair_valor(home_stats, "Corner Kicks")

    # =================================================
    # FORA
    # =================================================

    posse_fora = extrair_valor(away_stats, "Ball Possession")

    ataques_fora = extrair_valor(away_stats, "Dangerous Attacks")

    finalizacoes_fora = extrair_valor(away_stats, "Total Shots")

    finalizacoes_gol_fora = extrair_valor(away_stats, "Shots on Goal")

    escanteios_fora = extrair_valor(away_stats, "Corner Kicks")

    # =================================================
    # IA SCORE
    # =================================================

    score_casa = calcular_pressao(
        posse_casa,
        ataques_casa,
        finalizacoes_casa,
        finalizacoes_gol_casa,
        escanteios_casa
    )

    score_fora = calcular_pressao(
        posse_fora,
        ataques_fora,
        finalizacoes_fora,
        finalizacoes_gol_fora,
        escanteios_fora
    )

    # =================================================
    # COLUNAS
    # =================================================

    col1, col2 = st.columns(2)

    # =================================================
    # CASA
    # =================================================

    with col1:

        st.markdown(f"## 🏠 {time_casa}")

        st.metric("Posse", f"{posse_casa}%")

        st.metric("Ataques", ataques_casa)

        st.metric("Finalizações", finalizacoes_casa)

        st.metric("Finalizações no Gol", finalizacoes_gol_casa)

        st.metric("Escanteios", escanteios_casa)

        st.metric("Score IA", score_casa)

    # =================================================
    # FORA
    # =================================================

    with col2:

        st.markdown(f"## ✈️ {time_fora}")

        st.metric("Posse", f"{posse_fora}%")

        st.metric("Ataques", ataques_fora)

        st.metric("Finalizações", finalizacoes_fora)

        st.metric("Finalizações no Gol", finalizacoes_gol_fora)

        st.metric("Escanteios", escanteios_fora)

        st.metric("Score IA", score_fora)

    # =================================================
    # IA RESULTADO
    # =================================================

    st.markdown("---")

    st.subheader("📈 Resultado IA")

    alerta_casa = probabilidade_gol(score_casa)

    alerta_fora = probabilidade_gol(score_fora)

    # =================================================
    # ANÁLISE CASA
    # =================================================

    if score_casa > score_fora:

        st.success(f"""
🔥 FORTE TENDÊNCIA CASA

✅ Próximo Gol Casa

✅ Pressão Ofensiva Maior

✅ Over 1.5 Forte

✅ Over Escanteios

📊 Score Casa: {score_casa}

📊 Score Fora: {score_fora}

🚨 ALERTA: {alerta_casa}
        """)

    # =================================================
    # ANÁLISE FORA
    # =================================================

    elif score_fora > score_casa:

        st.error(f"""
🔥 FORTE TENDÊNCIA FORA

✅ Próximo Gol Fora

✅ Pressão Ofensiva Visitante

✅ Over 1.5 Forte

✅ Ambas Marcam Possível

📊 Score Casa: {score_casa}

📊 Score Fora: {score_fora}

🚨 ALERTA: {alerta_fora}
        """)

    # =================================================
    # EQUILIBRADO
    # =================================================

    else:

        st.warning("""
⚖️ Jogo equilibrado

✅ Mercado Ambas Marcam

✅ Over Escanteios

⚠️ Sem tendência clara
        """)

# =====================================================
# FOOTER
# =====================================================

st.markdown("---")

st.caption("IA Trader Esportivo PRO • Live Analytics")
