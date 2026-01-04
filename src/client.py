import os
from proxmoxer import ProxmoxAPI
from dotenv import load_dotenv
from urllib.parse import urlparse

load_dotenv()

class ProxmoxClient:
    def __init__(self):
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
        """Liste tous les nœuds du cluster."""
        return self.api.nodes.get()

    def get_all_machines(self):
        """Récupère toutes les VMs et Containers sur tous les nœuds."""
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
        Change l'état d'une machine (start, stop, shutdown, reboot).
        machine_type doit être 'qemu' ou 'lxc'.
        """
        if machine_type == 'qemu':
            return self.api.nodes(node).qemu(vmid).status.post(action)
        elif machine_type == 'lxc':
            return self.api.nodes(node).lxc(vmid).status.post(action)
        else:
            raise ValueError("machine_type doit être 'qemu' ou 'lxc'")

    def get_node_resources(self, node):
        """Récupère l'état des ressources d'un nœud spécifique."""
        return self.api.nodes(node).status.get()

    def get_storage_status(self, node):
        """Récupère l'état des stockages sur un nœud spécifique."""
        return self.api.nodes(node).storage.get()
