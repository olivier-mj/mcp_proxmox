# Proxmox MCP Server (Documentation FR)

Un serveur MCP (Model Context Protocol) en Python pour piloter et surveiller votre infrastructure Proxmox VE via une IA.

## Fonctionnalités

*   **Surveillance** :
    *   Liste des nœuds (CPU/RAM).
    *   Liste filtrable des VMs et Containers (LXC).
    *   Configuration détaillée des machines (CPU, RAM, Disques).
    *   **Diagnostic Avancé** : Récupération des IPs et infos réseau via l'agent QEMU.
    *   État des espaces de stockage (local, ceph, nfs...).
*   **Pilotage** :
    *   Démarrer, Arrêter, Redémarrer.
    *   **Console** : Génération de liens directs vers la console NoVNC.
    *   **Provisioning** : Clonage de machines (Templates) vers de nouvelles VMs/CTs.
    *   **Configuration DevOps (Cloud-Init)** : Configuration post-déploiement (User, Password, SSH, IP).
    *   **Orchestration (V5)** : Migration de machines à chaud (online) ou à froid entre nœuds.
    *   **Sécurité & Firewall** : Audit et gestion des règles de pare-feu par machine.
    *   **ISOs** : Téléchargement d'ISOs depuis une URL et listage des images disponibles.
    *   **Snapshots** : Liste, création et restauration de snapshots.
    *   **Backups** : Liste et création de sauvegardes complètes (vzdump).
    *   **Ressources (Hotplug)** : Ajustement dynamique des CPU et de la RAM (VM & LXC).
*   **Sécurité** :
    *   Authentification via API Token (recommandé).
    *   Aucune suppression de machine possible.
    *   Exécution isolée via Docker.

## Préparation de Proxmox (Création du Token)

Pour que l'IA puisse accéder à votre serveur, vous devez créer un Token API :

1.  Connectez-vous à votre interface Proxmox.
2.  Allez dans **Datacenter** > **Permissions** > **API Tokens**.
3.  Cliquez sur **Add**.
4.  Sélectionnez votre utilisateur (ex: `root@pam`) et donnez un ID au token (ex: `mcp`).
5.  **Important** : Décochez "Privilege Separation" pour plus de simplicité, ou assurez-vous que le token a les permissions nécessaires (PVEVMAdmin, PVEAuditor).
6.  Copiez le **Token ID** (ex: `mcp`) et le **Secret** qui s'affiche une seule fois.

## Prérequis

*   Un serveur Proxmox VE accessible.
*   Docker et Docker Compose installés sur votre machine locale.
*   Un client MCP compatible (Claude Desktop, Cursor, Gemini-CLI, etc.).

## Installation

### 1. Configuration des secrets

Créez un fichier `.env` à la racine du projet :

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

## Intégrations

### Utilisation de l'image Docker

Vous pouvez construire l'image localement (`docker build -t mcp-proxmox-image .`) ou utiliser l'image officielle publiée sur **Docker Hub** : `oliviermj/mcp_proxmox:latest`.

### Claude Desktop / Gemini-CLI / Windsurf

Ces clients utilisent une structure JSON similaire. Ajoutez la configuration à votre fichier respectif :
- **Claude** : `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Gemini-CLI** : `~/.gemini/settings.json`
- **Windsurf** : `~/.codeium/windsurf/mcp_config.json`

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

### Alternative : Configuration directe (Sans fichier .env)

Si vous ne souhaitez pas gérer de fichier `.env`, vous pouvez passer les variables directement dans la configuration JSON. Attention, vos secrets seront visibles dans ce fichier.

```json
{
  "mcpServers": {
    "proxmox": {
      "command": "docker",
      "args": [
        "run",
        "-i",
        "--rm",
        "-e", "PROXMOX_URL=https://192.168.1.100:8006",
        "-e", "PROXMOX_USER=root@pam",
        "-e", "PROXMOX_TOKEN_ID=mcp_token",
        "-e", "PROXMOX_TOKEN_SECRET=votre_secret_ici",
        "-e", "PROXMOX_VERIFY_SSL=false",
        "mcp-proxmox-image"
      ]
    }
  }
}
```

### Cursor (IDE)

1.  Allez dans **Cursor Settings** > **Features** > **MCP**.
2.  Cliquez sur **+ Add New MCP Server**.
3.  Remplissez les champs :
    *   **Name**: `proxmox`
    *   **Type**: `command`
    *   **Command**: `docker run -i --rm --env-file /chemin/absolu/vers/votre/dossier/mcp_proxmox/.env mcp-proxmox-image`

## Développement Local (Sans Docker)

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m src.server
```
