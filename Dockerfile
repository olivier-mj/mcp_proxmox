# Utiliser une image Python récente et sécurisée (Debian Bookworm)
FROM python:3.12-slim-bookworm

# Définir le répertoire de travail
WORKDIR /app

# Mettre à jour les paquets système pour corriger les CVEs
# Fix: apt-get upgrade aide à résoudre les vulnérabilités système connues
RUN apt-get update && apt-get upgrade -y && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Créer un utilisateur non-root pour la sécurité
RUN useradd -m -u 1000 appuser

# Copier le fichier des dépendances
COPY requirements.txt .

# Installer les dépendances Python
# Fix: upgrade pip résout la CVE-2025-8869 (MEDIUM)
# Fix: urllib3 est mis à jour dans requirements.txt pour la CVE-2026-21441 (HIGH)
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copier le code source
COPY src/ ./src/

# Créer le répertoire de logs
RUN mkdir -p /app/logs && chown -R appuser:appuser /app

# Basculer sur l'utilisateur non-root
USER appuser

# Définir les variables d'environnement par défaut
ENV PYTHONUNBUFFERED=1

# Commande pour lancer le serveur MCP
CMD ["python", "-m", "src.server"]
