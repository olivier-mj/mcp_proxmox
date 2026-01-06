import unittest
from unittest.mock import MagicMock, patch
from src.client import ProxmoxClient

class TestAnalyst(unittest.TestCase):

    @patch('src.client.ProxmoxAPI')
    @patch.dict('os.environ', {
        'PROXMOX_URL': 'https://test.proxmox.com:8006',
        'PROXMOX_USER': 'root@pam',
        'PROXMOX_TOKEN_ID': 'test-id',
        'PROXMOX_TOKEN_SECRET': 'test-secret',
        'PROXMOX_VERIFY_SSL': 'false'
    })
    def test_get_rrd_data(self, mock_api_cls):
        mock_api_instance = MagicMock()
        mock_api_cls.return_value = mock_api_instance
        client = ProxmoxClient()
        
        # Mock data (list of points)
        mock_data = [
            {'time': 1700000000, 'cpu': 0.1, 'mem': 1024},
            {'time': 1700000060, 'cpu': 0.2, 'mem': 2048}
        ]
        mock_api_instance.nodes("pve1").qemu(100).rrddata.get.return_value = mock_data

        # Execute
        data = client.get_machine_rrd_data("pve1", 100, "qemu", timeframe="hour")

        # Verify
        mock_api_instance.nodes("pve1").qemu(100).rrddata.get.assert_called_with(timeframe="hour")
        self.assertEqual(len(data), 2)
        print("✅ Test RRD Data (VM) passé.")

    @patch('src.client.ProxmoxAPI')
    @patch.dict('os.environ', {
        'PROXMOX_URL': 'https://test.proxmox.com:8006',
        'PROXMOX_USER': 'root@pam',
        'PROXMOX_TOKEN_ID': 'test-id',
        'PROXMOX_TOKEN_SECRET': 'test-secret',
        'PROXMOX_VERIFY_SSL': 'false'
    })
    def test_get_lxc_templates(self, mock_api_cls):
        mock_api_instance = MagicMock()
        mock_api_cls.return_value = mock_api_instance
        client = ProxmoxClient()
        
        mock_templates = [
            {'template': 'ubuntu-22.04-standard_22.04-1_amd64.tar.zst', 'description': 'Ubuntu 22.04'},
            {'template': 'alpine-3.18-default_20230622_amd64.tar.xz', 'description': 'Alpine 3.18'}
        ]
        # pveam available usually called on node level
        mock_api_instance.nodes("pve1").aplinfo.get.return_value = mock_templates

        # Execute
        templates = client.list_lxc_templates("pve1")

        # Verify
        mock_api_instance.nodes("pve1").aplinfo.get.assert_called_once()
        self.assertEqual(len(templates), 2)
        print("✅ Test List LXC Templates passé.")

    @patch('src.client.ProxmoxAPI')
    @patch.dict('os.environ', {
        'PROXMOX_URL': 'https://test.proxmox.com:8006',
        'PROXMOX_USER': 'root@pam',
        'PROXMOX_TOKEN_ID': 'test-id',
        'PROXMOX_TOKEN_SECRET': 'test-secret',
        'PROXMOX_VERIFY_SSL': 'false'
    })
    def test_download_lxc_template(self, mock_api_cls):
        mock_api_instance = MagicMock()
        mock_api_cls.return_value = mock_api_instance
        client = ProxmoxClient()
        
        # Execute
        client.download_lxc_template("pve1", "local", "alpine-3.18")

        # Verify
        mock_api_instance.nodes("pve1").aplinfo.post.assert_called_with(
            storage="local",
            template="alpine-3.18"
        )
        print("✅ Test Download LXC Template passé.")

if __name__ == '__main__':
    unittest.main()
