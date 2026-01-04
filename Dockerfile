# Utiliser une image Python légère
FROM python:3.11-slim

# Définir le répertoire de travail
WORKDIR /app

# Installer les dépendances système si nécessaire (ex: build-essential pour certains packages python)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copier le fichier des dépendances
COPY requirements.txt .

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code source
COPY src/ ./src/

# Définir les variables d'environnement par défaut (peuvent être surchargées par docker-compose ou -e)
ENV PYTHONUNBUFFERED=1

# Commande pour lancer le serveur MCP
# On utilise 'python -m src.server' si on veut lancer comme un module ou direct
CMD ["python", "-m", "src.server"]
