# Proxmox MCP Server

[![Docker Image CI](https://github.com/olivier-mj/mcp_proxmox/actions/workflows/docker-publish.yml/badge.svg)](https://github.com/olivier-mj/mcp_proxmox/actions/workflows/docker-publish.yml)

A Python-based **Model Context Protocol (MCP)** server to manage and monitor your Proxmox VE infrastructure via AI clients like Claude Desktop, Cursor, Windsurf, or Gemini-CLI.

🔗 **GitHub Repository:** [olivier-mj/mcp_proxmox](https://github.com/olivier-mj/mcp_proxmox)

---

## 🌟 Features

- 📊 **Monitoring**: View nodes (CPU/RAM), VMs, containers (LXC), storage status, and internal IPs (via Agent).
- ⚡ **Management**: Start, stop (graceful/forced), reboot, and **Clone** (Provisioning) machines.
- 🏗️ **Orchestration**: **Migrate** machines (live or offline) between nodes in a cluster.
- 📈 **Analytics**: View **Historical Performance** (CPU/RAM RRD data).
- 🛠️ **DevOps**: Configure **Cloud-Init**, **Resize** resources, and **Download ISOs/Templates**.
- 🛡️ **Security**: Audit and manage **Firewall** rules per machine.
- 🛡️ **Protection**: Manage **Snapshots** and **Backups** directly via AI.
- 🔗 **Access**: Generate direct links to the **NoVNC Console**.
- 🔒 **Secure**: Uses Proxmox API Tokens. **Machine deletion is disabled** for safety.
- 🐳 **Docker-ready**: Works instantly with `docker run`.

## 🛠️ Tool Reference

| Category | Tools |
|---|---|
| **Monitoring** | `list_infrastructure`, `list_machines`, `get_machine_config`, `list_storage`, `get_vm_agent_network`, `get_cluster_logs`, `get_machine_performance_history` |
| **Control** | `start_machine`, `stop_machine`, `reboot_machine`, `get_console_url`, `resize_resources`, `unlock_machine`, `set_machine_tags` |
| **Provisioning** | `clone_machine`, `set_cloudinit_config`, `list_isos`, `download_iso`, `list_available_lxc_templates`, `download_lxc_template` |
| **Protection** | `list_snapshots`, `create_snapshot`, `rollback_snapshot`, `delete_snapshot`, `list_backups`, `create_backup`, `list_firewall_rules`, `add_firewall_rule` |
| **Cluster** | `migrate_machine` |

## 🔑 Proxmox API Token Creation

1. Go to **Datacenter > Permissions > API Tokens** in Proxmox.
2. Click **Add**, select user (root@pam), and set an ID (e.g., `mcp`).
3. **Uncheck** "Privilege Separation".
4. Copy the Token ID and Secret.

## 🚀 Quick Start (Claude / Gemini-CLI / Windsurf)

Add this to your MCP configuration file:

```json
{
  "mcpServers": {
    "proxmox": {
      "command": "docker",
      "args": [
        "run",
        "-i",
        "--rm",
        "-e", "PROXMOX_URL=https://YOUR_PROXMOX_IP:8006",
        "-e", "PROXMOX_USER=root@pam",
        "-e", "PROXMOX_TOKEN_ID=your_token_name",
        "-e", "PROXMOX_TOKEN_SECRET=your_token_secret",
        "-e", "PROXMOX_VERIFY_SSL=false",
        "oliviermj/mcp_proxmox:latest"
      ]
    }
  }
}
```

## ⚙️ Environment Variables

| Variable | Description | Example |
|---|---|---|
| `PROXMOX_URL` | URL of your Proxmox server | `https://192.168.1.10:8006` |
| `PROXMOX_USER` | User (usually root@pam) | `root@pam` |
| `PROXMOX_TOKEN_ID` | API Token Name **(just the name)** | `mcp_token` |
| `PROXMOX_TOKEN_SECRET` | API Token Secret | `xxxxxxxx-xxxx-xxxx...` |
| `PROXMOX_VERIFY_SSL` | Verify SSL Certificate | `false` (for self-signed) |

---

## 🇫🇷 Version Française

Ce serveur MCP permet à une IA de piloter votre infrastructure Proxmox (Monitoring, Start/Stop, Clone, Snapshot, Backup, Migration) de manière sécurisée.

**Points forts :**
- Gestion complète : VMs, Containers, Stockage, Réseau.
- Sécurisé : Utilise des tokens API, suppression de machines désactivée.
- Prêt pour Docker : Utilisation immédiate via `docker run`.

**Configuration rapide :**
Utilisez le bloc JSON ci-dessus dans vos réglages d'IA (Claude, Cursor, etc.) en remplaçant les variables d'environnement par vos accès Proxmox.