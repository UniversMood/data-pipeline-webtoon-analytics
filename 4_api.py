from fastapi import FastAPI
import duckdb
import sqlite3
from datetime import datetime

# --- 1. Configuration de FastAPI ---
app = FastAPI(title="Webtoon Analytics API")

# --- 2. Connexion à DuckDB (pour lire le CSV) ---
con_duck = duckdb.connect()

# --- 3. Connexion à SQLite (pour l'historique) ---
# check_same_thread=False est important pour FastAPI (car il gère plusieurs requêtes en parallèle)
conn_sqlite = sqlite3.connect('history.db', check_same_thread=False)
cursor = conn_sqlite.cursor()

# Création de la table d'historique si elle n'existe pas
cursor.execute("""
    CREATE TABLE IF NOT EXISTS api_calls (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        endpoint TEXT,
        timestamp TEXT
    )
""")
conn_sqlite.commit()

# --- 4. Fonction utilitaire pour enregistrer les appels ---
def log_call(endpoint_name: str):
    now = datetime.now().isoformat()  # Exemple : "2026-08-25T14:35:22"
    cursor.execute("INSERT INTO api_calls (endpoint, timestamp) VALUES (?, ?)", (endpoint_name, now))
    conn_sqlite.commit()
    print(f"📝 Historique : {endpoint_name} appelé à {now}")  # Pour voir en direct dans le terminal

# --- 5. Les routes (Endpoints) ---

@app.get("/")
def read_root():
    return {"message": "Bienvenue sur l'API Webtoon. Va sur /top10, /genres ou /trends"}

@app.get("/top10")
def get_top10():
    log_call("top10")  # J'enregistre l'appel !
    df = con_duck.execute("""
        SELECT title, score 
        FROM 'anime_clean.csv' 
        WHERE score > 0
        ORDER BY score DESC 
        LIMIT 10
    """).fetchdf()
    return df.to_dict(orient='records')

@app.get("/genres")
def get_genres():
    log_call("genres")  # J'enregistre l'appel !
    df = con_duck.execute("""
        SELECT main_genre, COUNT(*) as nombre 
        FROM 'anime_clean.csv' 
        GROUP BY main_genre 
        ORDER BY nombre DESC
    """).fetchdf()
    return df.to_dict(orient='records')

@app.get("/trends")
def get_trends():
    log_call("trends")  # J'enregistre l'appel !
    df = con_duck.execute("""
        SELECT year, COUNT(*) as nombre 
        FROM 'anime_clean.csv' 
        WHERE year IS NOT NULL
        GROUP BY year 
        ORDER BY year
    """).fetchdf()
    return df.to_dict(orient='records')

# --- 6. NOUVEAU : Route pour consulter l'historique ---
@app.get("/history")
def get_history():
    cursor.execute("SELECT * FROM api_calls ORDER BY timestamp DESC LIMIT 50")
    rows = cursor.fetchall()
    # On transforme les lignes en liste de dictionnaires pour que FastAPI les transforme en JSON
    return [{"id": r[0], "endpoint": r[1], "timestamp": r[2]} for r in rows]