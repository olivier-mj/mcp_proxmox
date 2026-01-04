# Proxmox MCP Server

[![Docker Image CI](https://github.com/olivier-mj/mcp_proxmox/actions/workflows/docker-publish.yml/badge.svg)](https://github.com/olivier-mj/mcp_proxmox/actions/workflows/docker-publish.yml)

A Python-based **Model Context Protocol (MCP)** server to manage and monitor your Proxmox VE infrastructure via AI clients like Claude Desktop, Cursor, Windsurf, or Gemini-CLI.

🔗 **GitHub Repository:** [olivier-mj/mcp_proxmox](https://github.com/olivier-mj/mcp_proxmox)

---

## 🌟 Features

- 📊 **Monitoring**: View nodes (CPU/RAM), VMs, containers (LXC), and storage status.
- ⚡ **Management**: Start, stop (graceful/forced), and reboot machines.
- 🔒 **Secure**: Uses Proxmox API Tokens. **Machine deletion is disabled** for safety.
- 🐳 **Docker-ready**: Works instantly with `docker run`.

## 🔑 Proxmox API Token Creation

1. Go to **Datacenter > Permissions > API Tokens** in Proxmox.
2. Click **Add**, select user (root@pam), and set an ID (e.g., `mcp`).
3. **Uncheck** "Privilege Separation".
4. Copy the Token ID and Secret for the configuration below.

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
        "-e", "PROXMOX_URL=https://192.168.1.100:8006",
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

Ce serveur MCP permet à une IA de piloter votre serveur Proxmox (Start/Stop/Reboot/Monitoring) de manière sécurisée via le protocole MCP.

**Création du Token Proxmox :**
1. Allez dans **Datacenter > Permissions > API Tokens**.
2. Cliquez sur **Add**, choisissez l'utilisateur et un ID (ex: `mcp`).
3. **Décochez** "Privilege Separation".
4. Utilisez l'ID et le Secret dans la config ci-dessus.

**Utilisation rapide :**
Utilisez la configuration JSON ci-dessus dans vos réglages d'IA (Claude, Cursor, etc.) en remplaçant les valeurs par vos propres identifiants Proxmox.
