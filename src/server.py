import os
import logging
from typing import Literal, Optional
from mcp.server.fastmcp import FastMCP
from src.client import ProxmoxClient

# Configuration du Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger("mcp-proxmox")

# Initialisation du serveur MCP
mcp = FastMCP("Proxmox Manager")

# Initialisation du client Proxmox
try:
    proxmox = ProxmoxClient()
    logger.info("Client Proxmox initialisé avec succès.")
except Exception as e:
    logger.error(f"Erreur d'initialisation du client Proxmox: {e}")
    proxmox = None

@mcp.tool()
def list_infrastructure():
    """
    Lists all nodes in the Proxmox cluster with their CPU and RAM usage.
    
    Returns:
        str: A formatted string summarizing the infrastructure status.
    """
    logger.info("Tool called: list_infrastructure")
    if not proxmox: return "Client Proxmox non configuré."
    try:
        nodes = proxmox.get_nodes()
        result = "Infrastucture Proxmox :\n"
        for n in nodes:
            # Check node status first
            status = n.get('status', 'unknown')
            if status != 'online':
                result += f"- Nœud: {n['node']} | Statut: {status} (Hors ligne)\n"
                continue
                
            cpu = n.get('cpu', 0) * 100
            ram = (n.get('mem', 0) / n.get('maxmem', 1)) * 100
            result += f"- Nœud: {n['node']} | Statut: {status} | CPU: {cpu:.1f}% | RAM: {ram:.1f}%\n"
        return result
    except Exception as e:
        logger.error(f"Error in list_infrastructure: {e}")
        return f"Erreur lors de la récupération de l'infrastructure : {e}"

@mcp.tool()
def list_machines(name_filter: Optional[str] = None, status_filter: Optional[Literal['running', 'stopped']] = None, type_filter: Optional[Literal['qemu', 'lxc']] = None):
    """
    Lists all VMs and Containers (LXC) with optional filtering.

    Args:
        name_filter (str, optional): Filter by name substring (case-insensitive).
        status_filter (str, optional): Filter by status ('running' or 'stopped').
        type_filter (str, optional): Filter by type ('qemu' or 'lxc').

    Returns:
        str: A formatted list of machines matching the criteria.
    """
    logger.info(f"Tool called: list_machines(name={name_filter}, status={status_filter}, type={type_filter})")
    if not proxmox: return "Client Proxmox non configuré."
    try:
        machines = proxmox.get_all_machines()
        if not machines:
            return "Aucune machine trouvée."
        
        # Application des filtres
        if name_filter:
            machines = [m for m in machines if name_filter.lower() in m.get('name', '').lower()]
        if status_filter:
            machines = [m for m in machines if m.get('status') == status_filter.lower()]
        if type_filter:
            machines = [m for m in machines if m.get('type') == type_filter.lower()]

        if not machines:
            return "Aucune machine ne correspond aux filtres."

        result = f"Liste des machines ({len(machines)}) :\n"
        for m in machines:
            vmid = m.get('vmid')
            name = m.get('name')
            status = m.get('status')
            node = m.get('node')
            m_type = m.get('type')
            result += f"[{m_type.upper()}] ID: {vmid} | Nom: {name} | Statut: {status} | Nœud: {node}\n"
        return result
    except Exception as e:
        logger.error(f"Error in list_machines: {e}")
        return f"Erreur lors de la récupération des machines : {e}"

@mcp.tool()
def list_storage():
    """
    Displays the storage status for all nodes.

    Returns:
        str: A formatted string showing used/total space for each storage.
    """
    logger.info("Tool called: list_storage")
    if not proxmox: return "Client Proxmox non configuré."
    try:
        nodes = proxmox.get_nodes()
        result = "État des stockages :\n"
        for n in nodes:
            node_name = n['node']
            if n.get('status') != 'online':
                result += f"\nNœud: {node_name} (Hors ligne - Stockage inaccessible)\n"
                continue

            result += f"\nNœud: {node_name}\n"
            try:
                storages = proxmox.get_storage_status(node_name)
                for s in storages:
                    if s.get('active'):
                        used = (s.get('used', 0) / s.get('total', 1)) * 100
                        free_gb = s.get('avail', 0) / (1024**3)
                        result += f"  - {s['storage']} ({s['type']}) : {used:.1f}% utilisé ({free_gb:.1f} GB libres)\n"
            except Exception as e:
                logger.warning(f"Impossible de lire le stockage sur {node_name}: {e}")
                result += f"  - Erreur de lecture stockage: {e}\n"
        return result
    except Exception as e:
        logger.error(f"Error in list_storage: {e}")
        return f"Erreur lors de la récupération des stockages : {e}"

@mcp.tool()
def start_machine(vmid: int, node: str, type: Literal['qemu', 'lxc']):
    """
    Starts a specific machine.

    Args:
        vmid (int): Machine ID (e.g., 100).
        node (str): Node name (e.g., 'pve').
        type (str): 'qemu' (VM) or 'lxc' (Container).
    """
    logger.info(f"Tool called: start_machine(vmid={vmid}, node={node}, type={type})")
    if vmid < 100: return "Erreur: L'ID de la machine doit être >= 100."
    
    if not proxmox: return "Client Proxmox non configuré."
    try:
        proxmox.set_machine_state(node, vmid, type, 'start')
        return f"Commande de démarrage envoyée pour la machine {vmid} ({type}) sur le nœud {node}."
    except Exception as e:
        logger.error(f"Error in start_machine: {e}")
        return f"Erreur lors du démarrage : {e}"

@mcp.tool()
def stop_machine(vmid: int, node: str, type: Literal['qemu', 'lxc'], force: bool = False):
    """
    Stops a specific machine.

    Args:
        vmid (int): Machine ID.
        node (str): Node name.
        type (str): 'qemu' or 'lxc'.
        force (bool): If True, forces a hard stop. If False (default), attempts a graceful shutdown.
    """
    logger.info(f"Tool called: stop_machine(vmid={vmid}, node={node}, type={type}, force={force})")
    if vmid < 100: return "Erreur: L'ID de la machine doit être >= 100."

    if not proxmox: return "Client Proxmox non configuré."
    action = 'stop' if force else 'shutdown'
    try:
        proxmox.set_machine_state(node, vmid, type, action)
        mode = "forcé" if force else "propre"
        return f"Commande d'arrêt {mode} envoyée pour la machine {vmid} ({type}) sur le nœud {node}."
    except Exception as e:
        logger.error(f"Error in stop_machine: {e}")
        return f"Erreur lors de l'arrêt : {e}"

@mcp.tool()
def reboot_machine(vmid: int, node: str, type: Literal['qemu', 'lxc']):
    """
    Reboots a specific machine.

    Args:
        vmid (int): Machine ID.
        node (str): Node name.
        type (str): 'qemu' or 'lxc'.
    """
    logger.info(f"Tool called: reboot_machine(vmid={vmid}, node={node}, type={type})")
    if vmid < 100: return "Erreur: L'ID de la machine doit être >= 100."

    if not proxmox: return "Client Proxmox non configuré."
    try:
        proxmox.set_machine_state(node, vmid, type, 'reboot')
        return f"Commande de redémarrage envoyée pour la machine {vmid} ({type}) sur le nœud {node}."
    except Exception as e:
        logger.error(f"Error in reboot_machine: {e}")
        return f"Erreur lors du redémarrage : {e}"

@mcp.tool()
def get_machine_config(vmid: int, node: str, type: Literal['qemu', 'lxc']):
    """
    Retrieves the detailed configuration (CPU, RAM, Disks, etc.) of a machine.

    Args:
        vmid (int): Machine ID.
        node (str): Node name.
        type (str): 'qemu' or 'lxc'.
    """
    logger.info(f"Tool called: get_machine_config(vmid={vmid}, node={node}, type={type})")
    if vmid < 100: return "Erreur: L'ID de la machine doit être >= 100."

    if not proxmox: return "Client Proxmox non configuré."
    try:
        config = proxmox.get_machine_config(node, vmid, type)
        result = f"Configuration de la machine {vmid} ({type}) :\n"
        for key, value in config.items():
            result += f"  - {key}: {value}\n"
        return result
    except Exception as e:
        logger.error(f"Error in get_machine_config: {e}")
        return f"Erreur lors de la récupération de la config : {e}"

@mcp.tool()
def list_snapshots(vmid: int, node: str, type: Literal['qemu', 'lxc']):
    """
    Lists available snapshots for a machine.

    Args:
        vmid (int): Machine ID.
        node (str): Node name.
        type (str): 'qemu' or 'lxc'.
    """
    logger.info(f"Tool called: list_snapshots(vmid={vmid}, node={node}, type={type})")
    if vmid < 100: return "Erreur: L'ID de la machine doit être >= 100."

    if not proxmox: return "Client Proxmox non configuré."
    try:
        snaps = proxmox.list_snapshots(node, vmid, type)
        if not snaps: return "Aucun snapshot trouvé."
        result = f"Snapshots pour la machine {vmid} :\n"
        for s in snaps:
            desc = s.get('description', 'Sans description')
            result += f"  - {s['name']} (Date: {s.get('snaptime', 'Inconnue')}) | {desc}\n"
        return result
    except Exception as e:
        logger.error(f"Error in list_snapshots: {e}")
        return f"Erreur lors de la récupération des snapshots : {e}"

@mcp.tool()
def create_snapshot(vmid: int, node: str, type: Literal['qemu', 'lxc'], snapname: str, description: str = None):
    """
    Creates a snapshot for a machine.

    Args:
        vmid (int): Machine ID.
        node (str): Node name.
        type (str): 'qemu' or 'lxc'.
        snapname (str): Name of the snapshot (no spaces recommended).
        description (str, optional): Short description.
    """
    logger.info(f"Tool called: create_snapshot(vmid={vmid}, node={node}, name={snapname})")
    if vmid < 100: return "Erreur: L'ID de la machine doit être >= 100."

    if not proxmox: return "Client Proxmox non configuré."
    try:
        proxmox.create_snapshot(node, vmid, type, snapname, description)
        return f"Snapshot '{snapname}' en cours de création pour la machine {vmid}."
    except Exception as e:
        logger.error(f"Error in create_snapshot: {e}")
        return f"Erreur lors de la création du snapshot : {e}"

@mcp.tool()
def rollback_snapshot(vmid: int, node: str, type: Literal['qemu', 'lxc'], snapname: str):
    """
    Rolls back a machine to a previous snapshot.
    WARNING: Current state will be lost.

    Args:
        vmid (int): Machine ID.
        node (str): Node name.
        type (str): 'qemu' or 'lxc'.
        snapname (str): Name of the snapshot to restore.
    """
    logger.info(f"Tool called: rollback_snapshot(vmid={vmid}, node={node}, name={snapname})")
    if vmid < 100: return "Erreur: L'ID de la machine doit être >= 100."

    if not proxmox: return "Client Proxmox non configuré."
    try:
        proxmox.rollback_snapshot(node, vmid, type, snapname)
        return f"Restauration du snapshot '{snapname}' lancée pour la machine {vmid}."
    except Exception as e:
        logger.error(f"Error in rollback_snapshot: {e}")
        return f"Erreur lors de la restauration : {e}"

@mcp.tool()
def clone_machine(vmid: int, node: str, type: Literal['qemu', 'lxc'], newid: int, name: str, target_node: Optional[str] = None):
    """
    Clones a machine (usually a template) to create a new one.

    Args:
        vmid (int): ID of the source machine/template.
        node (str): Node where the source machine is located.
        type (str): 'qemu' or 'lxc'.
        newid (int): ID for the new machine (must be unique and > 100).
        name (str): Name for the new machine.
        target_node (str, optional): Target node for the new machine (if different).
    """
    logger.info(f"Tool called: clone_machine(source={vmid}, newid={newid}, name={name})")
    if vmid < 100 or newid < 100: return "Erreur: Les IDs doivent être >= 100."
    
    if not proxmox: return "Client Proxmox non configuré."
    try:
        proxmox.clone_machine(node, vmid, newid, name, type, target_node)
        return f"Clonage de {vmid} vers {newid} ({name}) lancé avec succès."
    except Exception as e:
        logger.error(f"Error in clone_machine: {e}")
        return f"Erreur lors du clonage : {e}"

@mcp.tool()
def get_vm_agent_network(vmid: int, node: str):
    """
    Retrieves internal network information (IP addresses) from a VM.
    Requires QEMU Guest Agent to be installed and enabled.

    Args:
        vmid (int): VM ID.
        node (str): Node name.
    """
    logger.info(f"Tool called: get_vm_agent_network(vmid={vmid}, node={node})")
    if not proxmox: return "Client Proxmox non configuré."
    try:
        data = proxmox.get_vm_agent_network(node, vmid)
        if not data: return "Aucune donnée réseau reçue (l'agent est-il activé ?)."
        
        result = f"Interfaces réseau internes pour VM {vmid} :\n"
        for interface in data.get('result', []):
            name = interface.get('name')
            ips = [addr.get('ip-address') for addr in interface.get('ip-addresses', [])]
            result += f"  - {name}: {', '.join(ips)}\n"
        return result
    except Exception as e:
        logger.error(f"Error in get_vm_agent_network: {e}")
        return f"Erreur lors de la communication avec l'agent : {e}. Assurez-vous que l'agent QEMU est actif sur la VM."

@mcp.tool()
def list_backups(node: str, storage: str):
    """
    Lists backups available on a specific storage.

    Args:
        node (str): Node name.
        storage (str): Storage name (e.g., 'local', 'nas').
    """
    logger.info(f"Tool called: list_backups(node={node}, storage={storage})")
    if not proxmox: return "Client Proxmox non configuré."
    try:
        backups = proxmox.list_backups(node, storage)
        if not backups: return f"Aucune sauvegarde trouvée sur {storage}."
        
        result = f"Sauvegardes sur {storage} ({len(backups)}) :\n"
        for b in backups:
            size_gb = b.get('size', 0) / (1024**3)
            result += f"  - {b['volid']} ({size_gb:.2f} GB) | Date: {b.get('ctime', 'Inconnue')}\n"
        return result
    except Exception as e:
        logger.error(f"Error in list_backups: {e}")
        return f"Erreur lors de la récupération des sauvegardes : {e}"

@mcp.tool()
def create_backup(vmid: int, node: str, storage: str, mode: Literal['snapshot', 'suspend', 'stop'] = 'snapshot'):
    """
    Creates a new backup for a machine.

    Args:
        vmid (int): Machine ID.
        node (str): Node name.
        storage (str): Target storage for the backup.
        mode (str): Backup mode ('snapshot' is default and recommended).
    """
    logger.info(f"Tool called: create_backup(vmid={vmid}, node={node}, storage={storage})")
    if not proxmox: return "Client Proxmox non configuré."
    try:
        proxmox.create_backup(node, vmid, storage, mode)
        return f"Tâche de sauvegarde lancée pour la machine {vmid} vers le stockage {storage}."
    except Exception as e:
        logger.error(f"Error in create_backup: {e}")
        return f"Erreur lors du lancement de la sauvegarde : {e}"

@mcp.tool()
def get_console_url(vmid: int, node: str, type: Literal['qemu', 'lxc']):
    """
    Generates a direct link to the NoVNC console in the Proxmox Web UI.
    Requires the user to be logged into the Proxmox Web interface.

    Args:
        vmid (int): Machine ID.
        node (str): Node name.
        type (str): 'qemu' or 'lxc'.
    """
    logger.info(f"Tool called: get_console_url(vmid={vmid}, node={node})")
    if not proxmox: return "Client Proxmox non configuré."
    try:
        url = proxmox.get_console_url(node, vmid, type)
        return f"Lien vers la console NoVNC pour la machine {vmid} :\n{url}"
    except Exception as e:
        logger.error(f"Error in get_console_url: {e}")
        return f"Erreur lors de la génération du lien : {e}"

if __name__ == "__main__":
    mcp.run()
