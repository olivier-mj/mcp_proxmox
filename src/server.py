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

@mcp.tool()
def set_cloudinit_config(vmid: int, node: str, user: str = None, password: str = None, ssh_keys: str = None, ip_config: str = "ip=dhcp"):
    """
    Configures Cloud-Init parameters for a VM.
    
    Args:
        vmid (int): VM ID.
        node (str): Node name.
        user (str, optional): Cloud-Init username.
        password (str, optional): Cloud-Init password.
        ssh_keys (str, optional): Public SSH key(s).
        ip_config (str, optional): Network config (default: 'ip=dhcp'). Example static: 'ip=192.168.1.50/24,gw=192.168.1.1'
    """
    logger.info(f"Tool called: set_cloudinit_config(vmid={vmid}, node={node})")
    if not proxmox: return "Client Proxmox non configuré."
    try:
        proxmox.set_cloudinit_config(node, vmid, user, password, ssh_keys, ip_config)
        return f"Configuration Cloud-Init appliquée pour la machine {vmid}. (Redémarrage nécessaire pour prise en compte)"
    except Exception as e:
        logger.error(f"Error in set_cloudinit_config: {e}")
        return f"Erreur lors de la configuration Cloud-Init : {e}"

@mcp.tool()
def resize_resources(vmid: int, node: str, type: Literal['qemu', 'lxc'], cores: Optional[int] = None, memory_mb: Optional[int] = None):
    """
    Adjusts the number of CPU cores and/or RAM of a machine.
    
    Args:
        vmid (int): Machine ID.
        node (str): Node name.
        type (str): 'qemu' or 'lxc'.
        cores (int, optional): New number of CPU cores.
        memory_mb (int, optional): New RAM size in MB (e.g., 2048 for 2GB).
    """
    logger.info(f"Tool called: resize_resources(vmid={vmid}, node={node}, cores={cores}, mem={memory_mb})")
    if not proxmox: return "Client Proxmox non configuré."
    try:
        proxmox.resize_machine_resources(node, vmid, type, cores, memory_mb)
        changes = []
        if cores: changes.append(f"{cores} cœurs")
        if memory_mb: changes.append(f"{memory_mb} MB RAM")
        return f"Ressources mises à jour pour la machine {vmid} : {', '.join(changes)}."
    except Exception as e:
        logger.error(f"Error in resize_resources: {e}")
        return f"Erreur lors du redimensionnement : {e}"

@mcp.tool()
def list_isos(node: str, storage: str):
    """
    Lists available ISO files on a storage.
    
    Args:
        node (str): Node name.
        storage (str): Storage ID (e.g., 'local').
    """
    logger.info(f"Tool called: list_isos(node={node}, storage={storage})")
    if not proxmox: return "Client Proxmox non configuré."
    try:
        isos = proxmox.list_isos(node, storage)
        if not isos: return f"Aucun ISO trouvé sur {storage}."
        
        result = f"ISOs disponibles sur {storage} ({len(isos)}) :\n"
        for iso in isos:
            size_gb = iso.get('size', 0) / (1024**3)
            result += f"  - {iso['volid']} ({size_gb:.2f} GB)\n"
        return result
    except Exception as e:
        logger.error(f"Error in list_isos: {e}")
        return f"Erreur lors de la récupération des ISOs : {e}"

@mcp.tool()
def download_iso(node: str, storage: str, url: str, filename: str):
    """
    Downloads an ISO file from a URL directly to Proxmox storage.
    
    Args:
        node (str): Node name.
        storage (str): Storage ID (e.g., 'local').
        url (str): Direct link to the ISO file.
        filename (str): Name of the file on disk (must end with .iso).
    """
    logger.info(f"Tool called: download_iso(node={node}, storage={storage}, url={url})")
    if not proxmox: return "Client Proxmox non configuré."
    try:
        proxmox.download_iso(node, storage, url, filename)
        return f"Téléchargement de '{filename}' lancé depuis {url} vers {storage}."
    except Exception as e:
        logger.error(f"Error in download_iso: {e}")
        return f"Erreur lors du téléchargement : {e}"

@mcp.tool()
def list_firewall_rules(vmid: int, node: str, type: Literal['qemu', 'lxc']):
    """
    Lists all firewall rules for a specific machine.
    
    Args:
        vmid (int): Machine ID.
        node (str): Node name.
        type (str): 'qemu' or 'lxc'.
    """
    logger.info(f"Tool called: list_firewall_rules(vmid={vmid}, node={node})")
    if not proxmox: return "Client Proxmox non configuré."
    try:
        rules = proxmox.get_firewall_rules(node, vmid, type)
        if not rules: return f"Aucune règle de pare-feu trouvée pour la machine {vmid}."
        
        result = f"Règles Firewall pour {vmid} ({type}) :\n"
        for r in rules:
            status = "ON" if r.get('enable') else "OFF"
            action = r.get('action')
            direction = r.get('type') # 'in' or 'out'
            proto = r.get('proto', 'any')
            dport = r.get('dport', 'any')
            result += f"  - [{status}] {direction.upper()} {action} | Proto: {proto} | Port: {dport}\n"
        return result
    except Exception as e:
        logger.error(f"Error in list_firewall_rules: {e}")
        return f"Erreur lors de la récupération des règles : {e}"

@mcp.tool()
def add_firewall_rule(vmid: int, node: str, type: Literal['qemu', 'lxc'], action: Literal['ACCEPT', 'DROP', 'REJECT'], direction: Literal['in', 'out'], proto: Optional[str] = None, port: Optional[str] = None):
    """
    Adds a firewall rule to a machine.
    
    Args:
        vmid (int): Machine ID.
        node (str): Node name.
        type (str): 'qemu' or 'lxc'.
        action (str): 'ACCEPT', 'DROP' or 'REJECT'.
        direction (str): 'in' for inbound or 'out' for outbound.
        proto (str, optional): Protocol (e.g., 'tcp', 'udp', 'icmp').
        port (str, optional): Destination port (e.g., '80', '22', '1000:2000').
    """
    logger.info(f"Tool called: add_firewall_rule(vmid={vmid}, action={action}, proto={proto})")
    if not proxmox: return "Client Proxmox non configuré."
    try:
        proxmox.add_firewall_rule(node, vmid, type, action, direction, proto=proto, dport=port)
        return f"Règle de pare-feu ({action} {direction} {proto or ''}) ajoutée avec succès pour la machine {vmid}."
    except Exception as e:
        logger.error(f"Error in add_firewall_rule: {e}")
        return f"Erreur lors de l'ajout de la règle : {e}"

@mcp.tool()
def migrate_machine(vmid: int, node: str, type: Literal['qemu', 'lxc'], target_node: str, online: bool = False):
    """
    Migrates a machine to another node in the cluster.
    
    Args:
        vmid (int): Machine ID.
        node (str): Source node name.
        type (str): 'qemu' or 'lxc'.
        target_node (str): Destination node name.
        online (bool): If True, attempts a live migration (no downtime).
    """
    logger.info(f"Tool called: migrate_machine(vmid={vmid}, from={node}, to={target_node}, online={online})")
    if not proxmox: return "Client Proxmox non configuré."
    try:
        proxmox.migrate_machine(node, vmid, type, target_node, online)
        mode = "à chaud (online)" if online else "à froid (offline)"
        return f"Migration {mode} de la machine {vmid} vers le nœud {target_node} lancée."
    except Exception as e:
        logger.error(f"Error in migrate_machine: {e}")
        return f"Erreur lors de la migration : {e}"

@mcp.tool()
def delete_snapshot(vmid: int, node: str, type: Literal['qemu', 'lxc'], snapname: str):
    """
    Deletes a specific snapshot to free up storage space.
    
    Args:
        vmid (int): Machine ID.
        node (str): Node name.
        type (str): 'qemu' or 'lxc'.
        snapname (str): Name of the snapshot to delete.
    """
    logger.info(f"Tool called: delete_snapshot(vmid={vmid}, snapname={snapname})")
    if not proxmox: return "Client Proxmox non configuré."
    try:
        proxmox.delete_snapshot(node, vmid, type, snapname)
        return f"Suppression du snapshot '{snapname}' lancée pour la machine {vmid}."
    except Exception as e:
        logger.error(f"Error in delete_snapshot: {e}")
        return f"Erreur lors de la suppression du snapshot : {e}"

@mcp.tool()
def unlock_machine(vmid: int, node: str):
    """
    Unlocks a machine if it is stuck in a 'locked' state (e.g., after a failed backup).
    
    Args:
        vmid (int): Machine ID.
        node (str): Node name.
    """
    logger.info(f"Tool called: unlock_machine(vmid={vmid}, node={node})")
    if not proxmox: return "Client Proxmox non configuré."
    try:
        proxmox.unlock_machine(node, vmid)
        return f"Commande de déverrouillage envoyée pour la machine {vmid}."
    except Exception as e:
        logger.error(f"Error in unlock_machine: {e}")
        return f"Erreur lors du déverrouillage : {e}"

@mcp.tool()
def get_cluster_logs(max_lines: int = 20):
    """
    Retrieves the latest global cluster logs to diagnose issues.
    
    Args:
        max_lines (int): Number of log lines to retrieve (default: 20).
    """
    logger.info(f"Tool called: get_cluster_logs(limit={max_lines})")
    if not proxmox: return "Client Proxmox non configuré."
    try:
        logs = proxmox.get_cluster_log(max_lines)
        if not logs: return "Aucun log trouvé."
        
        result = f"Derniers logs du cluster ({len(logs)}) :\n"
        for l in logs:
            # Proxmox logs have fields like 't' (text), 'u' (user), 'time', 'node'
            time_str = l.get('time', '')
            node = l.get('node', '?')
            user = l.get('user', '?')
            msg = l.get('msg', l.get('t', ''))
            result += f"[{time_str}] ({node}) {user}: {msg}\n"
        return result
    except Exception as e:
        logger.error(f"Error in get_cluster_logs: {e}")
        return f"Erreur lors de la récupération des logs : {e}"

if __name__ == "__main__":
    mcp.run()
