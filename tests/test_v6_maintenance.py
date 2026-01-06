import unittest
from unittest.mock import MagicMock, patch
from src.client import ProxmoxClient

class TestMaintenance(unittest.TestCase):

    @patch('src.client.ProxmoxAPI')
    @patch.dict('os.environ', {
        'PROXMOX_URL': 'https://test.proxmox.com:8006',
        'PROXMOX_USER': 'root@pam',
        'PROXMOX_TOKEN_ID': 'test-id',
        'PROXMOX_TOKEN_SECRET': 'test-secret',
        'PROXMOX_VERIFY_SSL': 'false'
    })
    def test_delete_snapshot(self, mock_api_cls):
        mock_api_instance = MagicMock()
        mock_api_cls.return_value = mock_api_instance
        client = ProxmoxClient()
        
        # Execute
        client.delete_snapshot("pve1", 100, "qemu", "snap1")

        # Verify
        mock_api_instance.nodes("pve1").qemu(100).snapshot("snap1").delete.assert_called_once()
        print("✅ Test Delete Snapshot passé.")

    @patch('src.client.ProxmoxAPI')
    @patch.dict('os.environ', {
        'PROXMOX_URL': 'https://test.proxmox.com:8006',
        'PROXMOX_USER': 'root@pam',
        'PROXMOX_TOKEN_ID': 'test-id',
        'PROXMOX_TOKEN_SECRET': 'test-secret',
        'PROXMOX_VERIFY_SSL': 'false'
    })
    def test_unlock_machine(self, mock_api_cls):
        mock_api_instance = MagicMock()
        mock_api_cls.return_value = mock_api_instance
        client = ProxmoxClient()
        
        # Execute
        client.unlock_machine("pve1", 100)

        # Verify
        mock_api_instance.nodes("pve1").qemu(100).config.post.assert_called_with(delete='lock')
        print("✅ Test Unlock Machine passé.")

    @patch('src.client.ProxmoxAPI')
    @patch.dict('os.environ', {
        'PROXMOX_URL': 'https://test.proxmox.com:8006',
        'PROXMOX_USER': 'root@pam',
        'PROXMOX_TOKEN_ID': 'test-id',
        'PROXMOX_TOKEN_SECRET': 'test-secret',
        'PROXMOX_VERIFY_SSL': 'false'
    })
    def test_get_cluster_log(self, mock_api_cls):
        mock_api_instance = MagicMock()
        mock_api_cls.return_value = mock_api_instance
        client = ProxmoxClient()
        
        mock_api_instance.cluster.log.get.return_value = [{'t': 'msg1'}, {'t': 'msg2'}]

        # Execute
        logs = client.get_cluster_log(max_lines=10)

        # Verify
        mock_api_instance.cluster.log.get.assert_called_with(limit=10)
        self.assertEqual(len(logs), 2)
        print("✅ Test Get Cluster Log passé.")

if __name__ == '__main__':
    unittest.main()
