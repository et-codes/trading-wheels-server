import os
import requests
import unittest
from dotenv import load_dotenv


load_dotenv()
SERVER_URL = os.environ.get('SERVER_URL')
TEST_USERNAME = os.environ.get('TEST_USERNAME')
TEST_PASSWORD = os.environ.get('TEST_PASSWORD')


class TradeTests(unittest.TestCase):

    def setUp(self):
        self._test_user = {
            'username': TEST_USERNAME,
            'password': TEST_PASSWORD
        }

        # Create test user if it doesn't already exist
        url = f'{SERVER_URL}/user/{TEST_USERNAME}'
        response = requests.get(url)
        if response.text != TEST_USERNAME:
            url = f'{SERVER_URL}/user'
            requests.post(url, json=self._test_user)
        
        self.header = self.login_get_auth_header()

    def tearDown(self):
        # Logout test user
        url = f'{SERVER_URL}/user/logout/{TEST_USERNAME}'
        requests.get(url, headers=self.header)

    def test_get_trade_by_id(self):
        trades = self.get_trades_by_username(TEST_USERNAME)

        url = f'{SERVER_URL}/trade/id/{trades[0]["id"]}'
        response = requests.get(url, headers=self.header)
        trade = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(trade, dict)
        self.assertGreaterEqual(trade['shares'], 1)

    def test_get_trades_by_username(self):
        trades = self.get_trades_by_username(TEST_USERNAME)

        self.assertIsInstance(trades, list)
        self.assertGreaterEqual(len(trades), 1)
        self.assertGreaterEqual(trades[0]['shares'], 1)
    
    def get_trades_by_username(self, username):
        url = f'{SERVER_URL}/trade/user/{username}'
        response = requests.get(url, headers=self.header)
        return response.json()

    def test_trade(self):
        url = f'{SERVER_URL}/trade'
        trade_obj = {
            'username': TEST_USERNAME,
            'symbol': 'AAPL',
            'shares': 100,
            'price': 12.34
        }
        response = requests.post(url, json=trade_obj, headers=self.header)
        trades = response.json()

        self.assertEqual(response.status_code, 201)
        self.assertIsInstance(trades, list)
        self.assertEqual(len(trades), 2)

        self.delete_trades(trades)

    def delete_trades(self, trades):
        for trade in trades:
            url = f"{SERVER_URL}/trade/id/{trade['id']}"
            requests.delete(url, headers=self.header)
    
    def login_get_auth_header(self):
        url = f'{SERVER_URL}/user/login'
        response = requests.post(url, json=self._test_user)
        token = response.text
        header = {'Authorization': f'Bearer {token}'}
        return header


if __name__ == '__main__':
    unittest.main()