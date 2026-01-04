# Proxmox MCP Server

Un serveur MCP (Model Context Protocol) en Python pour piloter et surveiller votre infrastructure Proxmox VE via une IA (comme Claude Desktop).

## Fonctionnalités

*   **Surveillance** :
    *   Liste des nœuds (CPU/RAM).
    *   Liste des VMs et Containers (LXC) avec leur état.
    *   État des espaces de stockage (local, ceph, nfs...).
*   **Pilotage** :
    *   Démarrer (Start).
    *   Arrêter (Shutdown propre ou Stop forcé).
    *   Redémarrer (Reboot).
*   **Sécurité** :
    *   Authentification via API Token (recommandé).
    *   Aucune suppression de machine possible.
    *   Exécution isolée via Docker.

## Prérequis

*   Un serveur Proxmox VE accessible.
*   Docker et Docker Compose installés sur votre machine locale.
*   Un client MCP (ex: Claude Desktop).

## Installation

### 1. Configuration des secrets

Créez un fichier `.env` à la racine :

```env
PROXMOX_URL=https://192.168.1.100:8006
PROXMOX_USER=root@pam
PROXMOX_TOKEN_ID=mcp_token       # Juste le nom du token (pas root@pam!mcp_token)
PROXMOX_TOKEN_SECRET=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
PROXMOX_VERIFY_SSL=false         # false si certificat auto-signé
```

### 2. Démarrage (Docker)

La méthode recommandée est d'utiliser Docker pour une isolation totale.

```bash
docker-compose up -d --build
```

### 3. Intégration à Claude Desktop

Ajoutez la configuration suivante à votre fichier de configuration Claude (accessible via `Settings > Developer > Edit Config`).

> **Note :** Nous utilisons `docker run` directement pour que Claude lance le conteneur à la demande. Assurez-vous d'adapter le chemin vers votre fichier `.env`.

**Chemin du fichier config (Mac/Linux) :** `~/Library/Application Support/Claude/claude_desktop_config.json` ou `~/.config/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "proxmox": {
      "command": "docker",
      "args": [
        "run",
        "-i",
        "--rm",
        "--env-file",
        "/chemin/absolu/vers/votre/dossier/mcp_proxmox/.env",
        "mcp-proxmox-image"
      ]
    }
  }
}
```

*Attention : Il faut d'abord construire l'image manuellement si vous utilisez cette commande `docker run` :*
```bash
docker build -t mcp-proxmox-image .
```

Alternativement, si vous préférez lancer le script Python directement (sans Docker) :

```json
{
  "mcpServers": {
    "proxmox": {
      "command": "/chemin/vers/votre/dossier/.venv/bin/python",
      "args": ["-m", "src.server"],
      "env": {
        "PROXMOX_URL": "https://...",
        "PROXMOX_USER": "...",
        "PROXMOX_TOKEN_ID": "...",
        "PROXMOX_TOKEN_SECRET": "...",
        "PROXMOX_VERIFY_SSL": "false"
      }
    }
  }
}
```

## Développement Local

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m src.server
```

## Structure du Projet

*   `src/client.py` : Logique de connexion à l'API Proxmox.
*   `src/server.py` : Définition des outils MCP.
*   `Dockerfile` : Configuration de l'image Docker.
