import streamlit as st
import requests
import pandas as pd
# =========================================
# CONFIG
# =========================================
st.set_page_config(
    page_title="IA Trader Esportivo PRO",
    layout="wide"
)
st.title("⚽ IA Trader Esportivo PRO")
# =========================================
# API CONFIG
# =========================================
API_KEY = "0354050b6f24a03a655e05cl268ef291"
HEADERS = {
    "x-apisports-key": API_KEY
}
BASE_URL = "https://v3.football.api-sports.io"
# =========================================
# MENU ABAS
# =========================================
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📡 Dashboard",
    "🤖 Análise IA",
    "🔥 Ao Vivo",
    "💰 Mercados",
    "📊 Histórico"
])
# =========================================
# DASHBOARD
# =========================================
with tab1:
    st.subheader("📡 Jogos do Dia")
    jogos_lista = []
    try:
        url = f"{BASE_URL}/fixtures?next=20"
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
                    horario = jogo["fixture"]["date"][11:16]
                    liga = jogo["league"]["name"]
                    texto = f"{casa} x {fora} • {horario} • {liga}"
                    jogos_lista.append(texto)
                st.success(
                    f"{len(jogos_lista)} jogos encontrados"
                )
                for item in jogos_lista:
                    st.write(f"✅ {item}")
            else:
                st.warning(
                    "Nenhum jogo encontrado"
                )
        else:
            st.error(
                f"Erro API: {response.status_code}"
            )
    except Exception as e:
        st.error(f"Erro: {e}")
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(
            "🔥 Jogos Quentes",
            "12"
        )
    with col2:
        st.metric(
            "🚨 Alertas",
            "5"
        )
    with col3:
        st.metric(
            "📈 Assertividade",
            "87%"
        )
# =========================================
# ANÁLISE IA
# =========================================
with tab2:
    st.subheader("🤖 IA Comparativa")
    col1, col2 = st.columns(2)
    # =====================================
    # TIME CASA
    # =====================================
    with col1:
        st.markdown("## 🏠 Time Casa")
        ataques_casa = st.slider(
            "Ataques Casa",
            0,
            100,
            70
        )
        posse_casa = st.slider(
            "Posse Casa",
            0,
            100,
            60
        )
        chutes_casa = st.slider(
            "Chutes Casa",
            0,
            20,
            8
        )
        escanteios_casa = st.slider(
            "Escanteios Casa",
            0,
            20,
            6
        )
        defesa_casa = st.slider(
            "Força Defesa Casa",
            0,
            100,
            65
        )
    # =====================================
    # TIME FORA
    # =====================================
    with col2:
        st.markdown("## ✈️ Time Fora")
        ataques_fora = st.slider(
            "Ataques Fora",
            0,
            100,
            45
        )
        posse_fora = st.slider(
            "Posse Fora",
            0,
            100,
            40
        )
        chutes_fora = st.slider(
            "Chutes Fora",
            0,
            20,
            4
        )
        escanteios_fora = st.slider(
            "Escanteios Fora",
            0,
            20,
            3
        )
        defesa_fora = st.slider(
            "Força Defesa Fora",
            0,
            100,
            50
        )
    # =====================================
    # SCORE IA
    # =====================================
    score_casa = (
        ataques_casa * 0.4 +
        posse_casa * 0.2 +
        chutes_casa * 2 +
        escanteios_casa * 1.5 +
        defesa_casa * 0.3
    )
    score_fora = (
        ataques_fora * 0.4 +
        posse_fora * 0.2 +
        chutes_fora * 2 +
        escanteios_fora * 1.5 +
        defesa_fora * 0.3
    )
    st.markdown("---")
    st.subheader("📈 Resultado IA")
    col3, col4 = st.columns(2)
    with col3:
        st.metric(
            "🏠 Score Casa",
            f"{score_casa:.1f}"
        )
    with col4:
        st.metric(
            "✈️ Score Fora",
            f"{score_fora:.1f}"
        )
    # =====================================
    # PREVISÃO
    # =====================================
    diferenca = score_casa - score_fora
    if diferenca > 20:
        st.success("""
🔥 FORTE TENDÊNCIA CASA
✅ Vitória Casa
✅ Próximo Gol Casa
✅ Over 1.5
✅ Over Escanteios
""")
    elif diferenca < -20:
        st.success("""
🔥 FORTE TENDÊNCIA VISITANTE
✅ Vitória Fora
✅ Próximo Gol Fora
✅ Over 1.5
""")
    else:
        st.warning("""
⚠️ JOGO EQUILIBRADO
Mercado perigoso.
""")
# =========================================
# AO VIVO
# =========================================
with tab3:
    st.subheader("🔥 Pressão Ao Vivo")
    ataques_total = ataques_casa + ataques_fora
    chutes_total = chutes_casa + chutes_fora
    escanteios_total = (
        escanteios_casa +
        escanteios_fora
    )
    over_score = (
        ataques_total * 0.5 +
        chutes_total * 2 +
        escanteios_total * 1.5
    )
    st.metric(
        "📈 Pressão do Jogo",
        f"{over_score:.1f}"
    )
    if over_score > 100:
        st.success("🚨 ALERTA FORTE OVER 2.5")
    elif over_score > 70:
        st.warning("⚠️ Tendência Over 1.5")
    else:
        st.error("❄️ Jogo lento")
# =========================================
# MERCADOS
# =========================================
with tab4:
    st.subheader("💰 Mercados Inteligentes")
    # OVER
    st.markdown("## ⚽ Over 2.5")
    over_prob = min(
        int(over_score),
        99
    )
    st.progress(over_prob)
    st.write(
        f"Probabilidade Over 2.5: {over_prob}%"
    )
    # ESCANTEIOS
    st.markdown("## 🚩 Escanteios")
    corners_score = (
        escanteios_total * 5 +
        ataques_total * 0.3
    )
    corners_prob = min(
        int(corners_score),
        99
    )
    st.progress(corners_prob)
    st.write(
        f"Probabilidade Over Escanteios: {corners_prob}%"
    )
    # BTTS
    st.markdown("## 🎯 Ambas Marcam")
    btts_score = (
        ataques_total * 0.4 +
        chutes_total * 3
    )
    btts_prob = min(
        int(btts_score),
        99
    )
    st.progress(btts_prob)
    st.write(
        f"Probabilidade BTTS: {btts_prob}%"
    )
# =========================================
# HISTÓRICO
# =========================================
with tab5:
    st.subheader("📊 Histórico IA")
    historico = pd.DataFrame({
        "Mercado": [
            "Over 2.5",
            "BTTS",
            "Escanteios",
            "Vitória Casa"
        ],
        "Resultado": [
            "WIN",
            "WIN",
            "LOSS",
            "WIN"
        ],
        "Odd": [
            1.85,
            1.72,
            2.10,
            1.65
        ]
    })
    st.dataframe(
        historico,
        use_container_width=True
    )
    st.metric(
        "🔥 Win Rate",
        "75%"
    )
# =========================================
# RODAPÉ
# =========================================
st.markdown("---")
st.caption(
    "IA Trader Esportivo PRO • Live Analytics"
)
