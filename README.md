# Proxmox MCP Server

**Manage your Proxmox VE infrastructure using AI.**
*Pilotez votre infrastructure Proxmox VE grâce à l'IA.*

This MCP (Model Context Protocol) server allows LLMs (like Claude, Gemini, etc.) to securely monitor and control your Proxmox nodes, VMs, and containers.

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
