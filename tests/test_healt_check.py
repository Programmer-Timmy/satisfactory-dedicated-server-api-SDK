import unittest
from satisfactory_ds_api.api_client import SatisfactoryAPI
from satisfactory_ds_api.data.response import Response


class TestHealthCheck(unittest.TestCase):
    def test_health_check(self):
        client = SatisfactoryAPI("localhost")
        response = client.health_check()
        self.assertIsInstance(response, Response)

    # Other tests...

if __name__ == "__main__":
    unittest.main()
