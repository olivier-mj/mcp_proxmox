# Plan de Développement Global (V1 -> V3)

Ce document retrace l'historique du développement et définit la feuille de route.

---

# ✅ V1 : Fondation Stable (Terminé)
- [x] Client API Proxmox & Auth Token.
- [x] Outils de base : Start, Stop, Reboot, List Infrastructure/Machines/Storage.
- [x] Dockerisation & CI/CD (Docker Hub).

# ✅ V2 : Robustesse & Observabilité (Terminé)
- [x] Validation Pydantic (IDs, Types).
- [x] Check Nœud Offline.
- [x] Logging centralisé.
- [x] Documentation Code & Readmes multilingues.

---

# ✅ V3 : Assistant SysAdmin (Terminé)

L'objectif de la V3 est de passer de la gestion passive au déploiement actif et au diagnostic.

## 1. 🏗️ Provisioning (Clonage)
- [x] Ajouter `clone_machine(vmid, newid, name, target_node)` dans `src/client.py`.
- [x] Exposer l'outil MCP `clone_machine`.
- [x] Test de simulation validé.

## 2. 🕵️‍♂️ Diagnostic Avancé (Logs Agent)
- [x] Ajouter `get_vm_agent_network` (IPs).
- [x] Ajouter `exec_agent_command` (pour lire des logs, optionnel/sécurisé).

## 3. 🛡️ Gestion des Backups
- [x] Gérer les sauvegardes complètes (dump).
- [x] Outils : `list_backups`, `create_backup`.

## 4. 🔗 Console VNC
- [x] Générer un lien d'accès rapide pour l'humain.
- [x] Outil : `get_console_url(vmid)`.

---

## Statut Actuel
- **Branche :** `dev` -> Prêt à être mergé dans `main` (V3 Release).
- **État :** V3 Complète.
