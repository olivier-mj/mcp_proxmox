# Plan de Développement : Serveur MCP pour Proxmox (Python & Docker)

Ce document détaille les étapes pour créer un serveur MCP (Model Context Protocol) permettant de piloter et surveiller une infrastructure Proxmox VE (Cluster ou Nœud unique) via une IA.

## 1. Prérequis et Configuration

### Objectifs
- Préparer l'environnement de développement.
- Configurer l'authentification sécurisée (API Token).

### Actions
1.  **Créer un environnement virtuel (pour le dév local) :**
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```
2.  **Installer les dépendances :**
    ```bash
    pip install mcp proxmoxer requests python-dotenv
    ```
3.  **Configurer le fichier `.env` :**
    Utilisation de Tokens API pour la sécurité et gestion de la vérification SSL.
    
    ```env
    # URL de votre Proxmox (ex: https://192.168.1.10:8006)
    PROXMOX_URL=https://<IP>:<PORT>
    
    # Authentification via Token (recommandé)
    # Format User: root@pam
    PROXMOX_USER=root@pam
    # ID du token (ex: mcp-token)
    PROXMOX_TOKEN_ID=votre_token_id
    # Secret du token (ex: xxxxx-xxxx-xxxx-xxxx)
    PROXMOX_TOKEN_SECRET=votre_token_secret
    
    # Sécurité SSL
    # 'true' pour vérifier le certificat (prod), 'false' pour ignorer (self-signed)
    PROXMOX_VERIFY_SSL=false
    ```

## 2. Abstraction de l'API Proxmox (`src/client.py`)

### Objectifs
- Créer une classe robuste pour dialoguer avec l'API Proxmox.
- Gérer l'authentification par Token.
- Supporter le mode Cluster et Nœud unique.

### Fonctionnalités Client
1.  **Connexion :** Gestion du booléen `verify_ssl` et auth par Token.
2.  **Découverte (Cluster/Nodes) :**
    *   `get_nodes()` : Liste tous les nœuds disponibles (essentiel pour les clusters).
3.  **Gestion des Machines (VMs & LXC) :**
    *   `get_all_machines()` : Itère sur tous les nœuds pour lister VMs et Containers.
    *   `get_machine_status(node, vm_id)` : État détaillé.
    *   `set_machine_state(node, vm_id, action)` : Actions start, stop, shutdown, reboot.
4.  **Monitoring & Stockage :**
    *   `get_storage_status(node)` : Liste les espaces de stockage (local, ceph, nfs) et leur usage (espace libre/total).
    *   `get_node_resources(node)` : CPU/RAM du serveur physique.

## 3. Implémentation du Serveur MCP (`src/server.py`)

### Objectifs
- Exposer les fonctions Proxmox comme des outils IA sécurisés.
- **Exclusion stricte :** Aucune fonction de suppression (Delete) ne sera implémentée.

### Outils (Tools) Exposés
*   **`list_infrastructure`** : Vue d'ensemble (Nœuds, status CPU/RAM globaux).
*   **`list_machines`** : Liste toutes les VMs/LXC avec ID, Nom, Nœud, Status (running/stopped), et type (qemu/lxc).
*   **`list_storage`** : Affiche l'état des disques/stockages sur tous les nœuds (monitoring espace).
*   **`start_machine(vm_id, node)`** : Démarre une machine.
*   **`stop_machine(vm_id, node, force=False)`** : Arrête une machine (Shutdown propre par défaut, Stop forcé si demandé).
*   **`reboot_machine(vm_id, node)`** : Redémarre une machine.

## 4. Dockerisation

### Objectifs
- Isoler l'application pour un déploiement facile et propre.

### Actions
1.  **Créer un `Dockerfile` :**
    *   Image de base légère (ex: `python:3.11-slim`).
    *   Installation des dépendances.
    *   Copie du code source.
    *   Point d'entrée pour lancer le serveur MCP.
2.  **Créer un `docker-compose.yml` (Optionnel mais pratique) :**
    *   Montage du fichier `.env`.
    *   Configuration du réseau.

## 5. Tests et Validation

### Actions
1.  Test local (hors Docker) pour valider le code Python.
2.  Construction de l'image Docker.
3.  Test d'intégration : Lancer le conteneur et connecter un client MCP (Claude Desktop ou Inspector).

## 6. Structure de Fichiers Finale

```text
mcp_proxmox/
├── .env                # Configuration (Secrets)
├── .gitignore
├── requirements.txt
├── Dockerfile          # Configuration de l'image Docker
├── src/
│   ├── __init__.py
│   ├── client.py       # Logique Proxmox (Cluster, Auth Token, SSL)
│   └── server.py       # Serveur FastMCP
└── README.md
```