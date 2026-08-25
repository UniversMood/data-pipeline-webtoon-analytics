\# 🚀 Data Pipeline Webtoon Analytics (ETL / ELT)



\## 📖 À propos du projet



Ce projet est un pipeline de données complet, conçu pour collecter, analyser et exposer via une API REST les tendances des anime populaires. 



L'objectif était de simuler une architecture Data Engineering moderne en utilisant une approche \*\*serverless\*\* et \*\*zéro configuration\*\* : DuckDB analyse directement les fichiers CSV, FastAPI expose les résultats, et SQLite gère l'historique des requêtes.



\*\*Stack technique utilisée :\*\*

\- \*\*Extraction\*\* : `Requests` (API REST Jikan)

\- \*\*Transformation\*\* : `Pandas` (Nettoyage et normalisation)

\- \*\*Stockage / Analyse\*\* : `DuckDB` (ELT serverless, requêtes SQL directement sur les CSV)

\- \*\*API\*\* : `FastAPI` (Documentation Swagger automatique)

\- \*\*Historique\*\* : `SQLite` (Suivi des tendances d'appel)



\## 🗺️ Architecture du Pipeline



```mermaid

graph LR

&#x20;   A\[API Jikan] -->|Extraction| B\[(anime\_raw.csv)]

&#x20;   B -->|Nettoyage Pandas| C\[(anime\_clean.csv)]

&#x20;   C -->|Lecture directe DuckDB| D\[Analyse SQL]

&#x20;   D -->|REST API| E\[FastAPI Endpoints]

&#x20;   E -->|Logs| F\[(SQLite history.db)]

&#x20;   E -->|JSON| G\[Frontend / Client]

