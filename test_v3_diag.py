import logging
from src.server import get_vm_agent_network

logging.basicConfig(level=logging.INFO)

print("--- TEST V3: Diagnostic (Agent QEMU) ---")

# On va tester sur votre VM 'home-assistant' (ID 200) qui est 'running'
VMID = 200
NODE = 'proxmox'

print(f"Tentative de récupération des IPs pour la VM {VMID}...")
result = get_vm_agent_network(vmid=VMID, node=NODE)
print(result)
