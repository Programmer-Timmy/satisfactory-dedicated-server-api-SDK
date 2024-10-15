import unittest
from unittest.mock import patch, MagicMock
from satisfactory_api_client import SatisfactoryAPI
from satisfactory_api_client.data import Response, MinimumPrivilegeLevel, AdvancedGameSettings
from satisfactory_api_client.data.server_options import ServerOptions


class TestApiFunctions(unittest.TestCase):

    def setUp(self):
        # Create a mock response object
        self.mock_response = MagicMock()
        self.mock_response.status_code = 200  # Set status code to 200
        self.mock_response.json.return_value = {"data": {"status": "ok"}}
        self.mock_response.headers = {'Content-Type': 'application/json;charset=utf-8'}  # Set the JSON response

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
            verify=False,
            stream=True
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
            verify=False,
            stream=True
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
            json={'function': 'PasswordLogin', 'data': {'MinimumPrivilegeLevel': 'Administrator', 'Password': 'password'}},
            headers={'Content-Type': 'application/json'},
            files=None,
            verify=False,
            stream=True
        )

    @patch('satisfactory_api_client.api_client.requests.post')
    def test_verify_authentication_token(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": {"status": "ok"}}
        mock_response.headers = {'Content-Type': 'application/json;charset=utf-8'}

        mock_post.return_value = mock_response

        api = SatisfactoryAPI("localhost")
        response = api.verify_authentication_token()

        self.assertEqual(response, Response(success=True, data={'message': 'Token is valid'}))

        mock_post.assert_called_once_with(
            'https://localhost:7777/api/v1',
            json={'function': 'VerifyAuthenticationToken'},
            headers={'Content-Type': 'application/json'},
            files=None,
            verify=False,
            stream=True
        )

    @patch('satisfactory_api_client.api_client.requests.post')
    def test_query_server_state(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": {"status": "ok"}}
        mock_response.headers = {'Content-Type': 'application/json;charset=utf-8'}

        mock_post.return_value = mock_response

        api = SatisfactoryAPI("localhost")
        response = api.query_server_state()

        self.assertEqual(response, Response(success=True, data={'status': 'ok'}))

        mock_post.assert_called_once_with(
            'https://localhost:7777/api/v1',
            json={'function': 'QueryServerState'},
            headers={'Content-Type': 'application/json'},
            files=None,
            verify=False,
            stream=True
        )

    @patch('satisfactory_api_client.api_client.requests.post')
    def test_get_server_options(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": {"status": "ok"}}
        mock_response.headers = {'Content-Type': 'application/json;charset=utf-8'}

        mock_post.return_value = mock_response

        api = SatisfactoryAPI("localhost")
        response = api.get_server_options()

        self.assertEqual(response, Response(success=True, data={'status': 'ok'}))

        mock_post.assert_called_once_with(
            'https://localhost:7777/api/v1',
            json={'function': 'GetServerOptions'},
            headers={'Content-Type': 'application/json'},
            files=None,
            verify=False,
            stream=True
        )

    @patch('satisfactory_api_client.api_client.requests.post')
    def test_get_advanced_game_settings(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": {"status": "ok"}}
        mock_response.headers = {'Content-Type': 'application/json;charset=utf-8'}

        mock_post.return_value = mock_response

        api = SatisfactoryAPI("localhost")
        response = api.get_advanced_game_settings()

        self.assertEqual(response, Response(success=True, data={'status': 'ok'}))

        mock_post.assert_called_once_with(
            'https://localhost:7777/api/v1',
            json={'function': 'GetAdvancedGameSettings'},
            headers={'Content-Type': 'application/json'},
            files=None,
            verify=False,
            stream=True
        )

    @patch('satisfactory_api_client.api_client.requests.post')
    def test_apply_advanced_game_settings(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": {"status": "ok"}}
        mock_response.headers = {'Content-Type': 'application/json;charset=utf-8'}

        mock_post.return_value = mock_response

        api = SatisfactoryAPI("localhost")

        advanced_game_settings = AdvancedGameSettings(
            NoPower=True,
            DisableArachnidCreatures=True,
            NoUnlockCost=True,
            SetGamePhase=1,
            GiveAllTiers=True,
            UnlockAllResearchSchematics=True,
            UnlockInstantAltRecipes=True,
            UnlockAllResourceSinkSchematics=True,
            GiveItems='empty',
            NoBuildCost=True,
            GodMode=True,
            FlightMode=True
        )



        response = api.apply_advanced_game_settings(advanced_game_settings)

        self.assertEqual(
            response,
            Response(
                success=True,
                data={
                    'message': 'Successfully applied advanced game settings to the server.',
                    'settings': advanced_game_settings.to_dict()
                }
            )
        )

        mock_post.assert_called_once_with(
            'https://localhost:7777/api/v1',
            json={'function': 'ApplyAdvancedGameSettings',
                  'data': {'AdvancedGameSettings': advanced_game_settings.to_dict()}
                  },
            headers={'Content-Type': 'application/json'},
            files=None,
            verify=False,
            stream=True
        )

    @patch('satisfactory_api_client.api_client.requests.post')
    def test_claim_server(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": {"status": "ok"}}
        mock_response.headers = {'Content-Type': 'application/json;charset=utf-8'}

        mock_post.return_value = mock_response

        api = SatisfactoryAPI("localhost")
        response = api.claim_server('server_name', 'server_password')

        self.assertEqual(response, Response(success=True, data={'status': 'ok'}))

        mock_post.assert_called_once_with(
            'https://localhost:7777/api/v1',
            json={'function': 'ClaimServer', 'data': {'ServerName': 'server_name', 'AdminPassword': 'server_password'}},
            headers={'Content-Type': 'application/json'},
            files=None,
            verify=False,
            stream=True
        )

    @patch('satisfactory_api_client.api_client.requests.post')
    def test_rename_server(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": {"status": "ok"}}
        mock_response.headers = {'Content-Type': 'application/json;charset=utf-8'}

        mock_post.return_value = mock_response

        api = SatisfactoryAPI("localhost")
        response = api.rename_server('server_name')

        self.assertEqual(response, Response(success=True, data={'status': 'ok'}))

        mock_post.assert_called_once_with(
            'https://localhost:7777/api/v1',
            json={'function': 'RenameServer', 'data': {'ServerName': 'server_name'}},
            headers={'Content-Type': 'application/json'},
            files=None,
            verify=False,
            stream=True
        )

    @patch('satisfactory_api_client.api_client.requests.post')
    def test_set_client_password(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": {"status": "ok"}}
        mock_response.headers = {'Content-Type': 'application/json;charset=utf-8'}

        mock_post.return_value = mock_response

        api = SatisfactoryAPI("localhost")
        response = api.set_client_password('password')

        self.assertEqual(response, Response(success=True, data={'status': 'ok'}))

        mock_post.assert_called_once_with(
            'https://localhost:7777/api/v1',
            json={'function': 'SetClientPassword', 'data': {'Password': 'password'}},
            headers={'Content-Type': 'application/json'},
            files=None,
            verify=False,
            stream=True
        )

    @patch('satisfactory_api_client.api_client.requests.post')
    def test_set_admin_password(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": {"status": "ok"}}
        mock_response.headers = {'Content-Type': 'application/json;charset=utf-8'}

        mock_post.return_value = mock_response

        api = SatisfactoryAPI("localhost")
        response = api.set_admin_password('password', 'new_admin_token')

        self.assertEqual(response, Response(success=True, data={'status': 'ok'}))

        mock_post.assert_called_once_with(
            'https://localhost:7777/api/v1',
            json={'function': 'SetAdminPassword',
                  'data': {'Password': 'password', 'AuthenticationToken': 'new_admin_token'}
                  },
            headers={'Content-Type': 'application/json'},
            files=None,
            verify=False,
            stream=True
        )

    @patch('satisfactory_api_client.api_client.requests.post')
    def test_set_auto_load_session_name(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": {"status": "ok"}}
        mock_response.headers = {'Content-Type': 'application/json;charset=utf-8'}

        mock_post.return_value = mock_response

        api = SatisfactoryAPI("localhost")
        response = api.set_auto_load_session_name('session_name')

        self.assertEqual(response, Response(success=True, data={'status': 'ok'}))

        mock_post.assert_called_once_with(
            'https://localhost:7777/api/v1',
            json={'function': 'SetAutoLoadSessionName', 'data': {'SessionName': 'session_name'}},
            headers={'Content-Type': 'application/json'},
            files=None,
            verify=False,
            stream=True
        )

    @patch('satisfactory_api_client.api_client.requests.post')
    def test_run_command(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": {"status": "ok"}}
        mock_response.headers = {'Content-Type': 'application/json;charset=utf-8'}

        mock_post.return_value = mock_response

        api = SatisfactoryAPI("localhost")
        response = api.run_command('command')

        self.assertEqual(response, Response(success=True, data={'status': 'ok'}))

        mock_post.assert_called_once_with(
            'https://localhost:7777/api/v1',
            json={'function': 'RunCommand', 'data': {'Command': 'command'}},
            headers={'Content-Type': 'application/json'},
            files=None,
            verify=False,
            stream=True
        )

    @patch('satisfactory_api_client.api_client.requests.post')
    def test_shutdown(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": {"status": "ok"}}
        mock_response.headers = {'Content-Type': 'application/json;charset=utf-8'}

        mock_post.return_value = mock_response

        api = SatisfactoryAPI("localhost")
        response = api.shutdown()

        self.assertEqual(response, Response(success=True, data={'message': "Server is shutting down... Note: If the "
                                                                           "server is configured as a service and the "
                                                                           "restart policy is set to 'always', "
                                                                           "it will restart automatically."
                                                                }
                                            )
                         )

        mock_post.assert_called_once_with(
            'https://localhost:7777/api/v1',
            json={'function': 'Shutdown'},
            headers={'Content-Type': 'application/json'},
            files=None,
            verify=False,
            stream=True
        )

    @patch('satisfactory_api_client.api_client.requests.post')
    def test_apply_server_options(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": {"status": "ok"}}
        mock_response.headers = {'Content-Type': 'application/json;charset=utf-8'}

        mock_post.return_value = mock_response

        server_options = ServerOptions(
            DSAutoPause=True,
            DSAutoSaveOnDisconnect=True,
            AutosaveInterval=300,
            ServerRestartTimeSlot=0,
            SendGameplayData=True,
            NetworkQuality=0
        )


        api = SatisfactoryAPI("localhost")
        response = api.apply_server_options(server_options)

        self.assertEqual(response, Response(success=True, data={"message": "Successfully applied server options to the server.",
                                                                "options": server_options.to_dict()
                                                                }))

        mock_post.assert_called_once_with(
            'https://localhost:7777/api/v1',
            json={'function': 'ApplyServerOptions', 'data': {'UpdatedServerOptions': server_options.to_dict()}},
            headers={'Content-Type': 'application/json'},
            files=None,
            verify=False,
            stream=True
        )

#     TODO: add test for savegames

if __name__ == "__main__":
    unittest.main()
