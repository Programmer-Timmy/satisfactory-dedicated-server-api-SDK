import requests

from .data.advanced_game_settings import AdvancedGameSettings
from .data.minimum_privilege_level import MinimumPrivilegeLevel
from .data.new_game_save import NewGameData
from .data.response import Response
from .data.server_options import ServerOptions
from .exceptions import APIError


class SatisfactoryAPI:
    """ A client for the Satisfactory Dedicated Server API """

    def __init__(self, host: str, port: int = 7777, auth_token: str = None):
        """
        Initialize the API client

        Parameters
        ----------
        host : str
            The hostname or IP address of the server
        port : int, optional
            The port to connect to, by default 7777
        auth_token : str, optional
            The authentication token, by default None.
            You can use the `password_login` or `passwordless_login` methods to request a token from the server.

        Raises
        ------
        APIError
            If the authentication token is invalid
        """
        self.host: str = host
        self.port: int = port
        self.auth_token: str | None = auth_token

        if self.auth_token:
            self.verify_authentication_token()

    def _post(self, function, data=None, files=None):
        """
        Post a request to the API

        :param function: The function to call
        :param data: The data to send
        :param files: The files to send
        :return: The response
        :rtype: dict

        :raises APIError: If the API returns an error
        """
        url = f"https://{self.host}:{self.port}/api/v1"
        headers = {'Content-Type': 'application/json'}

        if self.auth_token:
            headers['Authorization'] = f'Bearer {self.auth_token}'

        payload = {'function': function, 'data': data} if data else {'function': function}

        response = requests.post(url, json=payload, headers=headers, files=files, verify=False, stream=True)
        if response.status_code != 200 and response.status_code != 204:
            raise APIError(
                error_code=response.json().get('errorCode'),
                message=response.json().get('errorMessage')
            )

        if response.status_code == 204:
            return {}

        #  use switch
        match response.headers.get('Content-Type'):
            case 'application/json;charset=utf-8':
                if response.json().get('errorCode'):
                    raise APIError(response.json().get('errorMessage'))
                return response.json().get('data')
            case 'application/octet-stream':
                return response.content
            case _:
                return response.text

    def health_check(self, client_custom_data='') -> (
            Response):
        """
        Perform a health check on the server. This function is used to check if the server is running and if the API is.

        Parameters
        ----------
        client_custom_data : str
            Custom data to send to the server. Defaults to an empty string.

        Returns
        -------
        Response
            A Response containing the data returned by the API.

        Raises
        ------
        APIError
            If the API returns an error
        """
        response = self._post('HealthCheck', {'ClientCustomData': client_custom_data})
        return Response(success=True, data=response)

    def verify_authentication_token(self) -> Response:
        """
        Verify the authentication token

        Returns
        -------
        Response
            A Response containing the message 'Token is valid'.

        Raises
        ------
        APIError
            If the API returns an error or if the token is invalid.
        """
        self._post('VerifyAuthenticationToken')
        return Response(success=True, data={'message': 'Token is valid'})

    def passwordless_login(self, minimum_privilege_level: MinimumPrivilegeLevel) -> Response:
        """
        Perform a passwordless login and store the authentication token.

        Parameters
        ----------
        minimum_privilege_level : MinimumPrivilegeLevel
            The minimum privilege level required for the login.

        Returns
        -------
        Response
            A Response containing the message 'Successfully logged in, the token is now stored'.

        Raises
        ------
        APIError
            If the API returns an error or if the login is unsuccessful
            (e.g., incorrect password or insufficient privileges).
        """
        response = self._post('PasswordlessLogin', {'MinimumPrivilegeLevel': minimum_privilege_level.value})
        self.auth_token = response['authenticationToken']
        return Response(success=True, data={'message': 'Successfully logged in, the token is now stored'})

    def password_login(self, minimum_privilege_level: MinimumPrivilegeLevel, password: str) -> Response:
        """
        Perform a password login and store the authentication token.

        Parameters
        ----------
        minimum_privilege_level : MinimumPrivilegeLevel
            The minimum privilege level required for the login.
        password : str
            The password associated with the account. Must not be empty.

        Returns
        -------
        Response
            A Response containing the message 'Successfully logged in, the token is now stored'.

        Raises
        ------
        APIError
            If the API returns an error or if the login is unsuccessful
            (e.g., incorrect password or insufficient privileges).
        """
        response = self._post('PasswordLogin', {
            'MinimumPrivilegeLevel': minimum_privilege_level.value,
            'Password': password
        })
        self.auth_token = response['authenticationToken']
        return Response(success=True, data={'message': 'Successfully logged in, the token is now stored'})

    def query_server_state(self):
        """
        Query the server state

        Returns
        -------
        Response
            A Response containing the server state data.

        Raises
        ------
        APIError
            If the API returns an error.
        """
        response = self._post('QueryServerState')
        return Response(success=True, data=response)

    def get_server_options(self):
        """
        Get the server options

        Returns
        -------
        Response
            A Response containing the server options data.

        Raises
        ------
        APIError
            If the API returns an error.
        """
        response = self._post('GetServerOptions')
        return Response(success=True, data=response)

    def get_advanced_game_settings(self) -> Response:
        """
        Fetch advanced game settings.

        Returns
        -------
        Response
            A Response containing the advanced game settings.
        """
        response = self._post('GetAdvancedGameSettings')
        return Response(success=True, data=response)

    def apply_advanced_game_settings(self, settings: AdvancedGameSettings) -> Response:
        """
        Apply advanced game settings.

        Parameters
        ----------
        settings : AdvancedGameSettings
            The new advanced game settings to apply.

        Returns
        -------
        Response
            A Response indicating the success of the operation.
        """
        self._post('ApplyAdvancedGameSettings', {
            'AdvancedGameSettings': settings.to_dict()
        })
        return Response(success=True, data={
            'message': 'Successfully applied advanced game settings to the server.',
            'settings': settings.to_dict()
        })

    def claim_server(self, server_name: str, admin_password: str) -> Response:
        """
        Claim the server.

        Parameters
        ----------
        server_name : str
            The name of the server.
        admin_password : str
            The administrator password.

        Returns
        -------
        Response
            A Response containing the server claim result.
        """
        response = self._post('ClaimServer', {
            'ServerName': server_name,
            'AdminPassword': admin_password
        })
        return Response(success=True, data=response)

    def rename_server(self, server_name: str) -> Response:
        """
        Rename the server.

        Parameters
        ----------
        server_name : str
            The new name for the server.

        Returns
        -------
        Response
            A Response indicating the success of the operation.
        """
        response = self._post('RenameServer', {
            'ServerName': server_name
        })
        return Response(success=True, data=response)

    def set_client_password(self, password: str) -> Response:
        """
        Set the client password.

        Parameters
        ----------
        password : str
            The new client password.

        Returns
        -------
        Response
            A Response indicating the success of the operation.
        """
        response = self._post('SetClientPassword', {
            'Password': password
        })
        return Response(success=True, data=response)

    def set_admin_password(self, password: str, auth_token: str) -> Response:
        """
        Set the admin password.

        Parameters
        ----------
        password : str
            The new admin password.
        auth_token : str
            The authentication token.

        Returns
        -------
        Response
            A Response indicating the success of the operation.
        """
        response = self._post('SetAdminPassword', {
            'Password': password,
            'AuthenticationToken': auth_token
        })
        return Response(success=True, data=response)

    def set_auto_load_session_name(self, session_name: str) -> Response:
        """
        Set the auto-load session name. You can get session names by calling `enumerate_sessions` (You need admin privileges).

        Parameters
        ----------
        session_name : str
            The session name to auto-load.

        Returns
        -------
        Response
            A Response indicating the success of the operation.
        """
        response = self._post('SetAutoLoadSessionName', {
            'SessionName': session_name
        })
        return Response(success=True, data=response)

    def run_command(self, command: str) -> Response:
        """
        Run a server command.

        Parameters
        ----------
        command : str
            The command to run.

        Returns
        -------
        Response
            A Response containing the result of the command.
        """
        response = self._post('RunCommand', {
            'Command': command
        })
        return Response(success=True, data=response)

    def shutdown(self) -> Response:
        """
        Shut down the server.

        Returns
        -------
        Response
            A Response indicating the success of the operation.
        """
        self._post('Shutdown')
        return Response(success=True, data={
            'message': "Server is shutting down... Note: If the server is configured as a service and the restart "
                       "policy is set to 'always', it will restart automatically."
        })

    def apply_server_options(self, options: ServerOptions) -> Response:
        """
        Apply server options.

        Parameters
        ----------
        options : dict
            The server options to apply.

        Returns
        -------
        Response
            A Response indicating the success of the operation.
        """
        print(self._post('ApplyServerOptions', {
            'UpdatedServerOptions': options.to_dict()
        }))
        return Response(success=True, data={'message': 'Successfully applied server options to the server.',
                                            'options': options.to_dict()
                                            })

    def create_new_game(self, game_data: NewGameData) -> Response:
        """
        Create a new game.

        Parameters
        ----------
        game_data : NewGameData
            The data for the new game.

        Returns
        -------
        Response
            A Response indicating the success of the operation.
        """
        response = self._post('CreateNewGame', {
            'NewGameData': game_data.__dict__  # Convert dataclass to dict
        })
        return Response(success=True, data=response)

    def save_game(self, save_name: str) -> Response:
        """
        Save the game.

        Parameters
        ----------
        save_name : str
            The name of the save file.

        Returns
        -------
        Response
            A Response indicating the success of the save operation.
        """
        response = self._post('SaveGame', {
            'SaveName': save_name
        })
        return Response(success=True, data=response)

    def delete_save_file(self, save_name: str) -> Response:
        """
        Delete a save file.

        Parameters
        ----------
        save_name : str
            The name of the save file to delete.

        Returns
        -------
        Response
            A Response indicating the success of the operation.
        """
        response = self._post('DeleteSaveFile', {
            'SaveName': save_name
        })
        return Response(success=True, data=response)

    def delete_save_session(self, session_name: str) -> Response:
        """
        Delete a save session.

        Parameters
        ----------
        session_name : str
            The name of the session to delete.

        Returns
        -------
        Response
            A Response indicating the success of the operation.
        """
        response = self._post('DeleteSaveSession', {
            'SessionName': session_name
        })
        return Response(success=True, data=response)

    def enumerate_sessions(self) -> Response:
        """
        Enumerate available sessions. You need admin privileges to call this function.

        Returns
        -------
        Response
            A Response containing the available sessions.
        """
        response = self._post('EnumerateSessions')
        return Response(success=True, data=response)

    def load_game(self, save_name: str, enable_advanced_game_settings: bool = False) -> Response:
        """
        Load a saved game.

        Parameters
        ----------
        save_name : str
            The name of the save file to load.
        enable_advanced_game_settings : bool, optional
            Whether to enable advanced game settings (default is False).

        Returns
        -------
        Response
            A Response indicating the success of the load operation.
        """
        response = self._post('LoadGame', {
            'SaveName': save_name,
            'EnableAdvancedGameSettings': enable_advanced_game_settings
        })
        return Response(success=True, data=response)

    def upload_save_game(self, save_name: str, load_save_game: bool = False,
                         enable_advanced_game_settings: bool = False) -> Response:
        raise NotImplementedError('This method is not implemented yet')

    def download_save_game(self, save_name: str) -> Response:
        """
        Download a save game file.

        Parameters
        ----------
        save_name : str
            The name of the save file to download.

        Returns
        -------
        Response
            A Response indicating the success and the save game in bytes.
        """
        response = self._post('DownloadSaveGame', {
            'SaveName': save_name
        })
        return Response(success=True, data=response)
