
import streamlit as st
import pandas as pd
import numpy as np
import joblib
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import train_test_split

st.set_page_config(page_title="IA de Apostas", layout="wide")

st.title("⚽ IA de Apostas Profissional")
st.markdown("Modelo avançado com probabilidades e análise de valor.")

# =====================================
# DADOS REAIS EXEMPLO
# =====================================

dados = pd.DataFrame({
    "odds_casa": np.random.uniform(1.4, 3.5, 500),
    "odds_empate": np.random.uniform(2.8, 4.2, 500),
    "odds_fora": np.random.uniform(1.8, 5.5, 500),
    "xg_casa": np.random.uniform(0.5, 2.5, 500),
    "xg_fora": np.random.uniform(0.3, 2.0, 500),
    "forma_casa": np.random.randint(0, 15, 500),
    "forma_fora": np.random.randint(0, 15, 500),
    "resultado": np.random.choice([0,1,2], 500)
})

X = dados.drop(columns=["resultado"])
y = dados["resultado"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

modelo = GradientBoostingClassifier()
modelo.fit(X_train, y_train)

# =====================================
# INTERFACE
# =====================================

col1, col2 = st.columns(2)

with col1:
    st.subheader("Time da Casa")
    odds_casa = st.number_input("Odd Casa", value=1.85)
    xg_casa = st.number_input("xG Casa", value=1.7)
    forma_casa = st.slider("Forma Casa", 0, 15, 10)

with col2:
    st.subheader("Time Visitante")
    odds_fora = st.number_input("Odd Fora", value=4.20)
    xg_fora = st.number_input("xG Fora", value=0.9)
    forma_fora = st.slider("Forma Fora", 0, 15, 6)

odds_empate = st.number_input("Odd Empate", value=3.40)

if st.button("Analisar Jogo"):

    entrada = pd.DataFrame([{
        "odds_casa": odds_casa,
        "odds_empate": odds_empate,
        "odds_fora": odds_fora,
        "xg_casa": xg_casa,
        "xg_fora": xg_fora,
        "forma_casa": forma_casa,
        "forma_fora": forma_fora
    }])

    probs = modelo.predict_proba(entrada)[0]

    prob_fora = round(probs[0] * 100, 2)
    prob_empate = round(probs[1] * 100, 2)
    prob_casa = round(probs[2] * 100, 2)

    st.subheader("📊 Probabilidades")

    st.metric("Vitória Casa", f"{prob_casa}%")
    st.metric("Empate", f"{prob_empate}%")
    st.metric("Vitória Fora", f"{prob_fora}%")

    # =====================
    # EV
    # =====================

    ev_casa = (probs[2] * odds_casa) - 1
    ev_empate = (probs[1] * odds_empate) - 1
    ev_fora = (probs[0] * odds_fora) - 1

    st.subheader("💰 Value Bets")

    if ev_casa > 0:
        st.success(f"Valor na Casa | EV = {round(ev_casa,2)}")

    if ev_empate > 0:
        st.success(f"Valor no Empate | EV = {round(ev_empate,2)}")

    if ev_fora > 0:
        st.success(f"Valor no Visitante | EV = {round(ev_fora,2)}")

    if ev_casa <= 0 and ev_empate <= 0 and ev_fora <= 0:
        st.warning("Nenhuma aposta de valor encontrada.")
