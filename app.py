import streamlit as st
import requests
import pandas as pd
import os

# ===================================
# CONFIG
# ===================================

API_KEY = "0354050b6f24a03a655e05cl268ef291"

headers = {
    "x-apisports-key": API_KEY
}

st.set_page_config(
    page_title="IA Trader Esportivo",
    layout="wide"
)

st.title("⚽ IA Trader Esportivo Profissional")

# ===================================
# BUSCAR JOGOS AO VIVO
# ===================================

url = "https://v3.football.api-sports.io/fixtures?live=all"

try:

    response = requests.get(url, headers=headers)

    jogos_lista = []

    if response.status_code == 200:

        data = response.json()

        jogos = data.get("response", [])

        for jogo in jogos:

            casa = jogo["teams"]["home"]["name"]
            fora = jogo["teams"]["away"]["name"]

            minuto = jogo["fixture"]["status"]["elapsed"]

            fixture_id = jogo["fixture"]["id"]

            texto = f"{casa} x {fora} ({minuto}')"

            jogos_lista.append(texto)

    else:

        st.error(f"Erro API: {response.status_code}")

        jogos_lista = []

except Exception as e:

    st.error(f"Erro conexão: {e}")

    jogos_lista = []

# ===================================
# SELECT GAME
# ===================================

if len(jogos_lista) > 0:

    jogo_selecionado = st.selectbox(
        "Selecione o jogo",
        jogos_lista
    )

else:

    st.warning("Nenhum jogo ao vivo encontrado")

# ===================================
# IA PRÉ-JOGO
# ===================================

st.subheader("🤖 Análise IA")

odd_casa = st.number_input(
    "Odd Casa",
    value=1.80
)

odd_empate = st.number_input(
    "Odd Empate",
    value=3.40
)

odd_fora = st.number_input(
    "Odd Fora",
    value=4.50
)

prob_casa = (1 / odd_casa) * 100

st.write(
    f"📊 Probabilidade Casa: {prob_casa:.2f}%"
)

if prob_casa > 60:

    st.success("🔥 Forte favoritismo")

else:

    st.warning("⚠️ Jogo equilibrado")

# ===================================
# IA AO VIVO
# ===================================

st.subheader("🔥 IA AO VIVO")

ataques = st.slider(
    "Ataques Perigosos",
    0,
    100,
    60
)

posse = st.slider(
    "Posse de Bola",
    0,
    100,
    55
)

chutes = st.slider(
    "Chutes no Gol",
    0,
    20,
    6
)

indice = (
    ataques * 0.5 +
    posse * 0.2 +
    chutes * 2
)

st.write(
    f"📈 Pressão Ofensiva: {indice:.1f}"
)

if indice > 65:

    st.success("🚨 ALERTA DE GOL")

elif indice > 45:

    st.warning("⚠️ Pressão moderada")

else:

    st.error("❄️ Jogo morno")

# ===================================
# PREVISÃO IA
# ===================================

st.subheader("🧠 Previsão IA")

if indice > 65 and prob_casa > 55:

    st.success("""
✅ Entrada sugerida:

• Próximo Gol Casa
• Over 1.5
• Over Escanteios

🔥 Confiança IA: 8.8/10
""")

elif indice > 45:

    st.warning("""
⚠️ Mercado observável

Possível entrada futura.
""")

else:

    st.error("""
❌ Sem valor no momento.
""")
