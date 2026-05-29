import streamlit as st
import requests
import pandas as pd
import os
# ===================================
# CONFIGURAÇÃO
# ===================================
st.set_page_config(
    page_title="IA Trader Esportivo",
    layout="wide"
)
st.title("⚽ IA Trader Esportivo Profissional")
# ===================================
# API FOOTBALL
# ===================================
API_KEY = "0354050b6f24a03a655e05cl268ef291"
HEADERS = {
    "x-apisports-key": API_KEY
}
BASE_URL = "https://v3.football.api-sports.io"
# ===================================
# BUSCAR JOGOS AO VIVO
# ===================================
st.subheader("📡 Jogos Ao Vivo")
jogos_lista = []
jogos_dict = {}
try:
    url = f"{BASE_URL}/fixtures?live=all"
    response = requests.get(
        url,
        headers=HEADERS,
        timeout=15
    )
    if response.status_code == 200:
        data = response.json()
        jogos = data.get("response", [])
        if len(jogos) > 0:
            for jogo in jogos:
                casa = jogo["teams"]["home"]["name"]
                fora = jogo["teams"]["away"]["name"]
                minuto = jogo["fixture"]["status"]["elapsed"]
                fixture_id = jogo["fixture"]["id"]
                texto = f"{casa} x {fora} ({minuto}')"
                jogos_lista.append(texto)
                jogos_dict[texto] = fixture_id
        else:
            st.warning("Nenhum jogo ao vivo encontrado.")
    else:
        st.error(
            f"Erro API: {response.status_code}"
        )
except Exception as e:
    st.error(
        f"Erro de conexão: {e}"
    )
# ===================================
# SELECT GAME
# ===================================
fixture_id = None
if len(jogos_lista) > 0:
    jogo_selecionado = st.selectbox(
        "Selecione o jogo",
        jogos_lista
    )
    fixture_id = jogos_dict[jogo_selecionado]
# ===================================
# ODDS
# ===================================
st.subheader("💰 Mercado Odds")
col1, col2, col3 = st.columns(3)
with col1:
    odd_casa = st.number_input(
        "Odd Casa",
        min_value=1.01,
        value=1.80
    )
with col2:
    odd_empate = st.number_input(
        "Odd Empate",
        min_value=1.01,
        value=3.40
    )
with col3:
    odd_fora = st.number_input(
        "Odd Fora",
        min_value=1.01,
        value=4.50
    )
# ===================================
# PROBABILIDADE
# ===================================
prob_casa = (1 / odd_casa) * 100
prob_empate = (1 / odd_empate) * 100
prob_fora = (1 / odd_fora) * 100
st.subheader("📊 Probabilidades")
st.write(f"Casa: {prob_casa:.2f}%")
st.write(f"Empate: {prob_empate:.2f}%")
st.write(f"Fora: {prob_fora:.2f}%")
if prob_casa > 60:
    st.success("🔥 Forte favoritismo do mandante")
elif prob_fora > 60:
    st.success("🔥 Forte favoritismo visitante")
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
escanteios = st.slider(
    "Escanteios",
    0,
    20,
    7
)
# ===================================
# IA SCORE
# ===================================
indice = (
    ataques * 0.5 +
    posse * 0.2 +
    chutes * 2 +
    escanteios * 1.5
)
st.subheader("📈 Índice IA")
st.metric(
    "Pressão Ofensiva",
    f"{indice:.1f}"
)
# ===================================
# ALERTAS
# ===================================
if indice > 80:
    st.success("🚨 ALERTA FORTE DE GOL")
elif indice > 60:
    st.warning("⚠️ Pressão ofensiva moderada")
else:
    st.error("❄️ Jogo morno")
# ===================================
# PREVISÃO IA
# ===================================
st.subheader("🧠 Previsão IA")
if indice > 80 and prob_casa > 55:
    st.success("""
✅ ENTRADAS SUGERIDAS
• Próximo Gol Casa
• Over 1.5
• Over 2.5
• Over Escanteios
🔥 Confiança IA: 9.2/10
""")
elif indice > 60:
    st.warning("""
⚠️ Mercado observável
Possível entrada futura.
""")
else:
    st.error("""
❌ Sem valor no momento.
""")
# ===================================
# ESTATÍSTICAS
# ===================================
st.subheader("📋 Estatísticas")
dados = {
    "Indicador": [
        "Ataques",
        "Posse",
        "Chutes",
        "Escanteios"
    ],
    "Valor": [
        ataques,
        posse,
        chutes,
        escanteios
    ]
}
df = pd.DataFrame(dados)
st.dataframe(
    df,
    use_container_width=True
)
# ===================================
# RODAPÉ
# ===================================
st.markdown("---")
st.caption(
    "IA Trader Esportivo • Live Analytics"
)
