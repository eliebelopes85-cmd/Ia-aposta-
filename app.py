import streamlit as st
import requests
import pandas as pd
import os
from datetime import datetime
from streamlit_autorefresh import st_autorefresh


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

st_autorefresh(interval=30000, key="live_update")

# =====================================================
# API CONFIG
# =====================================================

API_KEY = "0354050b6f24a03a655e05cl268ef291"  # <- cole sua chave da API-Football aqui

HEADERS = {
    "x-apisports-key": API_KEY
}

# =====================================================
# FAVORITOS — SESSION STATE
# =====================================================

if "favoritos" not in st.session_state:
    st.session_state.favoritos = []

def is_favorito(jogo):
    time_casa = jogo["teams"]["home"]["name"].lower()
    time_fora = jogo["teams"]["away"]["name"].lower()
    for fav in st.session_state.favoritos:
        if fav.lower() in time_casa or fav.lower() in time_fora:
            return True
    return False

def ordenar_com_favoritos(lista):
    favs    = [j for j in lista if is_favorito(j)]
    normais = [j for j in lista if not is_favorito(j)]
    return favs + normais

# =====================================================
# FUNÇÕES API
# =====================================================

@st.cache_data(ttl=30)
def buscar_jogos_ao_vivo():
    url = "https://v3.football.api-sports.io/fixtures?live=all"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return response.json()["response"]
    return []

@st.cache_data(ttl=120)
def buscar_jogos_pre_jogo():
    hoje = datetime.utcnow().strftime("%Y-%m-%d")
    url  = f"https://v3.football.api-sports.io/fixtures?date={hoje}&status=NS"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return response.json()["response"][:20]
    return []

@st.cache_data(ttl=60)
def buscar_jogos_recentes():
    hoje = datetime.utcnow().strftime("%Y-%m-%d")
    url  = f"https://v3.football.api-sports.io/fixtures?date={hoje}&status=FT"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return response.json()["response"][:10]
    return []

@st.cache_data(ttl=60)
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

def calcular_pressao(posse, ataques, finalizacoes, finalizacoes_gol, escanteios):
    return round(
        posse * 0.15 +
        ataques * 0.30 +
        finalizacoes * 4 +
        finalizacoes_gol * 6 +
        escanteios * 2,
        2
    )

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
# SCORES IA DE UM JOGO
# =====================================================

def scores_do_jogo(fixture_id):
    estatisticas = buscar_estatisticas(fixture_id)
    if len(estatisticas) < 2:
        return None, None
    home_stats = estatisticas[0]["statistics"]
    away_stats = estatisticas[1]["statistics"]
    score_casa = calcular_pressao(
        extrair_valor(home_stats, "Ball Possession"),
        extrair_valor(home_stats, "Dangerous Attacks"),
        extrair_valor(home_stats, "Total Shots"),
        extrair_valor(home_stats, "Shots on Goal"),
        extrair_valor(home_stats, "Corner Kicks"),
    )
    score_fora = calcular_pressao(
        extrair_valor(away_stats, "Ball Possession"),
        extrair_valor(away_stats, "Dangerous Attacks"),
        extrair_valor(away_stats, "Total Shots"),
        extrair_valor(away_stats, "Shots on Goal"),
        extrair_valor(away_stats, "Corner Kicks"),
    )
    return score_casa, score_fora

# =====================================================
# CONSTRUIR LINHA DE RESUMO
# =====================================================

def construir_linha_resumo(jogo, status_label):
    fixture_id = jogo["fixture"]["id"]
    liga       = jogo["league"]["name"]
    time_casa  = jogo["teams"]["home"]["name"]
    time_fora  = jogo["teams"]["away"]["name"]
    gols_casa  = jogo["goals"]["home"]
    gols_fora  = jogo["goals"]["away"]
    fav_badge  = " ⭐" if is_favorito(jogo) else ""

    score_casa, score_fora = scores_do_jogo(fixture_id)

    if score_casa is None:
        return {
            "Status":      status_label,
            "Liga":        liga,
            "Casa":        time_casa + fav_badge,
            "Placar":      f"{gols_casa} x {gols_fora}",
            "Fora":        time_fora + fav_badge,
            "Score IA 🏠": "-",
            "Score IA ✈️": "-",
            "Tendência":   "—",
        }

    if score_casa > score_fora:
        tendencia = "🏠 Casa"
    elif score_fora > score_casa:
        tendencia = "✈️ Fora"
    else:
        tendencia = "⚖️ Equil."

    return {
        "Status":      status_label,
        "Liga":        liga,
        "Casa":        time_casa + fav_badge,
        "Placar":      f"{gols_casa} x {gols_fora}",
        "Fora":        time_fora + fav_badge,
        "Score IA 🏠": score_casa,
        "Score IA ✈️": score_fora,
        "Tendência":   tendencia,
    }

# =====================================================
# RENDERIZAR JOGO AO VIVO / ENCERRADO
# =====================================================

def renderizar_jogo(jogo, ao_vivo=True):
    fixture_id = jogo["fixture"]["id"]
    minuto     = jogo["fixture"]["status"]["elapsed"]
    liga       = jogo["league"]["name"]
    time_casa  = jogo["teams"]["home"]["name"]
    time_fora  = jogo["teams"]["away"]["name"]
    gols_casa  = jogo["goals"]["home"]
    gols_fora  = jogo["goals"]["away"]
    fav_badge  = " ⭐ FAVORITO" if is_favorito(jogo) else ""

    st.markdown("---")

    if ao_vivo:
        st.subheader(f"⚽ {time_casa} {gols_casa} x {gols_fora} {time_fora}{fav_badge}")
        st.write(f"🏆 Liga: {liga}")
        st.write(f"⏱️ Minuto: {minuto}")
    else:
        st.subheader(f"⚽ {time_casa} {gols_casa} x {gols_fora} {time_fora}  🏁 Encerrado{fav_badge}")
        st.write(f"🏆 Liga: {liga}")

    score_casa, score_fora = scores_do_jogo(fixture_id)

    if score_casa is None:
        st.warning("Sem estatísticas disponíveis.")
        return

    estatisticas = buscar_estatisticas(fixture_id)
    home_stats   = estatisticas[0]["statistics"]
    away_stats   = estatisticas[1]["statistics"]

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"## 🏠 {time_casa}")
        st.metric("Posse",               f"{extrair_valor(home_stats, 'Ball Possession')}%")
        st.metric("Ataques",             extrair_valor(home_stats, "Dangerous Attacks"))
        st.metric("Finalizações",        extrair_valor(home_stats, "Total Shots"))
        st.metric("Finalizações no Gol", extrair_valor(home_stats, "Shots on Goal"))
        st.metric("Escanteios",          extrair_valor(home_stats, "Corner Kicks"))
        st.metric("Score IA",            score_casa)

    with col2:
        st.markdown(f"## ✈️ {time_fora}")
        st.metric("Posse",               f"{extrair_valor(away_stats, 'Ball Possession')}%")
        st.metric("Ataques",             extrair_valor(away_stats, "Dangerous Attacks"))
        st.metric("Finalizações",        extrair_valor(away_stats, "Total Shots"))
        st.metric("Finalizações no Gol", extrair_valor(away_stats, "Shots on Goal"))
        st.metric("Escanteios",          extrair_valor(away_stats, "Corner Kicks"))
        st.metric("Score IA",            score_fora)

    st.markdown("---")
    st.subheader("📈 Resultado IA")

    alerta_casa = probabilidade_gol(score_casa)
    alerta_fora = probabilidade_gol(score_fora)

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
    else:
        st.warning("""
⚖️ Jogo equilibrado

✅ Mercado Ambas Marcam

✅ Over Escanteios

⚠️ Sem tendência clara
        """)

# =====================================================
# RENDERIZAR PRÉ JOGO
# =====================================================

def renderizar_pre_jogo(jogo):
    liga      = jogo["league"]["name"]
    time_casa = jogo["teams"]["home"]["name"]
    time_fora = jogo["teams"]["away"]["name"]
    fav_badge = " ⭐ FAVORITO" if is_favorito(jogo) else ""

    horario_utc = jogo["fixture"].get("date", "")
    try:
        dt      = datetime.fromisoformat(horario_utc.replace("Z", "+00:00"))
        horario = dt.strftime("%H:%M UTC")
    except Exception:
        horario = "—"

    st.markdown("---")
    st.subheader(f"🕐 {time_casa}  vs  {time_fora}{fav_badge}")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.write(f"🏆 **Liga:** {liga}")
    with col2:
        st.write(f"🏠 **Casa:** {time_casa}")
    with col3:
        st.write(f"✈️ **Fora:** {time_fora}")

    st.caption(f"⏰ Horário: {horario}")

# =====================================================
# TÍTULO
# =====================================================

st.title("⚽ Esportivo PRO IA")
st.markdown("---")

# =====================================================
# VERIFICAR API KEY
# =====================================================

if not API_KEY:
    st.error("⚠️ Chave de API não configurada. Adicione o secret **API_FOOTBALL_KEY** com sua chave da API-Football.")
    st.stop()

# =====================================================
# BUSCAR TODOS OS JOGOS
# =====================================================

jogos          = buscar_jogos_ao_vivo()
jogos_pre      = buscar_jogos_pre_jogo()

with st.spinner("Carregando jogos encerrados..."):
    jogos_recentes = buscar_jogos_recentes()

# =====================================================
# SIDEBAR — FILTRO DE LIGAS
# =====================================================

ligas_ao_vivo  = sorted({j["league"]["name"] for j in jogos})
ligas_pre      = sorted({j["league"]["name"] for j in jogos_pre})
ligas_recentes = sorted({j["league"]["name"] for j in jogos_recentes})
todas_as_ligas = sorted(set(ligas_ao_vivo + ligas_pre + ligas_recentes))

st.sidebar.title("🔍 Filtros")

if todas_as_ligas:
    ligas_selecionadas = st.sidebar.multiselect(
        "Competições",
        options=todas_as_ligas,
        default=todas_as_ligas,
        help="Selecione as ligas que deseja visualizar"
    )
else:
    ligas_selecionadas = []
    st.sidebar.info("Nenhuma liga disponível no momento.")

def filtrar(lista):
    if not ligas_selecionadas:
        return lista
    return [j for j in lista if j["league"]["name"] in ligas_selecionadas]

jogos_filtrados          = ordenar_com_favoritos(filtrar(jogos))
jogos_pre_filtrados      = ordenar_com_favoritos(filtrar(jogos_pre))
jogos_recentes_filtrados = ordenar_com_favoritos(filtrar(jogos_recentes))

# =====================================================
# SIDEBAR — FAVORITOS
# =====================================================

st.sidebar.markdown("---")
st.sidebar.subheader("⭐ Times Favoritos")

novo_fav = st.sidebar.text_input(
    "Adicionar time",
    placeholder="Ex: Flamengo",
    key="input_fav"
)

if st.sidebar.button("➕ Adicionar", key="btn_add_fav"):
    nome = novo_fav.strip()
    if nome and nome not in st.session_state.favoritos:
        st.session_state.favoritos.append(nome)
        st.rerun()

if st.session_state.favoritos:
    for fav in list(st.session_state.favoritos):
        col_fav, col_rm = st.sidebar.columns([4, 1])
        col_fav.write(f"⭐ {fav}")
        if col_rm.button("✕", key=f"rm_{fav}"):
            st.session_state.favoritos.remove(fav)
            st.rerun()
else:
    st.sidebar.caption("Nenhum time favorito ainda.")

# =====================================================
# SIDEBAR — ALERTAS IA AO VIVO
# =====================================================

st.sidebar.markdown("---")
st.sidebar.subheader("🚨 Alertas IA — Ao Vivo")

if not jogos_filtrados:
    st.sidebar.info("Nenhum jogo ao vivo no momento.")
else:
    alertas = []
    for j in jogos_filtrados:
        sc, sf = scores_do_jogo(j["fixture"]["id"])
        if sc is None:
            continue
        melhor_score  = max(sc, sf)
        time_destaque = j["teams"]["home"]["name"] if sc >= sf else j["teams"]["away"]["name"]
        alertas.append({
            "score":         melhor_score,
            "confronto":     f"{j['teams']['home']['name']} x {j['teams']['away']['name']}",
            "time_destaque": time_destaque,
            "liga":          j["league"]["name"],
            "alerta":        probabilidade_gol(melhor_score),
            "favorito":      is_favorito(j),
        })

    alertas.sort(key=lambda x: (x["favorito"], x["score"]), reverse=True)

    if not alertas:
        st.sidebar.info("Aguardando estatísticas dos jogos ao vivo.")
    else:
        for i, a in enumerate(alertas[:5], start=1):
            badge = " ⭐" if a["favorito"] else ""
            st.sidebar.markdown(
                f"**#{i} {a['confronto']}{badge}**  \n"
                f"{a['liga']}  \n"
                f"🏆 {a['time_destaque']} — Score: `{a['score']}`  \n"
                f"{a['alerta']}"
            )
            st.sidebar.markdown("---")

# =====================================================
# TABELA RESUMO DO DIA
# =====================================================

todos_filtrados = jogos_filtrados + jogos_recentes_filtrados

st.header("📋 Resumo do Dia")

if not todos_filtrados:
    st.info("Nenhum jogo ao vivo ou encerrado para as ligas selecionadas.")
else:
    with st.spinner("Calculando scores IA..."):
        linhas = []
        for j in jogos_filtrados:
            linhas.append(construir_linha_resumo(j, "🔴 Ao Vivo"))
        for j in jogos_recentes_filtrados:
            linhas.append(construir_linha_resumo(j, "🏁 Encerrado"))

    df = pd.DataFrame(linhas)

    def colorir_linha(row):
        is_fav = "⭐" in str(row.get("Casa", "")) or "⭐" in str(row.get("Fora", ""))
        base = "background-color: #fffde7;" if is_fav else ""
        styles = [base] * len(row)
        tend_idx = list(row.index).index("Tendência") if "Tendência" in row.index else -1
        if tend_idx >= 0:
            val = str(row["Tendência"])
            if "Casa" in val:
                styles[tend_idx] = base + "background-color: #d4edda; color: #155724;"
            elif "Fora" in val:
                styles[tend_idx] = base + "background-color: #f8d7da; color: #721c24;"
            elif "Equil" in val:
                styles[tend_idx] = base + "background-color: #fff3cd; color: #856404;"
        return styles

    styled = df.style.apply(colorir_linha, axis=1)
    st.dataframe(styled, use_container_width=True, hide_index=True)

st.markdown("---")

# =====================================================
# SEÇÃO AO VIVO
# =====================================================

st.header("🔴 Jogos Ao Vivo")

if len(jogos) == 0:
    st.warning("Nenhum jogo ao vivo no momento.")
elif len(jogos_filtrados) == 0:
    st.info("Nenhum jogo ao vivo para as ligas selecionadas.")
else:
    for jogo in jogos_filtrados:
        renderizar_jogo(jogo, ao_vivo=True)

st.markdown("---")

# =====================================================
# SEÇÃO PRÉ JOGO
# =====================================================

st.header("⏳ Pré Jogo — Hoje")

if len(jogos_pre) == 0:
    st.info("Nenhum jogo agendado para hoje.")
elif len(jogos_pre_filtrados) == 0:
    st.info("Nenhum pré-jogo para as ligas selecionadas.")
else:
    st.caption(f"{len(jogos_pre_filtrados)} jogo(s) agendado(s) para hoje")
    for jogo in jogos_pre_filtrados:
        renderizar_pre_jogo(jogo)

st.markdown("---")

# =====================================================
# SEÇÃO JOGOS ENCERRADOS HOJE
# =====================================================

st.header("🕓 Jogos Encerrados Hoje")

if len(jogos_recentes) == 0:
    st.info("Nenhum jogo encerrado hoje ainda.")
elif len(jogos_recentes_filtrados) == 0:
    st.info("Nenhum jogo encerrado para as ligas selecionadas.")
else:
    for jogo in jogos_recentes_filtrados:
        renderizar_jogo(jogo, ao_vivo=False)

# =====================================================
# FOOTER
# =====================================================

st.markdown("---")
st.caption("IA Trader Esportivo PRO • Live Analytics")
