import unittest
from unittest.mock import MagicMock, patch
from src.client import ProxmoxClient

class TestResources(unittest.TestCase):

    @patch('src.client.ProxmoxAPI')
    @patch.dict('os.environ', {
        'PROXMOX_URL': 'https://test.proxmox.com:8006',
        'PROXMOX_USER': 'root@pam',
        'PROXMOX_TOKEN_ID': 'test-id',
        'PROXMOX_TOKEN_SECRET': 'test-secret',
        'PROXMOX_VERIFY_SSL': 'false'
    })
    def test_resize_vm(self, mock_api_cls):
        mock_api_instance = MagicMock()
        mock_api_cls.return_value = mock_api_instance
        client = ProxmoxClient()
        
        client.resize_machine_resources("node1", 100, "qemu", cores=4, memory=4096)
        
        mock_api_instance.nodes("node1").qemu(100).config.post.assert_called_with(
            cores=4,
            memory=4096
        )
        print("✅ Test Resize VM (cores & mem) passé.")

    @patch('src.client.ProxmoxAPI')
    @patch.dict('os.environ', {
        'PROXMOX_URL': 'https://test.proxmox.com:8006',
        'PROXMOX_USER': 'root@pam',
        'PROXMOX_TOKEN_ID': 'test-id',
        'PROXMOX_TOKEN_SECRET': 'test-secret',
        'PROXMOX_VERIFY_SSL': 'false'
    })
    def test_resize_lxc_mem_only(self, mock_api_cls):
        mock_api_instance = MagicMock()
        mock_api_cls.return_value = mock_api_instance
        client = ProxmoxClient()
        
        client.resize_machine_resources("node1", 200, "lxc", memory=1024)
        
        mock_api_instance.nodes("node1").lxc(200).config.post.assert_called_with(
            memory=1024
        )
        print("✅ Test Resize LXC (mem only) passé.")

if __name__ == '__main__':
    unittest.main()
