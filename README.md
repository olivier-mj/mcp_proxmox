# Proxmox MCP Server

[![Docker Image CI](https://github.com/olivier-mj/mcp_proxmox/actions/workflows/docker-publish.yml/badge.svg)](https://github.com/olivier-mj/mcp_proxmox/actions/workflows/docker-publish.yml)

**Manage your Proxmox VE infrastructure using AI.**
*Pilotez votre infrastructure Proxmox VE grâce à l'IA.*

This MCP (Model Context Protocol) server allows LLMs (like Claude, Gemini, etc.) to securely monitor and control your Proxmox nodes, VMs, and containers.

## 🌟 Features

- 📊 **Monitoring**: View nodes (CPU/RAM), VMs, containers (LXC), storage status, and internal IPs (via Agent).
- ⚡ **Management**: Start, stop (graceful/forced), reboot, and **Clone** (Provisioning) machines.
- 🛡️ **Protection**: Manage **Snapshots** and **Backups** directly via MCP.
- 🔗 **Access**: Generate direct links to the **NoVNC Console**.
- 🔒 **Secure**: Uses Proxmox API Tokens. **Machine deletion is disabled** for safety.
- 🐳 **Docker-ready**: Works instantly with `docker run`.

## 📚 Documentation

Please select your language / Veuillez choisir votre langue :

*   [🇫🇷 **Documentation en Français**](docs/README_fr.md)
*   [🇺🇸 **English Documentation**](docs/README_en.md)

## 🔑 Proxmox API Token

To use this server, you need a Proxmox API Token.
*Pour utiliser ce serveur, vous avez besoin d'un Token API Proxmox.*

1.  **Datacenter > Permissions > API Tokens** > **Add**.
2.  Select user, set ID (e.g., `mcp`), and **uncheck** "Privilege Separation".
3.  Copy the Token ID and Secret.

## ⚙️ Environment Variables

| Variable | Description | Example |
|---|---|---|
| `PROXMOX_URL` | URL of your Proxmox server | `https://192.168.1.10:8006` |
| `PROXMOX_USER` | User (usually root@pam) | `root@pam` |
| `PROXMOX_TOKEN_ID` | API Token Name **(just the name)** | `mcp_token` |
| `PROXMOX_TOKEN_SECRET` | API Token Secret | `xxxxxxxx-xxxx-xxxx...` |
| `PROXMOX_VERIFY_SSL` | Verify SSL Certificate | `false` (for self-signed) |

## 🚀 Quick Start (Docker)

1.  Clone this repo.
2.  Copy `.env.example` to `.env` and fill in your Proxmox credentials.
3.  Run:
    ```bash
    docker-compose up -d --build
    ```
4.  Configure your MCP client (Claude Desktop, Cursor, Gemini-CLI) to use the Docker container.

*(See detailed instructions in the links above)*

## 📦 Project Structure

```text
mcp_proxmox/
├── docs/               # Documentation (FR/EN)
├── src/                # Python Source Code
├── .env.example        # Configuration Template
├── Dockerfile          # Docker Configuration
└── docker-compose.yml  # Docker Compose Configuration
```
