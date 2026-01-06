import unittest
from unittest.mock import MagicMock, patch
from src.client import ProxmoxClient

class TestMigration(unittest.TestCase):

    @patch('src.client.ProxmoxAPI')
    @patch.dict('os.environ', {
        'PROXMOX_URL': 'https://test.proxmox.com:8006',
        'PROXMOX_USER': 'root@pam',
        'PROXMOX_TOKEN_ID': 'test-id',
        'PROXMOX_TOKEN_SECRET': 'test-secret',
        'PROXMOX_VERIFY_SSL': 'false'
    })
    def test_migrate_vm_offline(self, mock_api_cls):
        mock_api_instance = MagicMock()
        mock_api_cls.return_value = mock_api_instance
        client = ProxmoxClient()
        
        # Execute Offline Migration
        client.migrate_machine("node1", 100, "qemu", "node2", online=False)

        # Verify
        mock_api_instance.nodes("node1").qemu(100).migrate.post.assert_called_with(
            target="node2"
        )
        print("✅ Test Migration Offline VM passé.")

    @patch('src.client.ProxmoxAPI')
    @patch.dict('os.environ', {
        'PROXMOX_URL': 'https://test.proxmox.com:8006',
        'PROXMOX_USER': 'root@pam',
        'PROXMOX_TOKEN_ID': 'test-id',
        'PROXMOX_TOKEN_SECRET': 'test-secret',
        'PROXMOX_VERIFY_SSL': 'false'
    })
    def test_migrate_lxc_online(self, mock_api_cls):
        mock_api_instance = MagicMock()
        mock_api_cls.return_value = mock_api_instance
        client = ProxmoxClient()
        
        # Execute Online Migration
        client.migrate_machine("node1", 200, "lxc", "node2", online=True)

        # Verify
        mock_api_instance.nodes("node1").lxc(200).migrate.post.assert_called_with(
            target="node2",
            online=1,
            **{'with-local-disks': 1} # Cannot use hyphen in keyword arg directly in call
        )
        print("✅ Test Migration Online LXC passé.")

if __name__ == '__main__':
    unittest.main()
