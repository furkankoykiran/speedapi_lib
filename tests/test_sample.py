import unittest
from speed_lib.api_client import SpeedAPIClient

class TestSpeedAPIClient(unittest.TestCase):

    def test_get_balance_sats(self):
        client = SpeedAPIClient(secret_key='your_secret_key', base_url='https://api.tryspeed.com')
        balance = client.get_balance_sats()
        self.assertIsInstance(balance, float)

if __name__ == '__main__':
    unittest.main()
