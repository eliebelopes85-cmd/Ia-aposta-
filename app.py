openapi: 3.1.0
info:
  title: Api
  version: 0.1.0
  description: IA Trader Esportivo API
servers:
  - url: /api
    description: Base API path
tags:
  - name: health
    description: Health operations
  - name: fixtures
    description: Football fixtures and statistics
  - name: odds
    description: Odds scanning and analysis
  - name: analysis
    description: AI analysis and alerts
paths:
  /healthz:
    get:
      operationId: healthCheck
      tags: [health]
      summary: Health check
      responses:
        "200":
          description: Healthy
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/HealthStatus"

  /fixtures/today:
    get:
      operationId: getTodayFixtures
      tags: [fixtures]
      from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "API funcionando"

app.run(host="0.0.0.0", port=3000)
      responses:
        "200":
          description: List of today's fixtures
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: "#/components/schemas/Fixture"

  /fixtures/{fixtureId}/statistics:
    get:
      operationId: getFixtureStatistics
      tags: [fixtures]
      summary: Get live statistics for a fixture
      parameters:
        - name: fixtureId
          in: path
          required: true
          schema:
            type: integer
      responses:
        "200":
          description: Fixture statistics
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/FixtureStatistics"
        "404":
          description: Fixture not found

  /fixtures/{fixtureId}/analysis:
    post:
      operationId: analyzeFixture
      tags: [analysis]
      summary: Run AI analysis on a fixture with given odds
      parameters:
        - name: fixtureId
          in: path
          required: true
          schema:
            type: integer
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/AnalysisInput"
      responses:
        "200":
          description: AI analysis result
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/AnalysisResult"

  /odds/scan:
    get:
      operationId: scanOdds
      tags: [odds]
      summary: Scan live odds from all sports
      responses:
        "200":
          description: Odds scan results
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: "#/components/schemas/OddsEntry"

  /odds/trap-detector:
    post:
      operationId: detectTrap
      tags: [odds]
      summary: Detect if a market is a trap
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/TrapInput"
      responses:
        "200":
          description: Trap detection result
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/TrapResult"

  /analysis/over25:
    post:
      operationId: analyzeOver25
      tags: [analysis]
      summary: Analyze Over 2.5 market for a fixture
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/MarketAnalysisInput"
      responses:
        "200":
          description: Over 2.5 analysis
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/MarketAnalysisResult"

  /analysis/corners:
    post:
      operationId: analyzeCorners
      tags: [analysis]
      summary: Analyze corners market for a fixture
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/MarketAnalysisInput"
      responses:
        "200":
          description: Corners analysis
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/MarketAnalysisResult"

  /analysis/btts:
    post:
      operationId: analyzeBtts
      tags: [analysis]
      summary: Analyze BTTS (Both Teams To Score) market
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/MarketAnalysisInput"
      responses:
        "200":
          description: BTTS analysis
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/MarketAnalysisResult"

  /history:
    get:
      operationId: listHistory
      tags: [analysis]
      summary: List all saved analysis history
      responses:
        "200":
          description: List of history entries
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: "#/components/schemas/HistoryEntry"
    post:
      operationId: saveHistory
      tags: [analysis]
      summary: Save an analysis to history
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/SaveAnalysisHistoryBody"
      responses:
        "201":
          description: Saved history entry
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/HistoryEntry"
    delete:
      operationId: clearHistory
      tags: [analysis]
      summary: Clear all history
      responses:
        "204":
          description: History cleared

  /history/{id}/result:
    patch:
      operationId: updateHistoryResult
      tags: [analysis]
      summary: Update the result of a history entry (WIN/LOSS/VOID)
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: integer
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/SetHistoryResultBody"
      responses:
        "200":
          description: Updated entry
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/HistoryEntry"
        "404":
          description: Entry not found

  /analysis/summary:
    get:
      operationId: getDashboardSummary
      tags: [analysis]
      summary: Get dashboard summary stats
      responses:
        "200":
          description: Dashboard summary
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/DashboardSummary"

components:
  schemas:
    HealthStatus:
      type: object
      required: [status]
      properties:
        status:
          type: string

    Fixture:
      type: object
      required: [id, homeTeam, awayTeam, league, date, status]
      properties:
        id:
          type: integer
        homeTeam:
          type: string
        awayTeam:
          type: string
        league:
          type: string
        date:
          type: string
        status:
          type: string
        homeGoals:
          type: ["integer", "null"]
        awayGoals:
          type: ["integer", "null"]

    FixtureStatistics:
      type: object
      required: [fixtureId, homePossession, awayPossession, homeShotsOnGoal, awayShotsOnGoal, homeCorners, awayCorners, homeAttacks, awayAttacks]
      properties:
        fixtureId:
          type: integer
        homePossession:
          type: number
        awayPossession:
          type: number
        homeShotsOnGoal:
          type: integer
        awayShotsOnGoal:
          type: integer
        homeCorners:
          type: integer
        awayCorners:
          type: integer
        homeAttacks:
          type: integer
        awayAttacks:
          type: integer

    AnalysisInput:
      type: object
      required: [oddHome, oddDraw, oddAway, oddOver25]
      properties:
        oddHome:
          type: number
        oddDraw:
          type: number
        oddAway:
          type: number
        oddOver25:
          type: number
        oddBtts:
          type: ["number", "null"]

    AnalysisResult:
      type: object
      required: [score, level, alerts, recommendation]
      properties:
        score:
          type: integer
        level:
          type: string
        alerts:
          type: array
          items:
            $ref: "#/components/schemas/Alert"
        recommendation:
          type: string

    Alert:
      type: object
      required: [type, message]
      properties:
        type:
          type: string
        message:
          type: string

    OddsEntry:
      type: object
      required: [game, bookmaker, market, team, odd]
      properties:
        game:
          type: string
        bookmaker:
          type: string
        market:
          type: string
        team:
          type: string
        odd:
          type: number

    TrapInput:
      type: object
      required: [oddFavorite, possession, attacks]
      properties:
        oddFavorite:
          type: number
        possession:
          type: number
        attacks:
          type: number

    TrapResult:
      type: object
      required: [isTrap, riskLevel, message, factors]
      properties:
        isTrap:
          type: boolean
        riskLevel:
          type: string
        message:
          type: string
        factors:
          type: array
          items:
            type: string

    MarketAnalysisInput:
      type: object
      required: [fixtureId, odd]
      properties:
        fixtureId:
          type: integer
        odd:
          type: number

    MarketAnalysisResult:
      type: object
      required: [market, score, recommendation, confidence, factors]
      properties:
        market:
          type: string
        score:
          type: integer
        recommendation:
          type: string
        confidence:
          type: string
        factors:
          type: array
          items:
            type: string

    HistoryEntry:
      type: object
      required: [id, market, homeTeam, awayTeam, league, score, level, recommendation, odd, createdAt]
      properties:
        id:
          type: integer
        market:
          type: string
        homeTeam:
          type: string
        awayTeam:
          type: string
        league:
          type: string
        fixtureId:
          type: ["integer", "null"]
        score:
          type: integer
        level:
          type: string
        recommendation:
          type: string
        odd:
          type: string
        result:
          type: ["string", "null"]
        createdAt:
          type: string

    SaveAnalysisHistoryBody:
      type: object
      required: [market, homeTeam, awayTeam, score, level, recommendation, odd]
      properties:
        market:
          type: string
        homeTeam:
          type: string
        awayTeam:
          type: string
        league:
          type: string
        fixtureId:
          type: ["integer", "null"]
        score:
          type: integer
        level:
          type: string
        recommendation:
          type: string
        odd:
          type: number

    SetHistoryResultBody:
      type: object
      required: [result]
      properties:
        result:
          type: string

    DashboardSummary:
      type: object
      required: [totalFixturesToday, hotGames, trapAlerts, topLeagues]
      properties:
        totalFixturesToday:
          type: integer
        hotGames:
          type: integer
        trapAlerts:
          type: integer
        topLeagues:
          type: array
          items:
            type: string
