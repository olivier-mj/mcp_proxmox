# Proxmox MCP Server

Un serveur MCP (Model Context Protocol) en Python pour piloter et surveiller votre infrastructure Proxmox VE via une IA (comme Claude Desktop).

*(English version below)*

## 🇫🇷 Français

### Fonctionnalités

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

### Prérequis

*   Un serveur Proxmox VE accessible.
*   Docker et Docker Compose installés sur votre machine locale.
*   Un client MCP (ex: Claude Desktop).

### Installation

#### 1. Configuration des secrets

Créez un fichier `.env` à la racine :

```env
PROXMOX_URL=https://192.168.1.100:8006
PROXMOX_USER=root@pam
PROXMOX_TOKEN_ID=mcp_token       # Juste le nom du token (pas root@pam!mcp_token)
PROXMOX_TOKEN_SECRET=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
PROXMOX_VERIFY_SSL=false         # false si certificat auto-signé
```

#### 2. Démarrage (Docker)

La méthode recommandée est d'utiliser Docker pour une isolation totale.

```bash
docker-compose up -d --build
```

#### 3. Intégration à Claude Desktop

Ajoutez la configuration suivante à votre fichier de configuration Claude.

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

*Attention : Construire l'image d'abord :* `docker build -t mcp-proxmox-image .`

---

## 🇺🇸 English

### Features

*   **Monitoring**:
    *   List nodes (CPU/RAM usage).
    *   List VMs and Containers (LXC) with their status.
    *   Storage status (local, ceph, nfs...).
*   **Management**:
    *   Start machine.
    *   Stop machine (Graceful shutdown or Forced stop).
    *   Reboot machine.
*   **Security**:
    *   Authentication via API Token (recommended).
    *   **No deletion**: Deleting machines is disabled for safety.
    *   Isolated execution via Docker.

### Prerequisites

*   Accessible Proxmox VE server.
*   Docker & Docker Compose installed locally.
*   MCP Client (e.g., Claude Desktop).

### Installation

#### 1. Secrets Configuration

Create a `.env` file at the root:

```env
PROXMOX_URL=https://192.168.1.100:8006
PROXMOX_USER=root@pam
PROXMOX_TOKEN_ID=mcp_token       # Just the token name (NOT root@pam!mcp_token)
PROXMOX_TOKEN_SECRET=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
PROXMOX_VERIFY_SSL=false         # false if using self-signed certificate
```

#### 2. Start (Docker)

Using Docker is recommended for isolation.

```bash
docker-compose up -d --build
```

#### 3. Claude Desktop Integration

Add the following configuration to your Claude config file.

**Config file path (Mac/Linux):** `~/Library/Application Support/Claude/claude_desktop_config.json` or `~/.config/Claude/claude_desktop_config.json`

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
        "/absolute/path/to/your/folder/mcp_proxmox/.env",
        "mcp-proxmox-image"
      ]
    }
  }
}
```

*Note: Build the image first:* `docker build -t mcp-proxmox-image .`

## Project Structure

*   `src/client.py` : Proxmox API connection logic.
*   `src/server.py` : MCP tools definition.
*   `Dockerfile` : Docker image configuration.
