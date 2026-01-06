# Proxmox MCP Server

[![Docker Image CI](https://github.com/olivier-mj/mcp_proxmox/actions/workflows/docker-publish.yml/badge.svg)](https://github.com/olivier-mj/mcp_proxmox/actions/workflows/docker-publish.yml)

**Manage your Proxmox VE infrastructure using AI.**
*Pilotez votre infrastructure Proxmox VE grâce à l'IA.*

This MCP (Model Context Protocol) server allows LLMs (like Claude, Gemini, etc.) to securely monitor and control your Proxmox nodes, VMs, and containers.

## 🌟 Features

- 📊 **Monitoring**: View nodes (CPU/RAM), VMs, containers (LXC), storage status, and internal IPs (via Agent).
- ⚡ **Management**: Start, stop (graceful/forced), reboot, and **Clone** (Provisioning) machines.
- 🏗️ **Orchestration**: **Migrate** machines (live or offline) between nodes in a cluster.
- 📈 **Analytics**: View **Historical Performance** (CPU/RAM RRD data) for diagnostics.
- 📚 **Library**: Manage **LXC Templates** and **ISOs** (Download/List).
- 🏷️ **Organization**: Manage machine **Tags**.
- 🛠️ **DevOps**: Configure **Cloud-Init** (User/SSH/IP), **Resize** resources (CPU/RAM Hotplug), and **Download ISOs**.
- 🛡️ **Security**: Audit and manage **Firewall** rules per VM/Container.
- 🛡️ **Protection**: Manage **Snapshots** and **Backups** directly via MCP.
- 🔗 **Access**: Generate direct links to the **NoVNC Console**.
- 🔒 **Secure**: Uses Proxmox API Tokens. **Machine deletion is disabled** for safety.
- 🐳 **Docker-ready**: Works instantly with `docker run`.

## 🛠️ Tool Reference

### 📊 Monitoring & Diagnostics
| Tool | Description |
|---|---|
| `list_infrastructure` | Shows node status (CPU, RAM, Online/Offline). |
| `list_machines` | Lists VMs and Containers (Filters: name, status, type). |
| `get_machine_config` | Shows detailed config (Cores, Memory, Disks). |
| `list_storage` | Shows storage usage (Used/Free). |
| `get_vm_agent_network` | Retrieves internal IPs via QEMU Agent. |
| `get_cluster_logs` | (V6) Shows global cluster error logs. |
| `get_machine_performance_history` | (V7) Retrieves RRD history (CPU/RAM trends). |

### ⚡ Control & Actions
| Tool | Description |
|---|---|
| `start_machine` | Starts a VM or Container. |
| `stop_machine` | Stops (Graceful Shutdown or Forced Stop) a machine. |
| `reboot_machine` | Reboots a machine. |
| `get_console_url` | Generates a direct link to the NoVNC console. |
| `resize_resources` | (V4) Adjusts CPU or RAM (Hotplug if supported). |
| `unlock_machine` | (V6) Unlocks a machine (removes lock file). |
| `set_machine_tags` | (V7) Sets tags (e.g., "prod,db"). |

### 🏗️ Provisioning & DevOps
| Tool | Description |
|---|---|
| `clone_machine` | Clones a machine (Template) to a new ID. |
| `set_cloudinit_config` | (V4) Configures User, Password, SSH, IP via Cloud-Init. |
| `list_isos` | Lists available ISO files. |
| `download_iso` | (V4) Downloads an ISO from a URL. |
| `list_available_lxc_templates` | (V7) Lists system templates (Alpine, Ubuntu...). |
| `download_lxc_template` | (V7) Downloads an LXC template. |

### 🛡️ Security & Protection
| Tool | Description |
|---|---|
| `list_snapshots` | Lists restore points. |
| `create_snapshot` | Creates an instant snapshot. |
| `rollback_snapshot` | Restores a snapshot. |
| `delete_snapshot` | (V6) Deletes a snapshot to free space. |
| `list_backups` | Lists full backups (vzdump). |
| `create_backup` | Starts a full backup. |
| `list_firewall_rules` | (V5) Lists firewall rules. |
| `add_firewall_rule` | (V5) Adds a rule (ACCEPT/DROP) to the firewall. |

### 🏗️ Orchestration (Cluster)
| Tool | Description |
|---|---|
| `migrate_machine` | (V5) Moves a machine to another node (Live/Offline). |

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
