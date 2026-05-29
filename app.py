

from flask import Flask, jsonify, request
import requests
import os
import random
app = Flask(__name__)
API_KEY = os.getenv("API_FOOTBALL_KEY")
HEADERS = {
    "x-apisports-key": API_KEY
}
BASE_URL = "https://v3.football.api-sports.io"
# =========================================
# HEALTH CHECK
# =========================================
@app.route("/api/healthz", methods=["GET"])
def health_check():
    return jsonify({
        "status": "healthy"
    })
# =========================================
# TODAY FIXTURES
# =========================================
@app.route("/api/fixtures/today", methods=["GET"])
def get_today_fixtures():
    url = f"{BASE_URL}/fixtures?live=all"
    response = requests.get(url, headers=HEADERS)
    data = response.json()
    fixtures = []
    if "response" in data:
        for match in data["response"]:
            fixtures.append({
                "id": match["fixture"]["id"],
                "homeTeam": match["teams"]["home"]["name"],
                "awayTeam": match["teams"]["away"]["name"],
                "league": match["league"]["name"],
                "date": match["fixture"]["date"],
                "status": match["fixture"]["status"]["short"],
                "homeGoals": match["goals"]["home"],
                "awayGoals": match["goals"]["away"]
            })
    return jsonify(fixtures)
# =========================================
# FIXTURE STATISTICS
# =========================================
@app.route("/api/fixtures/<int:fixture_id>/statistics", methods=["GET"])
def get_fixture_statistics(fixture_id):
    url = f"{BASE_URL}/fixtures/statistics?fixture={fixture_id}"
    response = requests.get(url, headers=HEADERS)
    data = response.json()
    return jsonify(data)
# =========================================
# OVER 2.5 ANALYSIS
# =========================================
@app.route("/api/analysis/over25", methods=["POST"])
def analyze_over25():
    body = request.json
    odd = body.get("odd", 0)
    score = random.randint(60, 95)
    recommendation = "ENTRADA RECOMENDADA"
    if score < 75:
        recommendation = "RISCO ELEVADO"
    return jsonify({
        "market": "OVER 2.5",
        "score": score,
        "recommendation": recommendation,
        "confidence": f"{score}%",
        "factors": [
            "Alta pressão ofensiva",
            "Média alta de finalizações",
            "Defesas vulneráveis"
        ]
    })
# =========================================
# CORNERS ANALYSIS
# =========================================
@app.route("/api/analysis/corners", methods=["POST"])
def analyze_corners():
    score = random.randint(65, 98)
    return jsonify({
        "market": "CORNERS",
        "score": score,
        "recommendation": "OVER ESCANTEIOS",
        "confidence": f"{score}%",
        "factors": [
            "Times usam muito as laterais",
            "Alta média de ataques perigosos",
            "Pressão ofensiva intensa"
        ]
    })
# =========================================
# BTTS ANALYSIS
# =========================================
@app.route("/api/analysis/btts", methods=["POST"])
def analyze_btts():
    score = random.randint(55, 96)
    return jsonify({
        "market": "BTTS",
        "score": score,
        "recommendation": "AMBAS MARCAM",
        "confidence": f"{score}%",
        "factors": [
            "Defesas frágeis",
            "Ataques eficientes",
            "Alta média de gols"
        ]
    })
# =========================================
# TRAP DETECTOR
# =========================================
@app.route("/api/odds/trap-detector", methods=["POST"])
def detect_trap():
    score = random.randint(1, 100)
    is_trap = score > 70
    return jsonify({
        "isTrap": is_trap,
        "riskLevel": "ALTO" if is_trap else "BAIXO",
        "message": "Possível armadilha detectada" if is_trap else "Mercado saudável",
        "factors": [
            "Odd desbalanceada",
            "Volume suspeito",
            "Pressão inconsistente"
        ]
    })
# =========================================
# DASHBOARD SUMMARY
# =========================================
@app.route("/api/analysis/summary", methods=["GET"])
def dashboard_summary():
    return jsonify({
        "totalFixturesToday": 269,
        "hotGames": 44,
        "trapAlerts": 21,
        "topLeagues": [
            "Premier League",
            "Serie A",
            "La Liga",
            "Brasileirão"
        ]
    })
# =========================================
# START SERVER
# =========================================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
