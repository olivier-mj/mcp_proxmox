import logging
from src.server import list_backups, list_storage

logging.basicConfig(level=logging.INFO)

print("--- TEST V3: Gestion des Backups ---")

# 1. Lister les stockages pour trouver celui qui accepte les backups
print("Analyse des stockages...")
print(list_storage())

# 2. Lister les backups sur 'local' (souvent celui par défaut pour les dumps)
STORAGE = 'local'
NODE = 'proxmox'

print(f"\nTentative de lecture des backups sur '{STORAGE}'...")
result = list_backups(node=NODE, storage=STORAGE)
print(result)
