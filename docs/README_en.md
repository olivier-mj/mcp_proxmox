# Proxmox MCP Server (EN Documentation)

A Python-based Model Context Protocol (MCP) server to manage and monitor your Proxmox VE infrastructure via AI.

## Features

*   **Monitoring**:
    *   List nodes (CPU/RAM usage).
    *   Filterable list of VMs and Containers (LXC).
    *   Detailed machine configuration (CPU, RAM, Disks).
    *   **Advanced Diagnostic**: Retrieve IPs and network info via QEMU Agent.
    *   Storage status (local, ceph, nfs...).
*   **Management**:
    *   Start, Stop, Reboot machine.
    *   **Console**: Generate direct NoVNC console links.
    *   **Provisioning**: Clone machines (Templates) to new VMs/CTs.
    *   **Snapshots**: List, create, and restore snapshots.
    *   **Backups**: List and create full backups (vzdump).
    *   **Orchestration**: Migrate machines live or offline between nodes.
    *   **Analytics**: View historical performance (RRD Data).
    *   **DevOps**: Cloud-Init configuration, resource resizing, and ISO/LXC template management.
*   **Security**:
    *   Authentication via API Token (recommended).
    *   **No deletion**: Deleting machines is disabled for safety.
    *   Isolated execution via Docker.
    *   **Firewall Management**: Audit and manage rules per machine.

## 🛠️ Tool Reference

### 📊 Monitoring & Diagnostics
| Tool | Description |
|---|---|
| `list_infrastructure` | Shows node status (CPU, RAM, Online/Offline). |
| `list_machines` | Lists VMs and Containers (Filters: name, status, type). |
| `get_machine_config` | Shows detailed config (Cores, Memory, Disks). |
| `list_storage` | Shows storage usage (Used/Free). |
| `get_vm_agent_network` | Retrieves internal IPs via QEMU Agent. |
| `get_cluster_logs` | Shows global cluster error logs. |
| `get_machine_performance_history` | Retrieves RRD history (CPU/RAM trends). |

### ⚡ Control & Actions
| Tool | Description |
|---|---|
| `start_machine` | Starts a VM or Container. |
| `stop_machine` | Stops (Graceful Shutdown or Forced Stop) a machine. |
| `reboot_machine` | Reboots a machine. |
| `get_console_url` | Generates a direct link to the NoVNC console. |
| `resize_resources` | Adjusts CPU or RAM (Hotplug if supported). |
| `unlock_machine` | Unlocks a machine (removes lock file). |
| `set_machine_tags` | Sets tags (e.g., "prod,db"). |

### 🏗️ Provisioning & DevOps
| Tool | Description |
|---|---|
| `clone_machine` | Clones a machine (Template) to a new ID. |
| `set_cloudinit_config` | Configures User, Password, SSH, IP via Cloud-Init. |
| `list_isos` | Lists available ISO files. |
| `download_iso` | Downloads an ISO from a URL. |
| `list_available_lxc_templates` | Lists system templates (Alpine, Ubuntu...). |
| `download_lxc_template` | Downloads an LXC template. |

### 🛡️ Security & Protection
| Tool | Description |
|---|---|
| `list_snapshots` | Lists restore points. |
| `create_snapshot` | Creates an instant snapshot. |
| `rollback_snapshot` | Restores a snapshot. |
| `delete_snapshot` | Deletes a snapshot to free space. |
| `list_backups` | Lists full backups (vzdump). |
| `create_backup` | Starts a full backup. |
| `list_firewall_rules` | Lists firewall rules. |
| `add_firewall_rule` | Adds a rule (ACCEPT/DROP) to the firewall. |

### 🏗️ Orchestration (Cluster)
| Tool | Description |
|---|---|
| `migrate_machine` | Moves a machine to another node (Live/Offline). |

## Proxmox Preparation (API Token Creation)

To allow the AI to access your server, you need to create an API Token:

1.  Log in to your Proxmox web interface.
2.  Go to **Datacenter** > **Permissions** > **API Tokens**.
3.  Click **Add**.
4.  Select your user (e.g., `root@pam`) and give the token an ID (e.g., `mcp`).
5.  **Important**: Uncheck "Privilege Separation" for simplicity, or ensure the token has appropriate permissions (PVEVMAdmin, PVEAuditor).
6.  Copy the **Token ID** (e.g., `mcp`) and the **Secret** (only shown once).

## Prerequisites

*   Accessible Proxmox VE server.
*   Docker & Docker Compose installed locally.
*   Compatible MCP Client (Claude Desktop, Cursor, Gemini-CLI, etc.).

## Installation

### 1. Secrets Configuration

Create a `.env` file at the root of the project:

```env
PROXMOX_URL=https://192.168.1.100:8006
PROXMOX_USER=root@pam
PROXMOX_TOKEN_ID=mcp_token       # Just the token name (NOT root@pam!mcp_token)
PROXMOX_TOKEN_SECRET=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
PROXMOX_VERIFY_SSL=false         # false if using self-signed certificate
```

### 2. Start (Docker)

Using Docker is recommended for isolation.

```bash
docker-compose up -d --build
```

## Integrations

### Using Docker Image

You can build the image locally (`docker build -t mcp-proxmox-image .`) or use the official image published on **Docker Hub**: `oliviermj/mcp_proxmox:latest`.

### Claude Desktop / Gemini-CLI / Windsurf

These clients use a similar JSON structure. Add the configuration to your respective file:
- **Claude**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Gemini-CLI**: `~/.gemini/settings.json`
- **Windsurf**: `~/.codeium/windsurf/mcp_config.json`

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
        "/absolute/path/to/your/folder/mcp_proxmox/.env",
        "mcp-proxmox-image"
      ]
    }
  }
}
```

### Alternative: Direct Configuration (No .env file)

If you prefer not to manage a `.env` file, you can pass environment variables directly in the JSON configuration. Be aware that your secrets will be visible in this file.

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
        "-e", "PROXMOX_TOKEN_SECRET=your_secret_here",
        "-e", "PROXMOX_VERIFY_SSL=false",
        "mcp-proxmox-image"
      ]
    }
  }
}
```

### Cursor (IDE)

1.  Go to **Cursor Settings** > **Features** > **MCP**.
2.  Click on **+ Add New MCP Server**.
3.  Fill in the details:
    *   **Name**: `proxmox`
    *   **Type**: `command`
    *   **Command**: `docker run -i --rm --env-file /absolute/path/to/your/folder/mcp_proxmox/.env mcp-proxmox-image`

## Local Development (No Docker)

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m src.server
```
