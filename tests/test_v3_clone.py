import logging
from src.server import list_machines, clone_machine

logging.basicConfig(level=logging.INFO)

print("--- TEST V3: Provisioning (Clonage) ---")

# 1. Lister les machines pour trouver un candidat (Template)
print("Recherche de machines...")
print(list_machines())

# 2. Simulation de clonage (A ajuster avec un vrai ID si vous voulez tester réellement)
# Remplacez 9000 par un ID de template valide sur votre infra pour tester le succès.
SOURCE_ID = 9000 
NEW_ID = 9001
NAME = "test-mcp-clone"

print(f"\nTentative de clonage (Simulation avec ID {SOURCE_ID})...")
# Cela va probablement échouer si l'ID n'existe pas, mais on verra l'appel dans les logs
result = clone_machine(vmid=SOURCE_ID, node='proxmox', type='qemu', newid=NEW_ID, name=NAME)
print(f"Résultat : {result}")
