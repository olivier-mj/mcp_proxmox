import os
from src.client import ProxmoxClient
from dotenv import load_dotenv

def test_live_storage():
    load_dotenv()
    print("🔍 Connexion à Proxmox pour test live du stockage...")
    
    try:
        client = ProxmoxClient()
        nodes = client.get_nodes()
        
        print(f"✅ Connecté. {len(nodes)} nœud(s) détecté(s).\n")
        print(f"{ 'NŒUD':<12} | {'STOCKAGE':<15} | {'TYPE':<8} | {'UTILISATION':<10} | {'CONTENU'}")
        print("-" * 80)
        
        for node in nodes:
            node_name = node['node']
            if node.get('status') != 'online':
                print(f"{node_name:<12} | (HORS LIGNE)")
                continue
                
            storages = client.get_storage_status(node_name)
            for s in storages:
                if s.get('active'):
                    name = s['storage']
                    stype = s['type']
                    used_pct = (s.get('used', 0) / s.get('total', 1)) * 100
                    content = s.get('content', 'aucun')
                    shared = "*" if s.get('shared') else " "
                    
                    print(f"{node_name:<12} | {name:<15}{shared} | {stype:<8} | {used_pct:>6.1f}% | {content}")
        
        print("\n* = Stockage partagé (Shared)")
        
    except Exception as e:
        print(f"❌ Erreur lors du test : {e}")

if __name__ == "__main__":
    test_live_storage()
