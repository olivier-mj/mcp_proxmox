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
    *   **Analyste (V7)** : Consultation de l'historique de performance (RRD Data - CPU/RAM).
    *   **Libraire (V7)** : Gestion des Templates LXC (Listage & Téléchargement).
    *   **Tags (V7)** : Organisation des machines par étiquettes.
    *   **ISOs** : Téléchargement d'ISOs depuis une URL et listage des images disponibles.
    *   **Snapshots** : Liste, création et restauration de snapshots.
    *   **Backups** : Liste et création de sauvegardes complètes (vzdump).
    *   **Ressources (Hotplug)** : Ajustement dynamique des CPU et de la RAM (VM & LXC).
*   **Sécurité** :
    *   Authentification via API Token (recommandé).
    *   Aucune suppression de machine possible.
    *   Exécution isolée via Docker.

## 🛠️ Référence Complète des Outils

### 📊 Surveillance & Diagnostic
| Outil | Description |
|---|---|
| `list_infrastructure` | Affiche l'état des nœuds (CPU, RAM, Statut). |
| `list_machines` | Liste les VMs et Containers (Filtres: nom, statut, type). |
| `get_machine_config` | Affiche la config détaillée (Cœurs, Mémoire, Disques). |
| `list_storage` | Affiche l'espace et les contenus (Filtre: `content_filter`). |
| `get_vm_agent_network` | Récupère les IPs internes via l'Agent QEMU. |
| `get_cluster_logs` | Affiche les logs d'erreurs globaux du cluster. |
| `get_machine_performance_history` | Affiche l'historique RRD (CPU/RAM) sur une période. |

### ⚡ Pilotage & Actions
| Outil | Description |
|---|---|
| `start_machine` | Démarre une VM ou un Conteneur. |
| `stop_machine` | Arrête (Shutdown propre ou Stop forcé) une machine. |
| `reboot_machine` | Redémarre une machine. |
| `get_console_url` | Génère un lien direct vers la console NoVNC. |
| `resize_resources` | Modifie le CPU ou la RAM (Hotplug si supporté). |
| `unlock_machine` | Débloque une machine figée (lock). |
| `set_machine_tags` | Applique des étiquettes (ex: "prod,db"). |

### 🏗️ Provisioning & DevOps
| Outil | Description |
|---|---|
| `clone_machine` | Clone une machine (Template) vers une nouvelle ID. |
| `set_cloudinit_config` | Configure User, Password, SSH, IP via Cloud-Init. |
| `list_isos` | Liste les fichiers ISO disponibles. |
| `download_iso` | Télécharge un ISO depuis une URL. |
| `list_available_lxc_templates` | Liste les templates système (Alpine, Ubuntu...). |
| `download_lxc_template` | Télécharge un template LXC. |

### 🛡️ Sécurité & Protection
| Outil | Description |
|---|---|
| `list_snapshots` | Liste les points de restauration. |
| `create_snapshot` | Crée un snapshot instantané. |
| `rollback_snapshot` | Revient à un état précédent. |
| `delete_snapshot` | Supprime un snapshot pour libérer de l'espace. |
| `list_backups` | Liste les sauvegardes complètes (vzdump). |
| `create_backup` | Lance une sauvegarde complète. |
| `list_firewall_rules` | Affiche les règles de pare-feu. |
| `add_firewall_rule` | Ajoute une règle (ACCEPT/DROP) au pare-feu. |

### 🏗️ Orchestration (Cluster)
| Outil | Description |
|---|---|
| `migrate_machine` | Déplace une machine vers un autre nœud (Live/Offline). |

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
