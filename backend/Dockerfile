# Dockerfile pour le backend FastAPI avec SQLite

# Utilisez une image Python officielle
FROM python:3.9-slim

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers nécessaires
COPY requirements.txt /app/
COPY . /app/

# Installer les dépendances Python
RUN apt-get update
RUN apt-get install sqlite3
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Exposer le port 8000 pour l'application FastAPI
EXPOSE 8000

# Ajouter une étape pour exécuter les migrations avant de démarrer le serveur
CMD ["sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000"]