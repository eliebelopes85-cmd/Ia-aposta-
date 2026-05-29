import streamlit as st
import requests
from datetime import datetime

# =====================================================
# CONFIGURAÇÃO DA PÁGINA
# =====================================================

st.set_page_config(
    page_title="Esportivo PRO IA",
    layout="wide"
)

# =====================================================
# API KEY
# =====================================================

API_KEY = "SUA_API_KEY"

HEADERS = {
    "x-apisports-key": API_KEY
}

# =====================================================
# FUNÇÃO BUSCAR JOGOS AO VIVO
# =====================================================

def buscar_jogos():

    try:

        url = "https://v3.football.api-sports.io/fixtures?live=all"

        response = requests.get(url, headers=HEADERS)

        data = response.json()

        if "response" in data:
            return data["response"]

        return []

    except Exception as erro:

        st.error(f"Erro API: {erro}")

        return []

# =====================================================
# FUNÇÃO BUSCAR ESTATÍSTICAS
# =====================================================

def buscar_estatisticas(fixture_id):

    try:

        url = f"https://v3.football.api-sports.io/fixtures/statistics?fixture={fixture_id}"

        response = requests.get(url, headers=HEADERS)

        data = response.json()

        if "response" in data:
            return data["response"]

        return []

    except Exception as erro:

        st.error(f"Erro Estatísticas: {erro}")

        return []

# =====================================================
# EXTRAIR VALORES
# =====================================================

def pegar_estatistica(stats, tipo):

    try:

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

    except:
        return 0

# =====================================================
# IA PRESSÃO
# =====================================================

def calcular_score(
    posse,
    ataques,
    finalizacoes,
    finalizacoes_gol,
    escanteios
):

    try:

        score = (
            posse * 0.15 +
            ataques * 0.30 +
            finalizacoes * 4 +
            finalizacoes_gol * 6 +
            escanteios * 2
        )

        return round(score, 2)

    except:
        return 0

# =====================================================
# ALERTA IA
# =====================================================

def gerar_alerta(score):

    if score >= 90:
        return "🔥 EXTREMAMENTE FORTE"

    elif score >= 70:
        return "🔥 FORTE CHANCE DE GOL"

    elif score >= 50:
        return "⚠️ PRESSÃO MODERADA"

    else:
        return "❄️ BAIXA PRESSÃO"

# =====================================================
# CABEÇALHO
# =====================================================

st.title("⚽ Esportivo PRO IA")

st.markdown("---")

# =====================================================
# BOTÃO ATUALIZAR
# =====================================================

if st.button("🔄 Atualizar Jogos"):
    st.rerun()

# =====================================================
# BUSCAR JOGOS
# =====================================================

jogos = buscar_jogos()

# =====================================================
# SEM JOGOS
# =====================================================

if len(jogos) == 0:

    st.warning("Nenhum jogo ao vivo encontrado.")

# =====================================================
# LOOP DOS JOGOS
# =====================================================

for jogo in jogos:

    try:

        fixture_id = jogo["fixture"]["id"]

        minuto = jogo["fixture"]["status"]["elapsed"]

        status = jogo["fixture"]["status"]["short"]

        liga = jogo["league"]["name"]

        time_casa = jogo["teams"]["home"]["name"]

        time_fora = jogo["teams"]["away"]["name"]

        gols_casa = jogo["goals"]["home"]

        gols_fora = jogo["goals"]["away"]

        # =================================================
        # CABEÇALHO JOGO
        # =================================================

        st.markdown("---")

        st.subheader(
            f"⚽ {time_casa} {gols_casa} x {gols_fora} {time_fora}"
        )

        col_a, col_b, col_c = st.columns(3)

        with col_a:
            st.metric("⏱️ Minuto", minuto)

        with col_b:
            st.metric("🏆 Liga", liga)

        with col_c:
            st.metric("📡 Status", status)

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

        posse_casa = pegar_estatistica(
            home_stats,
            "Ball Possession"
        )

        ataques_casa = pegar_estatistica(
            home_stats,
            "Dangerous Attacks"
        )

        finalizacoes_casa = pegar_estatistica(
            home_stats,
            "Total Shots"
        )

        finalizacoes_gol_casa = pegar_estatistica(
            home_stats,
            "Shots on Goal"
        )

        escanteios_casa = pegar_estatistica(
            home_stats,
            "Corner Kicks"
        )

        # =================================================
        # FORA
        # =================================================

        posse_fora = pegar_estatistica(
            away_stats,
            "Ball Possession"
        )

        ataques_fora = pegar_estatistica(
            away_stats,
            "Dangerous Attacks"
        )

        finalizacoes_fora = pegar_estatistica(
            away_stats,
            "Total Shots"
        )

        finalizacoes_gol_fora = pegar_estatistica(
            away_stats,
            "Shots on Goal"
        )

        escanteios_fora = pegar_estatistica(
            away_stats,
            "Corner Kicks"
        )

        # =================================================
        # SCORE IA
        # =================================================

        score_casa = calcular_score(
            posse_casa,
            ataques_casa,
            finalizacoes_casa,
            finalizacoes_gol_casa,
            escanteios_casa
        )

        score_fora = calcular_score(
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
        # TIME CASA
        # =================================================

        with col1:

            st.markdown(f"## 🏠 {time_casa}")

            st.metric("Posse", f"{posse_casa}%")

            st.metric("Ataques", ataques_casa)

            st.metric("Finalizações", finalizacoes_casa)

            st.metric(
                "Finalizações no Gol",
                finalizacoes_gol_casa
            )

            st.metric("Escanteios", escanteios_casa)

            st.metric("Score IA", score_casa)

        # =================================================
        # TIME FORA
        # =================================================

        with col2:

            st.markdown(f"## ✈️ {time_fora}")

            st.metric("Posse", f"{posse_fora}%")

            st.metric("Ataques", ataques_fora)

            st.metric("Finalizações", finalizacoes_fora)

            st.metric(
                "Finalizações no Gol",
                finalizacoes_gol_fora
            )

            st.metric("Escanteios", escanteios_fora)

            st.metric("Score IA", score_fora)

        # =================================================
        # RESULTADO IA
        # =================================================

        st.markdown("---")

        st.subheader("📈 Resultado IA")

        alerta_casa = gerar_alerta(score_casa)

        alerta_fora = gerar_alerta(score_fora)

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

✅ Ambas Marcam

✅ Over Escanteios

⚠️ Sem tendência clara
            """)

    except Exception as erro:

        st.error(f"Erro no jogo: {erro}")

# =====================================================
# RODAPÉ
# =====================================================

st.markdown("---")

st.caption("IA Trader Esportivo PRO • Live Analytics")
