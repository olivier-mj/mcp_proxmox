import os
from proxmoxer import ProxmoxAPI
from dotenv import load_dotenv
from urllib.parse import urlparse

load_dotenv()

class ProxmoxClient:
    """
    Client wrapper for interacting with the Proxmox VE API.
    
    Handles authentication via API Tokens and provides simplified methods
    for common operations like listing nodes, managing VMs/LXC, and snapshots.
    """

    def __init__(self):
        """
        Initializes the Proxmox API client using environment variables.

        Raises:
            ValueError: If required environment variables are missing.
        """
        url = os.getenv("PROXMOX_URL")
        if not url:
            raise ValueError("PROXMOX_URL is not set in .env")
            
        parsed_url = urlparse(url)
        host = parsed_url.hostname
        port = parsed_url.port or 8006
        
        user = os.getenv("PROXMOX_USER")
        token_id = os.getenv("PROXMOX_TOKEN_ID")
        token_secret = os.getenv("PROXMOX_TOKEN_SECRET")
        verify_ssl = os.getenv("PROXMOX_VERIFY_SSL", "false").lower() == "true"

        if not all([user, token_id, token_secret]):
            raise ValueError("Proxmox credentials (USER, TOKEN_ID, TOKEN_SECRET) are missing in .env")

        # Debugging credentials (security-safe)
        # print(f"DEBUG: Host={host}, User={user}, TokenID={token_id}")

        self.api = ProxmoxAPI(
            host,
            user=user,
            token_name=token_id,
            token_value=token_secret,
            verify_ssl=verify_ssl,
            port=port
        )

    def get_nodes(self):
        """
        Lists all nodes in the Proxmox cluster.

        Returns:
            list: A list of dictionaries containing node information.
        """
        return self.api.nodes.get()

    def get_all_machines(self):
        """
        Retrieves all VMs (QEMU) and Containers (LXC) across all nodes.

        Returns:
            list: A unified list of dictionaries for both VMs and LXCs,
                  including an extra 'type' field ('qemu' or 'lxc').
        """
        machines = []
        for node in self.get_nodes():
            node_name = node['node']
            # VMs (QEMU)
            try:
                vms = self.api.nodes(node_name).qemu.get()
                for vm in vms:
                    vm['node'] = node_name
                    vm['type'] = 'qemu'
                    machines.append(vm)
            except Exception as e:
                print(f"Erreur lors de la récupération des VMs sur {node_name}: {e}")

            # Containers (LXC)
            try:
                lxcs = self.api.nodes(node_name).lxc.get()
                for lxc in lxcs:
                    lxc['node'] = node_name
                    lxc['type'] = 'lxc'
                    # Proxmox API LXC returns 'vmid', QEMU returns 'vmid' too, but let's be consistent
                    machines.append(lxc)
            except Exception as e:
                print(f"Erreur lors de la récupération des containers sur {node_name}: {e}")
        
        return machines

    def set_machine_state(self, node, vmid, machine_type, action):
        """
        Changes the state of a specific machine.

        Args:
            node (str): The name of the node where the machine is located.
            vmid (int): The ID of the machine.
            machine_type (str): 'qemu' for VMs or 'lxc' for containers.
            action (str): The action to perform ('start', 'stop', 'shutdown', 'reboot').

        Returns:
            str: Task ID of the operation.

        Raises:
            ValueError: If machine_type is invalid.
        """
        if machine_type == 'qemu':
            return self.api.nodes(node).qemu(vmid).status.post(action)
        elif machine_type == 'lxc':
            return self.api.nodes(node).lxc(vmid).status.post(action)
        else:
            raise ValueError("machine_type doit être 'qemu' ou 'lxc'")

    def get_node_resources(self, node):
        """
        Retrieves resource usage statistics for a specific node.

        Args:
            node (str): Node name.

        Returns:
            dict: Dictionary containing cpu, memory, etc.
        """
        return self.api.nodes(node).status.get()

    def get_storage_status(self, node):
        """
        Retrieves storage status for a specific node.

        Args:
            node (str): Node name.

        Returns:
            list: List of storage devices and their usage.
        """
        return self.api.nodes(node).storage.get()

    def get_machine_config(self, node, vmid, machine_type):
        """
        Retrieves the detailed configuration of a machine.

        Args:
            node (str): Node name.
            vmid (int): Machine ID.
            machine_type (str): 'qemu' or 'lxc'.

        Returns:
            dict: Configuration parameters (cores, memory, net, etc.).
        """
        if machine_type == 'qemu':
            return self.api.nodes(node).qemu(vmid).config.get()
        return self.api.nodes(node).lxc(vmid).config.get()

    def list_snapshots(self, node, vmid, machine_type):
        """
        Lists snapshots for a specific machine.

        Args:
            node (str): Node name.
            vmid (int): Machine ID.
            machine_type (str): 'qemu' or 'lxc'.

        Returns:
            list: List of snapshot dictionaries.
        """
        if machine_type == 'qemu':
            return self.api.nodes(node).snapshot.get()
        return self.api.nodes(node).lxc(vmid).snapshot.get()

    def create_snapshot(self, node, vmid, machine_type, snapname, description="Created via MCP"):
        """
        Creates a new snapshot.

        Args:
            node (str): Node name.
            vmid (int): Machine ID.
            machine_type (str): 'qemu' or 'lxc'.
            snapname (str): Name of the snapshot.
            description (str, optional): Description of the snapshot.

        Returns:
            str: Task ID.
        """
        if machine_type == 'qemu':
            return self.api.nodes(node).snapshot.post(snapname=snapname, description=description)
        return self.api.nodes(node).lxc(vmid).snapshot.post(snapname=snapname, description=description)

    def rollback_snapshot(self, node, vmid, machine_type, snapname):
        """
        Rolls back to a specific snapshot.

        Args:
            node (str): Node name.
            vmid (int): Machine ID.
            machine_type (str): 'qemu' or 'lxc'.
            snapname (str): Name of the snapshot to restore.

        Returns:
            str: Task ID.
        """
        if machine_type == 'qemu':
            return self.api.nodes(node).snapshot(snapname).rollback.post()
        return self.api.nodes(node).lxc(vmid).snapshot(snapname).rollback.post()

    def clone_machine(self, node, vmid, newid, name, machine_type, target_node=None):
        """
        Clones a machine (VM or LXC).

        Args:
            node (str): Source node name.
            vmid (int): Source machine ID (Template).
            newid (int): New machine ID.
            name (str): New machine name.
            machine_type (str): 'qemu' or 'lxc'.
            target_node (str, optional): Target node (if different from source). Defaults to None.

        Returns:
            str: Task ID.
        """
        params = {'newid': newid, 'name': name}
        if target_node:
            params['target'] = target_node

        if machine_type == 'qemu':
            return self.api.nodes(node).qemu(vmid).clone.post(**params)
        elif machine_type == 'lxc':
            # LXC cloning usually requires the source to be a template or stopped
            return self.api.nodes(node).lxc(vmid).clone.post(**params)
        else:
            raise ValueError("machine_type doit être 'qemu' ou 'lxc'")

    def get_vm_agent_network(self, node, vmid):
        """Retrieves internal network interfaces via QEMU Guest Agent."""
        return self.api.nodes(node).qemu(vmid).agent.network_get_interfaces.get()

    def exec_agent_command(self, node, vmid, command):
        """Executes a simple command via QEMU Guest Agent."""
        # Note: Command execution via agent usually requires specific formatting
        return self.api.nodes(node).qemu(vmid).agent.exec.post(command=command)

    def list_backups(self, node, storage):
        """Lists backups available on a specific storage."""
        # Proxmox stores backups as content type 'backup'
        return self.api.nodes(node).storage(storage).content.get(content='backup')

    def create_backup(self, node, vmid, storage, mode='snapshot', compress='zstd'):
        """Creates a new backup for a machine."""
        return self.api.nodes(node).vzdump.post(vmid=vmid, storage=storage, mode=mode, compress=compress)

    def get_console_url(self, node, vmid, machine_type):
        """Constructs a direct link to the NoVNC console in the Proxmox Web UI."""
        base_url = os.getenv("PROXMOX_URL").rstrip('/')
        # Proxmox Web UI console URL format
        # Note: The user must be logged into the Web UI for this link to work immediately.
        return f"{base_url}/#v1:0:18:4:::::::{node}:{vmid}:novnc"

    def set_cloudinit_config(self, node, vmid, ciuser=None, cipassword=None, sshkeys=None, ipconfig0=None):
        """
        Sets Cloud-Init configuration for a VM.

        Args:
            node (str): Node name.
            vmid (int): VM ID.
            ciuser (str, optional): Cloud-Init user.
            cipassword (str, optional): Cloud-Init password.
            sshkeys (str, optional): Public SSH keys.
            ipconfig0 (str, optional): IP configuration (e.g., 'ip=dhcp' or 'ip=192.168.1.10/24,gw=192.168.1.1').
        
        Returns:
            str: Task ID.
        """
        params = {}
        if ciuser: params['ciuser'] = ciuser
        if cipassword: params['cipassword'] = cipassword
        if sshkeys: params['sshkeys'] = sshkeys
        if ipconfig0: params['ipconfig0'] = ipconfig0
        
        if not params:
            raise ValueError("Au moins un paramètre Cloud-Init doit être fourni.")

        return self.api.nodes(node).qemu(vmid).config.post(**params)

    def resize_machine_resources(self, node, vmid, machine_type, cores=None, memory=None):
        """
        Resizes CPU cores and RAM for a VM or Container.
        Note: RAM for VMs is in MB.

        Args:
            node (str): Node name.
            vmid (int): Machine ID.
            machine_type (str): 'qemu' or 'lxc'.
            cores (int, optional): Number of CPU cores.
            memory (int, optional): RAM in MB.
        """
        params = {}
        if cores: params['cores'] = cores
        if memory: params['memory'] = memory
        
        if not params:
            raise ValueError("Au moins un paramètre (cores ou memory) doit être fourni.")

        if machine_type == 'qemu':
            return self.api.nodes(node).qemu(vmid).config.post(**params)
        return self.api.nodes(node).lxc(vmid).config.post(**params)

    def list_isos(self, node, storage):
        """
        Lists ISO files available on a specific storage.

        Args:
            node (str): Node name.
            storage (str): Storage name (e.g., 'local', 'nas').
        
        Returns:
            list: List of ISO files.
        """
        return self.api.nodes(node).storage(storage).content.get(content='iso')

    def download_iso(self, node, storage, url, filename):
        """
        Downloads an ISO file from a URL to a specific storage.

        Args:
            node (str): Node name.
            storage (str): Storage name.
            url (str): URL of the ISO file.
            filename (str): Target filename (must end with .iso).

        Returns:
            str: Task ID.
        """
        if not filename.endswith('.iso'):
            raise ValueError("Le nom du fichier doit se terminer par .iso")
            
        return self.api.nodes(node).storage(storage).download_url.post(
            content='iso',
            filename=filename,
            url=url
        )

    def get_firewall_rules(self, node, vmid, machine_type):
        """Lists firewall rules for a VM or LXC container."""
        if machine_type == 'qemu':
            return self.api.nodes(node).qemu(vmid).firewall.rules.get()
        return self.api.nodes(node).lxc(vmid).firewall.rules.get()

    def add_firewall_rule(self, node, vmid, machine_type, action, rule_type, proto=None, dport=None, sport=None, source=None, dest=None, enable=1):
        """Adds a new firewall rule to a VM or LXC container."""
        params = {
            'action': action,
            'type': rule_type,
            'enable': enable
        }
        if proto: params['proto'] = proto
        if dport: params['dport'] = dport
        if sport: params['sport'] = sport
        if source: params['source'] = source
        if dest: params['dest'] = dest

        if machine_type == 'qemu':
            return self.api.nodes(node).qemu(vmid).firewall.rules.post(**params)
        return self.api.nodes(node).lxc(vmid).firewall.rules.post(**params)

    def migrate_machine(self, node, vmid, machine_type, target_node, online=False):
        """
        Migrates a machine to another node.

        Args:
            node (str): Source node.
            vmid (int): Machine ID.
            machine_type (str): 'qemu' or 'lxc'.
            target_node (str): Destination node.
            online (bool): If True, perform online migration (no downtime).
        """
        params = {'target': target_node}
        if online:
            params['online'] = 1
            params['with-local-disks'] = 1 # Often needed for online migration if local storage is used

        if machine_type == 'qemu':
            return self.api.nodes(node).qemu(vmid).migrate.post(**params)
        elif machine_type == 'lxc':
            return self.api.nodes(node).lxc(vmid).migrate.post(**params)
        else:
            raise ValueError("machine_type doit être 'qemu' ou 'lxc'")
