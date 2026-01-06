import unittest
from unittest.mock import MagicMock, patch
from src.client import ProxmoxClient

class TestISOManagement(unittest.TestCase):

    @patch('src.client.ProxmoxAPI')
    @patch.dict('os.environ', {
        'PROXMOX_URL': 'https://test.proxmox.com:8006',
        'PROXMOX_USER': 'root@pam',
        'PROXMOX_TOKEN_ID': 'test-id',
        'PROXMOX_TOKEN_SECRET': 'test-secret',
        'PROXMOX_VERIFY_SSL': 'false'
    })
    def test_list_isos(self, mock_api_cls):
        mock_api_instance = MagicMock()
        mock_api_cls.return_value = mock_api_instance
        client = ProxmoxClient()
        
        # Mock return data
        mock_api_instance.nodes("pve").storage("local").content.get.return_value = [
            {'volid': 'local:iso/ubuntu.iso', 'size': 1024**3}
        ]

        # Execute
        isos = client.list_isos("pve", "local")

        # Verify
        mock_api_instance.nodes("pve").storage("local").content.get.assert_called_with(content='iso')
        self.assertEqual(len(isos), 1)
        print("✅ Test List ISOs passé.")

    @patch('src.client.ProxmoxAPI')
    @patch.dict('os.environ', {
        'PROXMOX_URL': 'https://test.proxmox.com:8006',
        'PROXMOX_USER': 'root@pam',
        'PROXMOX_TOKEN_ID': 'test-id',
        'PROXMOX_TOKEN_SECRET': 'test-secret',
        'PROXMOX_VERIFY_SSL': 'false'
    })
    def test_download_iso(self, mock_api_cls):
        mock_api_instance = MagicMock()
        mock_api_cls.return_value = mock_api_instance
        client = ProxmoxClient()
        
        url = "http://archive.ubuntu.com/ubuntu.iso"
        filename = "ubuntu-24.04.iso"

        # Execute
        client.download_iso("pve", "local", url, filename)

        # Verify
        mock_api_instance.nodes("pve").storage("local").download_url.post.assert_called_with(
            content='iso',
            filename=filename,
            url=url
        )
        print("✅ Test Download ISO passé.")

    @patch('src.client.ProxmoxAPI')
    @patch.dict('os.environ', {
        'PROXMOX_URL': 'https://test.proxmox.com:8006',
        'PROXMOX_USER': 'root@pam',
        'PROXMOX_TOKEN_ID': 'test-id',
        'PROXMOX_TOKEN_SECRET': 'test-secret',
        'PROXMOX_VERIFY_SSL': 'false'
    })
    def test_download_iso_bad_extension(self, mock_api_cls):
        client = ProxmoxClient()
        with self.assertRaises(ValueError):
            client.download_iso("pve", "local", "http://site.com/file", "image.img")
        print("✅ Test Download Bad Extension passé.")

if __name__ == '__main__':
    unittest.main()
