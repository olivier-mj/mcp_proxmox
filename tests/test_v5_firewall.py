import unittest
from unittest.mock import MagicMock, patch
from src.client import ProxmoxClient

class TestFirewall(unittest.TestCase):

    @patch('src.client.ProxmoxAPI')
    @patch.dict('os.environ', {
        'PROXMOX_URL': 'https://test.proxmox.com:8006',
        'PROXMOX_USER': 'root@pam',
        'PROXMOX_TOKEN_ID': 'test-id',
        'PROXMOX_TOKEN_SECRET': 'test-secret',
        'PROXMOX_VERIFY_SSL': 'false'
    })
    def test_get_firewall_rules(self, mock_api_cls):
        mock_api_instance = MagicMock()
        mock_api_cls.return_value = mock_api_instance
        client = ProxmoxClient()
        
        # Mock return data for firewall rules
        mock_rules = [
            {'pos': 0, 'enable': 1, 'action': 'ACCEPT', 'type': 'in', 'proto': 'tcp', 'dport': '80'},
            {'pos': 1, 'enable': 1, 'action': 'DROP', 'type': 'in'}
        ]
        mock_api_instance.nodes("pve1").qemu(100).firewall.rules.get.return_value = mock_rules

        # Execute
        rules = client.get_firewall_rules("pve1", 100, "qemu")

        # Verify
        mock_api_instance.nodes("pve1").qemu(100).firewall.rules.get.assert_called_once()
        self.assertEqual(len(rules), 2)
        self.assertEqual(rules[0]['action'], 'ACCEPT')
        print("✅ Test Get Firewall Rules passé.")

    @patch('src.client.ProxmoxAPI')
    @patch.dict('os.environ', {
        'PROXMOX_URL': 'https://test.proxmox.com:8006',
        'PROXMOX_USER': 'root@pam',
        'PROXMOX_TOKEN_ID': 'test-id',
        'PROXMOX_TOKEN_SECRET': 'test-secret',
        'PROXMOX_VERIFY_SSL': 'false'
    })
    def test_add_firewall_rule(self, mock_api_cls):
        mock_api_instance = MagicMock()
        mock_api_cls.return_value = mock_api_instance
        client = ProxmoxClient()
        
        # Execute
        client.add_firewall_rule(
            node="pve1", 
            vmid=100, 
            machine_type="qemu",
            action="ACCEPT",
            rule_type="in",
            proto="tcp",
            dport="443"
        )

        # Verify
        mock_api_instance.nodes("pve1").qemu(100).firewall.rules.post.assert_called_with(
            action="ACCEPT",
            type="in",
            proto="tcp",
            dport="443",
            enable=1
        )
        print("✅ Test Add Firewall Rule passé.")

if __name__ == '__main__':
    unittest.main()
