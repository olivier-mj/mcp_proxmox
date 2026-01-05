import logging
from src.server import get_console_url

logging.basicConfig(level=logging.INFO)

print("--- TEST V3: Console VNC ---")

VMID = 200
NODE = 'proxmox'

print(f"Génération du lien pour la VM {VMID}...")
result = get_console_url(vmid=VMID, node=NODE, type='qemu')
print(result)
