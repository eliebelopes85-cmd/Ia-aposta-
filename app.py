# =====================================================
# IA AVANÇADA — RADAR PRO
# =====================================================
def calcular_momentum(
    posse,
    ataques,
    finalizacoes,
    finalizacoes_gol,
    escanteios
):
    momentum = (
        posse * 0.12 +
        ataques * 0.28 +
        finalizacoes * 5 +
        finalizacoes_gol * 8 +
        escanteios * 3
    )
    return round(momentum, 2)
def calcular_probabilidade_gol(momentum):
    if momentum >= 120:
        return 95
    elif momentum >= 100:
        return 90
    elif momentum >= 80:
        return 82
    elif momentum >= 60:
        return 70
    elif momentum >= 40:
        return 55
    else:
        return 35
def calcular_probabilidade_escanteios(
    ataques,
    finalizacoes,
    escanteios
):
    valor = (
        ataques * 0.3 +
        finalizacoes * 3 +
        escanteios * 5
    )
    if valor >= 120:
        return "🔥 OVER 10.5 MUITO FORTE"
    elif valor >= 90:
        return "🔥 OVER 8.5 FORTE"
    elif valor >= 70:
        return "⚠️ OVER 7.5 MODERADO"
    else:
        return "❄️ BAIXA PRESSÃO"
def tendencia_ia_avancada(
    score_casa,
    score_fora
):
    diferenca = abs(score_casa - score_fora)
    if score_casa > score_fora:
        if diferenca >= 40:
            return "🔥 DOMÍNIO TOTAL CASA"
        elif diferenca >= 20:
            return "🏠 FORTE PRESSÃO CASA"
        else:
            return "⚖️ LEVE VANTAGEM CASA"
    elif score_fora > score_casa:
        if diferenca >= 40:
            return "🔥 DOMÍNIO TOTAL FORA"
        elif diferenca >= 20:
            return "✈️ FORTE PRESSÃO FORA"
        else:
            return "⚖️ LEVE VANTAGEM FORA"
    else:
        return "⚖️ EQUILIBRADO"
# =====================================================
# ABA RADAR IA
# =====================================================
def renderizar_radar_ia(jogo):
    fixture_id = jogo["fixture"]["id"]
    estatisticas = buscar_estatisticas(fixture_id)
    if len(estatisticas) < 2:
        st.warning("Sem estatísticas disponíveis.")
        return
    home_stats = estatisticas[0]["statistics"]
    away_stats = estatisticas[1]["statistics"]
    time_casa = jogo["teams"]["home"]["name"]
    time_fora = jogo["teams"]["away"]["name"]
    # =========================
    # DADOS CASA
    # =========================
    posse_casa = extrair_valor(home_stats, "Ball Possession")
    ataques_casa = extrair_valor(home_stats, "Dangerous Attacks")
    finalizacoes_casa = extrair_valor(home_stats, "Total Shots")
    gol_casa = extrair_valor(home_stats, "Shots on Goal")
    escanteios_casa = extrair_valor(home_stats, "Corner Kicks")
    # =========================
    # DADOS FORA
    # =========================
    posse_fora = extrair_valor(away_stats, "Ball Possession")
    ataques_fora = extrair_valor(away_stats, "Dangerous Attacks")
    finalizacoes_fora = extrair_valor(away_stats, "Total Shots")
    gol_fora = extrair_valor(away_stats, "Shots on Goal")
    escanteios_fora = extrair_valor(away_stats, "Corner Kicks")
    # =========================
    # IA
    # =========================
    momentum_casa = calcular_momentum(
        posse_casa,
        ataques_casa,
        finalizacoes_casa,
        gol_casa,
        escanteios_casa
    )
    momentum_fora = calcular_momentum(
        posse_fora,
        ataques_fora,
        finalizacoes_fora,
        gol_fora,
        escanteios_fora
    )
    prob_gol_casa = calcular_probabilidade_gol(momentum_casa)
    prob_gol_fora = calcular_probabilidade_gol(momentum_fora)
    corners_casa = calcular_probabilidade_escanteios(
        ataques_casa,
        finalizacoes_casa,
        escanteios_casa
    )
    corners_fora = calcular_probabilidade_escanteios(
        ataques_fora,
        finalizacoes_fora,
        escanteios_fora
    )
    tendencia = tendencia_ia_avancada(
        momentum_casa,
        momentum_fora
    )
    st.markdown("---")
    st.header("🧠 RADAR IA PROFISSIONAL")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader(f"🏠 {time_casa}")
        st.metric(
            "🔥 Momentum",
            momentum_casa
        )
        st.metric(
            "⚽ Probabilidade de Gol",
            f"{prob_gol_casa}%"
        )
        st.metric(
            "📈 Escanteios",
            corners_casa
        )
    with col2:
        st.subheader(f"✈️ {time_fora}")
        st.metric(
            "🔥 Momentum",
            momentum_fora
        )
        st.metric(
            "⚽ Probabilidade de Gol",
            f"{prob_gol_fora}%"
        )
        st.metric(
            "📈 Escanteios",
            corners_fora
        )
    st.markdown("---")
    st.success(f"""
📊 TENDÊNCIA IA:
{tendencia}
🔥 Mercado recomendado:
✅ Over 1.5
✅ Over Escanteios
✅ Próximo Gol
✅ Ambas Marcam
✅ Pressão Ofensiva
🚨 Sistema IA Trader PRO
""
