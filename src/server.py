import os
from mcp.server.fastmcp import FastMCP
from src.client import ProxmoxClient

# Initialisation du serveur MCP
mcp = FastMCP("Proxmox Manager")

# Initialisation du client Proxmox
try:
    proxmox = ProxmoxClient()
except Exception as e:
    print(f"Erreur d'initialisation du client Proxmox: {e}")
    proxmox = None

@mcp.tool()
def list_infrastructure():
    """Liste tous les nœuds du cluster Proxmox avec leur statut CPU et RAM."""
    if not proxmox: return "Client Proxmox non configuré."
    try:
        nodes = proxmox.get_nodes()
        result = "Infrastucture Proxmox :\n"
        for n in nodes:
            cpu = n.get('cpu', 0) * 100
            ram = (n.get('mem', 0) / n.get('maxmem', 1)) * 100
            status = n.get('status', 'unknown')
            result += f"- Nœud: {n['node']} | Statut: {status} | CPU: {cpu:.1f}% | RAM: {ram:.1f}%\n"
        return result
    except Exception as e:
        return f"Erreur lors de la récupération de l'infrastructure : {e}"

@mcp.tool()
def list_machines():
    """Liste toutes les VMs et Containers (LXC) sur tous les nœuds."""
    if not proxmox: return "Client Proxmox non configuré."
    try:
        machines = proxmox.get_all_machines()
        if not machines:
            return "Aucune machine trouvée."
        
        result = "Liste des machines (VMs & LXC) :\n"
        for m in machines:
            vmid = m.get('vmid')
            name = m.get('name')
            status = m.get('status')
            node = m.get('node')
            m_type = m.get('type')
            result += f"[{m_type.upper()}] ID: {vmid} | Nom: {name} | Statut: {status} | Nœud: {node}\n"
        return result
    except Exception as e:
        return f"Erreur lors de la récupération des machines : {e}"

@mcp.tool()
def list_storage():
    """Affiche l'état des stockages sur tous les nœuds."""
    if not proxmox: return "Client Proxmox non configuré."
    try:
        nodes = proxmox.get_nodes()
        result = "État des stockages :\n"
        for n in nodes:
            node_name = n['node']
            result += f"\nNœud: {node_name}\n"
            storages = proxmox.get_storage_status(node_name)
            for s in storages:
                if s.get('active'):
                    used = (s.get('used', 0) / s.get('total', 1)) * 100
                    free_gb = s.get('avail', 0) / (1024**3)
                    result += f"  - {s['storage']} ({s['type']}) : {used:.1f}% utilisé ({free_gb:.1f} GB libres)\n"
        return result
    except Exception as e:
        return f"Erreur lors de la récupération des stockages : {e}"

@mcp.tool()
def start_machine(vmid: int, node: str, type: str):
    """
    Démarre une machine spécifique.
    - vmid: ID de la machine (ex: 100)
    - node: Nom du nœud (ex: 'pve')
    - type: 'qemu' pour VM ou 'lxc' pour container
    """
    if not proxmox: return "Client Proxmox non configuré."
    try:
        proxmox.set_machine_state(node, vmid, type, 'start')
        return f"Commande de démarrage envoyée pour la machine {vmid} ({type}) sur le nœud {node}."
    except Exception as e:
        return f"Erreur lors du démarrage : {e}"

@mcp.tool()
def stop_machine(vmid: int, node: str, type: str, force: bool = False):
    """
    Arrête une machine spécifique.
    - vmid: ID de la machine
    - node: Nom du nœud
    - type: 'qemu' ou 'lxc'
    - force: Si True, force l'arrêt (stop), sinon fait un arrêt propre (shutdown).
    """
    if not proxmox: return "Client Proxmox non configuré."
    action = 'stop' if force else 'shutdown'
    try:
        proxmox.set_machine_state(node, vmid, type, action)
        mode = "forcé" if force else "propre"
        return f"Commande d'arrêt {mode} envoyée pour la machine {vmid} ({type}) sur le nœud {node}."
    except Exception as e:
        return f"Erreur lors de l'arrêt : {e}"

@mcp.tool()
def reboot_machine(vmid: int, node: str, type: str):
    """Redémarre une machine spécifique."""
    if not proxmox: return "Client Proxmox non configuré."
    try:
        proxmox.set_machine_state(node, vmid, type, 'reboot')
        return f"Commande de redémarrage envoyée pour la machine {vmid} ({type}) sur le nœud {node}."
    except Exception as e:
        return f"Erreur lors du redémarrage : {e}"

if __name__ == "__main__":
    mcp.run()
