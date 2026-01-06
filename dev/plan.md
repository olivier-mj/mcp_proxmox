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

# ✅ V4 : DevOps & Personnalisation (Terminé)

L'objectif de la V4 est de permettre une configuration fine des machines après clonage et de gérer les ressources dynamiquement.

## 1. ☁️ Support Cloud-Init
- [x] Ajouter `set_cloudinit_config` dans `src/client.py` (User, Password, SSH Keys, IP).
- [x] Exposer l'outil MCP correspondant.
- [x] Test de validation validé.

## 2. ⚡ Redimensionnement (Hotplug)
- [x] Ajouter `resize_resources(vmid, cpu, memory)` dans `src/client.py`.
- [x] Exposer l'outil MCP pour ajuster CPU/RAM à chaud (si OS compatible) ou à froid.
- [x] *But :* Adapter les ressources selon la charge observée.

## 3. 💿 Gestion des ISOs
- [x] Ajouter `download_iso(url, storage, filename)` dans `src/client.py`.
- [x] Outil : `list_isos(storage)`.
- [x] *But :* Rendre l'IA autonome pour récupérer de nouveaux OS.

---

# ✅ V5 : Sécurité & Orchestration (Terminé)

L'objectif de la V5 est de donner à l'IA les moyens de protéger le réseau et d'équilibrer la charge du cluster.

## 1. 🔥 Gestion du Firewall
- [x] Ajouter `get_firewall_rules(vmid)` et `add_firewall_rule(...)` dans `src/client.py`.
- [x] Exposer les outils MCP correspondants.
- [x] Test de validation validé.

## 2. 🏗️ Migration (HA)
- [x] Ajouter `migrate_machine(vmid, target_node, online)` dans `src/client.py`.
- [x] Exposer l'outil MCP.
- [x] Test de validation validé.

---

# ✅ V6 : Maintenance & Nettoyage (Terminé)

L'objectif de la V6 est d'automatiser les tâches de "Janitor" (nettoyage) et de résolution d'incidents mineurs.

## 1. ♻️ Gestion des Snapshots (Suppression)
- [x] Ajouter `delete_snapshot(vmid, snapname)`.
- [x] Exposer l'outil MCP correspondant.
- [x] Test de validation validé.

## 2. 🚑 Réparation (Unlock)
- [x] Ajouter `unlock_machine(vmid)`.
- [x] Exposer l'outil MCP correspondant.
- [x] Test de validation validé.

## 3. 📜 Logs Cluster
- [x] Ajouter `get_cluster_log(max_lines)`.
- [x] Exposer l'outil MCP `get_cluster_logs`.
- [x] Test de validation validé.

---

# 📈 V7 : Analyste & Libraire (Futur)

L'objectif de la V7 est de donner à l'IA une vision historique (performances) et une autonomie complète sur les conteneurs LXC.

## 1. 📊 Données Historiques (RRD)
- [ ] Ajouter `get_machine_performance_history(vmid, timeframe)`.
- [ ] *But :* Analyser les tendances (CPU/RAM) pour diagnostiquer des crashs passés.

## 2. 📦 Gestion des Templates LXC
- [ ] Ajouter `list_lxc_templates()` et `download_lxc_template()`.
- [ ] *But :* Permettre le déploiement instantané de conteneurs légers (Alpine, Debian, Apps TurnKey).

## 3. 🏷️ Gestion des Tags
- [ ] Ajouter `set_machine_tags(vmid, tags)`.
- [ ] *But :* Organiser le parc (ex: "prod", "test", "webserver") pour faciliter les recherches de l'IA.

---

## Statut Actuel
- **Branche :** `feature/v6-maintenance` (Contient V4 + V5 + V6).
- **Prochaine étape :** Release V6 -> Début V7.
