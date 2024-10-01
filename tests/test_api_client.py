import unittest

from satisfactory_ds_api.api_client import SatisfactoryAPI
from satisfactory_ds_api.data.response import Response


class TestAPIClient(unittest.TestCase):
    def test_initialization(self):
        client = SatisfactoryAPI("localhost")
        self.assertEqual(client.host, "localhost")
        self.assertEqual(client.port, 7777)

    def test_initialization_with_port(self):
        client = SatisfactoryAPI("localhost", port=1234)
        self.assertEqual(client.port, 1234)

    def test_initialization_with_auth_token(self):
        client = SatisfactoryAPI("localhost", auth_token="1234")
        self.assertEqual(client.auth_token, "1234")

    def test_post(self):
        client = SatisfactoryAPI("localhost")
        response = client._post('HealthCheck', data={'ClientCustomData': ''})
        self.assertIsInstance(response, dict)

if __name__ == "__main__":
    unittest.main()
