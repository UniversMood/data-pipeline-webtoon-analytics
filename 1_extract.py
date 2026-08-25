import requests
import pandas as pd
import time

def fetch_top_anime():
    all_anime = []
    
    for page in range(1, 3):
        print(f"Téléchargement page {page}...")
        url = f"https://api.jikan.moe/v4/top/anime?page={page}"
        response = requests.get(url)
        
        # On vérifie d'abord si la requête a réussi (code 200)
        if response.status_code != 200:
            print(f"❌ Erreur HTTP {response.status_code} : {response.text}")
            return  # On arrête le programme ici
        
        data = response.json()
        
        # On vérifie que la clé 'data' est bien présente
        if 'data' not in data:
            print(f"❌ La clé 'data' est manquante. Réponse brute : {data}")
            return  # On arrête le programme ici
        
        # Ajout des animés
        for anime in data['data']:
            all_anime.append(anime)
        
        time.sleep(1.2)
    
    # Sauvegarde
    df = pd.DataFrame(all_anime)
    df.to_csv('anime_raw.csv', index=False)
    print(f"✅ {len(df)} anime téléchargés en brut !")

if __name__ == "__main__":
    fetch_top_anime()
