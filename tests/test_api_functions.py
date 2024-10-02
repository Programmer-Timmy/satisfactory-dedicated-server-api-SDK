import unittest
from unittest.mock import patch, MagicMock
from satisfactory_api_client import SatisfactoryAPI
from satisfactory_api_client.data import Response, MinimumPrivilegeLevel, AdvancedGameSettings
from satisfactory_api_client.data.advanced_game_settings import AdvancedGameRules


class TestApiFunctions(unittest.TestCase):

    def setUp(self):
        # Create a mock response object
        self.mock_response = MagicMock()
        self.mock_response.status_code = 200  # Set status code to 200
        self.mock_response.json.return_value = {"data": {"status": "ok"}}  # Set the JSON response

    @patch('satisfactory_api_client.api_client.requests.post')
    def test_health_check(self, mock_post):
        # Configure the mock to return the mock response
        mock_post.return_value = self.mock_response

        api = SatisfactoryAPI("localhost")  # Initialize the API client
        response = api.health_check()  # Call the method to test

        # Assert that the response matches the expected value
        self.assertEqual(response, Response(success=True, data={"status": "ok"}))

        # Assert that requests.post was called with the correct arguments
        mock_post.assert_called_once_with(
            'https://localhost:7777/api/v1',
            json={'function': 'HealthCheck', 'data': {'ClientCustomData': ''}},
            headers={'Content-Type': 'application/json'},
            files=None,
            verify=False
        )

    @patch('satisfactory_api_client.api_client.requests.post')
    def test_passwordless_login(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": {"authenticationToken": "1234"}}

        mock_post.return_value = mock_response

        api = SatisfactoryAPI("localhost")
        response = api.passwordless_login(minimum_privilege_level=MinimumPrivilegeLevel.CLIENT)

        self.assertEqual(response,
                         Response(success=True, data={'message': 'Successfully logged in, the token is now stored'}))

        mock_post.assert_called_once_with(
            'https://localhost:7777/api/v1',
            json={'function': 'PasswordlessLogin', 'data': {'MinimumPrivilegeLevel': 'Client'}},
            headers={'Content-Type': 'application/json'},
            files=None,
            verify=False
        )

    @patch('satisfactory_api_client.api_client.requests.post')
    def test_password_login(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": {"authenticationToken": "1234"}}

        mock_post.return_value = mock_response

        api = SatisfactoryAPI("localhost")
        response = api.password_login(minimum_privilege_level=MinimumPrivilegeLevel.ADMINISTRATOR, password="password")

        self.assertEqual(response,
                         Response(success=True, data={'message': 'Successfully logged in, the token is now stored'}))

        mock_post.assert_called_once_with(
            'https://localhost:7777/api/v1',
            json={'function': 'PasswordLogin',
                  'data': {'MinimumPrivilegeLevel': 'Administrator', 'Password': 'password'}},
            headers={'Content-Type': 'application/json'},
            files=None,
            verify=False
        )

    @patch('satisfactory_api_client.api_client.requests.post')
    def test_verify_authentication_token(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": {"status": "ok"}}

        mock_post.return_value = mock_response

        api = SatisfactoryAPI("localhost")
        response = api.verify_authentication_token()

        self.assertEqual(response, Response(success=True, data={'message': 'Token is valid'}))

        mock_post.assert_called_once_with(
            'https://localhost:7777/api/v1',
            json={'function': 'VerifyAuthenticationToken'},
            headers={'Content-Type': 'application/json'},
            files=None,
            verify=False
        )

    @patch('satisfactory_api_client.api_client.requests.post')
    def test_query_server_state(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": {"status": "ok"}}

        mock_post.return_value = mock_response

        api = SatisfactoryAPI("localhost")
        response = api.query_server_state()

        self.assertEqual(response, Response(success=True, data={'status': 'ok'}))

        mock_post.assert_called_once_with(
            'https://localhost:7777/api/v1',
            json={'function': 'QueryServerState'},
            headers={'Content-Type': 'application/json'},
            files=None,
            verify=False
        )

    @patch('satisfactory_api_client.api_client.requests.post')
    def test_get_server_options(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": {"status": "ok"}}

        mock_post.return_value = mock_response

        api = SatisfactoryAPI("localhost")
        response = api.get_server_options()

        self.assertEqual(response, Response(success=True, data={'status': 'ok'}))

        mock_post.assert_called_once_with(
            'https://localhost:7777/api/v1',
            json={'function': 'GetServerOptions'},
            headers={'Content-Type': 'application/json'},
            files=None,
            verify=False
        )

    @patch('satisfactory_api_client.api_client.requests.post')
    def test_get_advanced_game_settings(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": {"status": "ok"}}

        mock_post.return_value = mock_response

        api = SatisfactoryAPI("localhost")
        response = api.get_advanced_game_settings()

        self.assertEqual(response, Response(success=True, data={'status': 'ok'}))

        mock_post.assert_called_once_with(
            'https://localhost:7777/api/v1',
            json={'function': 'GetAdvancedGameSettings'},
            headers={'Content-Type': 'application/json'},
            files=None,
            verify=False
        )

    @patch('satisfactory_api_client.api_client.requests.post')
    def test_apply_advanced_game_settings(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": {"status": "ok"}}

        mock_post.return_value = mock_response

        api = SatisfactoryAPI("localhost")

        advanced_game_settings = AdvancedGameSettings(
            creativeModeEnabled=True,
            advancedGameSettings=AdvancedGameRules(
                NoPower=True,
                DisableArachnidCreatures=True,
                NoUnlockCost=True,
                SetGamePhase='1',
                GiveAllTiers=True,
                UnlockAllResearchSchematics=True,
                UnlockInstantAltRecipes=True,
                UnlockAllResourceSinkSchematics=True,
                GiveItems='empty',
                NoBuildCost=True,
                GodMode=True,
                FlightMode=True
            )
        )

        response = api.apply_advanced_game_settings(advanced_game_settings)

        self.assertEqual(
            response,
            Response(
                success=True,
                data={
                    'message': 'Successfully applied advanced game settings to the server.',
                    'settings': advanced_game_settings
                }
            )
        )

        mock_post.assert_called_once_with(
            'https://localhost:7777/api/v1',
            json={'function': 'ApplyAdvancedGameSettings'},
            headers={'Content-Type': 'application/json'},
            files=None,
            verify=False
        )


if __name__ == "__main__":
    unittest.main()
