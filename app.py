import streamlit as st
import requests

API_KEY = "27eb4c6573548e562e26d6f70052f8bd"

headers = {
    "x-apisports-key": API_KEY
}
st.title("Jogos de Hoje")

url = "https://v3.football.api-sports.io/fixtures?live=all"

response = requests.get(url, headers=headers)

if response.status_code == 200:
    data = response.json()

    jogos = data["response"]

    for jogo in jogos:
        casa = jogo["teams"]["home"]["name"]
        fora = jogo["teams"]["away"]["name"]
        tempo = jogo["fixture"]["status"]["elapsed"]

        st.write(f"⚽ {casa} x {fora}")
        st.write(f"⏱️ {tempo} minutos")
        st.divider()
# =========================
# IA PROFISSIONAL
# =========================

st.subheader("🤖 IA Profissional")

odd_casa = st.number_input("Odd Casa", value=1.80)
odd_empate = st.number_input("Odd Empate", value=3.20)
odd_fora = st.number_input("Odd Fora", value=4.50)

prob_real = (1 / odd_casa) * 100

st.write(f"📊 Probabilidade implícita Casa: {prob_real:.2f}%")

if prob_real < 60:
    st.success("🔥 Possível aposta de valor (EV+)")
else:
    st.warning("⚠️ Mercado já precificou forte favoritismo")

    # =========================
# NÍVEL 4 — IA LIVE
# =========================

st.subheader("🔥 IA AO VIVO")

ataques_perigosos = st.slider("Ataques perigosos", 0, 100, 65)
posse_bola = st.slider("Posse de bola (%)", 0, 100, 58)
chutes_gol = st.slider("Chutes no gol", 0, 20, 7)

indice_pressao = (
    ataques_perigosos * 0.5 +
    posse_bola * 0.2 +
    chutes_gol * 2
)

st.write(f"📈 Índice de pressão: {indice_pressao:.1f}")

if indice_pressao > 60:
    st.success("🚨 Forte possibilidade de gol nos próximos minutos")
elif indice_pressao > 40:
    st.warning("⚠️ Pressão moderada")
else:
    st.error("❄️ Jogo morno / baixo ritmo")
# ===================================
# DECISÃO FINAL DA IA
# ===================================

st.divider()

st.header("🧠 DECISÃO DA IA")

prob_gol = (
    ataques_perigosos * 0.4 +
    posse_bola * 0.2 +
    chutes_gol * 0.4
)

st.metric("Probabilidade de Gol", f"{prob_gol:.1f}%")

# ===================================
# ALERTAS INTELIGENTES
# ===================================

if prob_gol >= 75:
    st.success("🚨 ENTRADA FORTE PARA GOL")
    
elif prob_gol >= 60:
    st.warning("⚠️ Jogo com tendência ofensiva")
    
else:
    st.info("❄️ Mercado sem pressão suficiente")

# ===================================
# OVER 1.5
# ===================================

st.divider()

st.subheader("📈 Mercado Over 1.5")

if chutes_gol >= 10 and ataques_perigosos >= 70:
    st.success("🔥 Forte tendência para OVER 1.5")
else:
    st.warning("⚠️ Over ainda sem confirmação")

# ===================================
# PRESSÃO EXTREMA
# ===================================

st.divider()

st.subheader("🔥 Detector de Pressão")

if indice_pressao >= 80:
    st.error("🚨 PRESSÃO EXTREMA — GOL PODE SAIR A QUALQUER MOMENTO")
    
elif indice_pressao >= 65:
    st.warning("⚠️ Pressão ofensiva alta")
    
else:
    st.info("🧊 Jogo controlado")

# ===================================
# LEITURA TÁTICA
# ===================================

st.divider()

st.subheader("🧠 Leitura Tática da IA")
if posse_bola > 60 and ataques_perigosos > 70:
    st.success("📈 Time dominante ofensivamente")

elif posse_bola < 45 and ataques_perigosos < 40:
    st.warning("📉 Time recuado e sem criação")
# ===================================
# JOGOS AO VIVO AUTOMÁTICOS
# ===================================

st.divider()

st.header("📺 Jogos Ao Vivo")
st.divider()
st.divider()

st.header("🧠 Análise Pré-Jogo")

# BUSCAR JOGOS DO DIA
from datetime import datetime

hoje = datetime.today().strftime('%Y-%m-%d')

url_jogos = f"https://v3.football.api-sports.io/fixtures?date={hoje}"

resposta_jogos = requests.get(url_jogos, headers=headers)

if resposta_jogos.status_code == 200:

    dados_jogos = resposta_jogos.json()

    lista_jogos = {}

    for jogo in dados_jogos["response"]:

        casa = jogo["teams"]["home"]["name"]
        fora = jogo["teams"]["away"]["name"]

        nome = f"{casa} x {fora}"

        fixture_id = jogo["fixture"]["id"]

        lista_jogos[nome] = fixture_id

    jogo_escolhido = st.selectbox(
        "Escolha o jogo",
        list(lista_jogos.keys())
    )

    fixture_id = lista_jogos[jogo_escolhido]
      st.success(f"🎯 Jogo selecionado: {jogo_escolhido}")

    # BUSCAR ESTATÍSTICAS
    stats_url = f"https://v3.football.api-sports.io/fixtures/statistics?fixture={fixture_id}"

    resposta_stats = requests.get(stats_url, headers=headers)

    if resposta_stats.status_code == 200:

         stats_data = resposta_stats.json()
          st.subheader("📊 Leitura da IA")

        try:

            time_casa = stats_data["response"][0]["team"]["name"]
            time_fora = stats_data["response"][1]["team"]["name"]

            st.write(f"🏠 Casa: {time_casa}")
            st.write(f"✈️ Fora: {time_fora}")

            st.success("✅ Dados carregados")

        except:

            st.warning("⚠️ Estatísticas ainda não disponíveis")

else:

    st.error("Erro ao carregar jogos")
