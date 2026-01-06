import unittest
from unittest.mock import MagicMock, patch
from src.client import ProxmoxClient

class TestTags(unittest.TestCase):

    @patch('src.client.ProxmoxAPI')
    @patch.dict('os.environ', {
        'PROXMOX_URL': 'https://test.proxmox.com:8006',
        'PROXMOX_USER': 'root@pam',
        'PROXMOX_TOKEN_ID': 'test-id',
        'PROXMOX_TOKEN_SECRET': 'test-secret',
        'PROXMOX_VERIFY_SSL': 'false'
    })
    def test_add_tags(self, mock_api_cls):
        mock_api_instance = MagicMock()
        mock_api_cls.return_value = mock_api_instance
        client = ProxmoxClient()
        
        # Execute
        client.set_machine_tags("pve1", 100, "qemu", "prod,webserver")

        # Verify
        mock_api_instance.nodes("pve1").qemu(100).config.post.assert_called_with(
            tags="prod,webserver"
        )
        print("✅ Test Set Tags passé.")

if __name__ == '__main__':
    unittest.main()
