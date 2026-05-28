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

    
