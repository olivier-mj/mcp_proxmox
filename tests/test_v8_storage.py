import unittest
from unittest.mock import MagicMock, patch
from src.client import ProxmoxClient

class TestStorageV8(unittest.TestCase):

    @patch('src.client.ProxmoxAPI')
    @patch.dict('os.environ', {
        'PROXMOX_URL': 'https://test.proxmox.com:8006',
        'PROXMOX_USER': 'root@pam',
        'PROXMOX_TOKEN_ID': 'test-id',
        'PROXMOX_TOKEN_SECRET': 'test-secret',
        'PROXMOX_VERIFY_SSL': 'false'
    })
    def test_get_storage_status_with_content(self, mock_api_cls):
        mock_api_instance = MagicMock()
        mock_api_cls.return_value = mock_api_instance
        client = ProxmoxClient()
        
        # Mock data from Proxmox API /nodes/{node}/storage
        mock_storage = [
            {
                'storage': 'local', 
                'type': 'dir', 
                'content': 'iso,vztmpl,backup', 
                'used': 100, 
                'total': 1000, 
                'avail': 900,
                'active': 1,
                'shared': 0
            },
            {
                'storage': 'ceph-rbd', 
                'type': 'rbd', 
                'content': 'images', 
                'used': 500, 
                'total': 1000, 
                'avail': 500,
                'active': 1,
                'shared': 1
            }
        ]
        mock_api_instance.nodes("pve1").storage.get.return_value = mock_storage

        # Execute
        storages = client.get_storage_status("pve1")

        # Verify
        self.assertEqual(len(storages), 2)
        self.assertIn('content', storages[0])
        self.assertEqual(storages[0]['content'], 'iso,vztmpl,backup')
        self.assertEqual(storages[1]['shared'], 1)
        print("✅ Test Storage V8 (Capacités & Partage) passé.")

if __name__ == '__main__':
    unittest.main()
