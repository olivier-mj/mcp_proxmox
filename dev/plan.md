# Plan de Développement Global (V1 + V2)

Ce document retrace l'historique du développement (V1) et définit la feuille de route pour la prochaine itération (V2).

---

# ✅ V1 : Fondation Stable (Terminé)

## 1. Prérequis et Configuration
- [x] Environnement Python (`.venv`, `requirements.txt`).
- [x] Configuration via `.env` (URL, Token ID, Secret, SSL).

## 2. Abstraction de l'API Proxmox (`src/client.py`)
- [x] Classe `ProxmoxClient` robuste.
- [x] Authentification par Token API.
- [x] Support des clusters et nœuds multiples.
- [x] Gestion de base : `get_nodes`, `get_all_machines`, `set_machine_state`.

## 3. Serveur MCP (`src/server.py`)
- [x] Outils exposés :
    - `list_infrastructure` (Status nœuds).
    - `list_machines` (VMs/LXCs).
    - `list_storage` (Usage disques).
    - `start_machine`, `stop_machine`, `reboot_machine`.
- [x] Documentation des outils (Docstrings).

## 4. Dockerisation & CI/CD
- [x] `Dockerfile` sécurisé (User non-root).
- [x] `docker-compose.yml` optimisé (TTY désactivé).
- [x] GitHub Actions : Build & Push auto sur Docker Hub (`oliviermj/mcp_proxmox`).

## 5. Fonctionnalités Avancées (v1.1)
- [x] Filtrage dans `list_machines` (par nom, status, type).
- [x] Gestion des Snapshots (`list`, `create`, `rollback`).
- [x] Inspection de configuration (`get_machine_config`).

---

# ✅ V2 : Robustesse & Observabilité (Terminé)

L'objectif de la V2 était de rendre le serveur plus "pro" et plus facile à déboguer en production.

## 1. Validation Stricte des Entrées (Pydantic/Typing)
- [x] Utilisation de `Literal['qemu', 'lxc']` pour contraindre les types.
- [x] Validation manuelle des IDs (`vmid >= 100`).

## 2. Gestion Intelligente Multi-nœuds
- [x] Vérification de l'état (`online`/`offline`) du nœud avant d'interroger ses VMs/Storage.

## 3. Logging Centralisé (Observabilité)
- [x] Configuration du module `logging` standard.
- [x] Logs informatifs pour chaque appel d'outil (avec arguments).
- [x] Logs d'erreurs pour les échecs API.

## 4. Documentation Code
- [x] Ajout de Docstrings complètes sur toutes les fonctions et classes.

---

## Statut Actuel
- **Branche :** `dev` -> Prêt à être mergé dans `main`.
- **État :** V2 Complète.
