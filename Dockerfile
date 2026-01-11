# Utiliser une image Python légère
FROM python:3.11-slim

# Définir le répertoire de travail
WORKDIR /app

# Installer les dépendances système si nécessaire (ex: build-essential pour certains packages python)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Créer un utilisateur non-root pour la sécurité
RUN useradd -m -u 1000 appuser

# Copier le fichier des dépendances
COPY requirements.txt .

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code source
COPY src/ ./src/

# Changer la propriété des fichiers pour l'utilisateur non-root
RUN chown -R appuser:appuser /app

# Basculer sur l'utilisateur non-root
USER appuser

# Définir les variables d'environnement par défaut
ENV PYTHONUNBUFFERED=1

# Expose the port for the REST API (LobeChat Plugin)
EXPOSE 8000

# Commande pour lancer le serveur MCP par défaut
CMD ["python", "-m", "src.server"]
