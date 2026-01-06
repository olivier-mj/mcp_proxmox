import unittest
from unittest.mock import MagicMock, patch
from src.client import ProxmoxClient

class TestCloudInit(unittest.TestCase):

    @patch('src.client.ProxmoxAPI')
    @patch.dict('os.environ', {
        'PROXMOX_URL': 'https://test.proxmox.com:8006',
        'PROXMOX_USER': 'root@pam',
        'PROXMOX_TOKEN_ID': 'test-id',
        'PROXMOX_TOKEN_SECRET': 'test-secret',
        'PROXMOX_VERIFY_SSL': 'false'
    })
    def test_set_cloudinit_config(self, mock_api_cls):
        # Setup mock
        mock_api_instance = MagicMock()
        mock_api_cls.return_value = mock_api_instance
        
        client = ProxmoxClient()
        
        node = "pve1"
        vmid = 105
        user = "devops"
        password = "secretpassword"
        ssh_keys = "ssh-rsa AAAAB3Nza..."
        ip_config = "ip=192.168.1.50/24,gw=192.168.1.1"

        # Execute
        client.set_cloudinit_config(node, vmid, user, password, ssh_keys, ip_config)

        # Verify
        mock_api_instance.nodes.assert_called_with(node)
        mock_api_instance.nodes(node).qemu.assert_called_with(vmid)
        mock_api_instance.nodes(node).qemu(vmid).config.post.assert_called_with(
            ciuser=user,
            cipassword=password,
            sshkeys=ssh_keys,
            ipconfig0=ip_config
        )
        print("✅ Test Cloud-Init config passé avec succès.")

    @patch('src.client.ProxmoxAPI')
    @patch.dict('os.environ', {
        'PROXMOX_URL': 'https://test.proxmox.com:8006',
        'PROXMOX_USER': 'root@pam',
        'PROXMOX_TOKEN_ID': 'test-id',
        'PROXMOX_TOKEN_SECRET': 'test-secret',
        'PROXMOX_VERIFY_SSL': 'false'
    })
    def test_set_cloudinit_config_partial(self, mock_api_cls):
        # Setup mock
        mock_api_instance = MagicMock()
        mock_api_cls.return_value = mock_api_instance
        
        client = ProxmoxClient()
        
        node = "pve1"
        vmid = 106
        user = "admin"

        # Execute only user change
        client.set_cloudinit_config(node, vmid, ciuser=user)

        # Verify
        mock_api_instance.nodes(node).qemu(vmid).config.post.assert_called_with(
            ciuser=user
        )
        print("✅ Test Cloud-Init partiel passé avec succès.")

if __name__ == '__main__':
    unittest.main()
