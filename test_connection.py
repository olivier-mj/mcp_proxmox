from src.client import ProxmoxClient
import sys

try:
    print("Tentative de connexion à Proxmox...")
    client = ProxmoxClient()
    nodes = client.get_nodes()
    print(f"✅ Connexion réussie ! {len(nodes)} nœud(s) trouvé(s).")
    for node in nodes:
        print(f"   - {node['node']} (Status: {node.get('status', 'unknown')})")
        
    print("\nTest de récupération des machines...")
    machines = client.get_all_machines()
    print(f"✅ {len(machines)} machine(s) trouvée(s).")
    for m in machines[:5]: # Affiche les 5 premières
        print(f"   - [{m.get('type')}] {m.get('name')} (ID: {m.get('vmid')}) sur {m.get('node')}")
        
except Exception as e:
    print(f"❌ Échec de la connexion ou de l'exécution : {e}")
    sys.exit(1)
