import pandas as pd
import ast

def clean_data():
    # 1. Charger le brut
    df = pd.read_csv('anime_raw.csv')
    
    # 2. Sélectionner les colonnes intéressantes
    df_clean = df[['title', 'score', 'aired', 'genres', 'episodes', 'members']].copy()
    
    # 3. Gérer les notes manquantes (NaN) -> on met 0
    df_clean['score'] = df_clean['score'].fillna(0)
    
    # 4. Extraire l'année de diffusion depuis la colonne 'aired'
    def extract_year(aired_str):
        try:
            if pd.isna(aired_str):
                return None
            aired_dict = ast.literal_eval(aired_str) 
            if 'from' in aired_dict and aired_dict['from']:
                return pd.to_datetime(aired_dict['from']).year
            return None
        except:
            return None
    
    df_clean['year'] = df_clean['aired'].apply(extract_year)
    
    # 5. Extraire le NOM du premier genre
    def extract_genre_name(genres_str):
        try:
            if pd.isna(genres_str):
                return 'Inconnu'
            genre_list = ast.literal_eval(genres_str)
            if genre_list and len(genre_list) > 0:
                return genre_list[0]['name']
            return 'Inconnu'
        except:
            return 'Inconnu'
    
    df_clean['main_genre'] = df_clean['genres'].apply(extract_genre_name)
    
    # 6. Enlever les doublons
    df_clean = df_clean.drop_duplicates(subset=['title'])
    
    # 7. Sauvegarder le fichier propre
    df_clean.to_csv('anime_clean.csv', index=False)
    print(f"✅ Nettoyage terminé ! {len(df_clean)} animes propres.")
    print(df_clean[['title', 'score', 'year', 'main_genre']].head())

if __name__ == "__main__":
    clean_data()