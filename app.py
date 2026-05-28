impimport streamlit as st
import requests

API_KEY = "27eb4c6573548e562e26d6f70052f8bd"

headers = {
    "x-apisports-key": API_KEY
}st.title("Jogos de Hoje")

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

else:
    st.error("Erro ao conectar API")
