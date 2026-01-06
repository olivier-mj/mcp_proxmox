import logging
from src.server import list_infrastructure, list_machines, start_machine

# On configure le logging pour voir les traces dans le test
logging.basicConfig(level=logging.INFO)

print("--- TEST 1: Infrastructure & Logging ---")
infra = list_infrastructure()
print(infra)

print("\n--- TEST 2: Filtrage list_machines ---")
# Test filtrage par type
machines_qemu = list_machines(type_filter='qemu')
print(f"Machines QEMU filtrées:\n{machines_qemu[:200]}...") # Truncated for display

print("\n--- TEST 3: Validation Pydantic/ID ---")
# On s'attend à un message d'erreur pour un ID < 100
error_msg = start_machine(vmid=50, node='pve', type='qemu')
print(f"Résultat validation ID (doit être erreur): {error_msg}")

print("\n--- TEST 4: Validation Type (Simulée) ---")
# Note: En Python Literal est une indication, mais nous testons la logique
# Si on passait un mauvais type via MCP (JSON), FastMCP le rejetterait.
