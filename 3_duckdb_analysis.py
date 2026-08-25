import duckdb

# On se connecte à DuckDB (en mémoire, zéro configuration)
con = duckdb.connect()

print("="*50)
print("🔍 ANALYSE DE TES ANIMES AVEC DUCKDB")
print("="*50)

# Requête 1 : Top 10 des notes (ici on a que 5, mais c'est pareil)
print("\n--- TOP 10 DES NOTES ---")
top_10 = con.execute("""
    SELECT title, score 
    FROM 'anime_clean.csv' 
    WHERE score > 0
    ORDER BY score DESC 
    LIMIT 10
""").fetchdf()
print(top_10.to_string(index=False))

# Requête 2 : Répartition par genre (combien d'animes par genre)
print("\n--- RÉPARTITION PAR GENRE ---")
genre_stats = con.execute("""
    SELECT main_genre, COUNT(*) as nombre 
    FROM 'anime_clean.csv' 
    GROUP BY main_genre 
    ORDER BY nombre DESC
""").fetchdf()
print(genre_stats.to_string(index=False))

# Requête 3 : Évolution temporelle (combien d'animes par année)
print("\n--- ÉVOLUTION TEMPORELLE (par année) ---")
trends = con.execute("""
    SELECT year, COUNT(*) as nombre 
    FROM 'anime_clean.csv' 
    WHERE year IS NOT NULL
    GROUP BY year 
    ORDER BY year
""").fetchdf()
print(trends.to_string(index=False))

con.close()
print("\n✅ Analyse DuckDB terminée !")