import unittest
from satisfactory_api_client.api_client import SatisfactoryAPI
class TestAPIClient(unittest.TestCase):
    def test_initialization(self):
        client = SatisfactoryAPI("localhost")
        self.assertEqual(client.host, "localhost")
        self.assertEqual(client.port, 7777)

    def test_initialization_with_port(self):
        client = SatisfactoryAPI("localhost", port=1234)
        self.assertEqual(client.port, 1234)


if __name__ == "__main__":
    unittest.main()
