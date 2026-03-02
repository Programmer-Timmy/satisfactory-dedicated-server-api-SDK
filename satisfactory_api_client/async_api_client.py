import asyncio
import os
import ssl

import aiohttp

from .data.advanced_game_settings import AdvancedGameSettings
from .data.minimum_privilege_level import MinimumPrivilegeLevel
from .data.new_game_save import NewGameData
from .data.response import Response
from .data.server_options import ServerOptions
from .exceptions import APIError


class AsyncSatisfactoryAPI:
    """ An async client for the Satisfactory Dedicated Server API """

    def __init__(self, host: str, port: int = 7777, auth_token: str = None, skip_ssl_verification: bool = False):
        """
        Initialize the async API client

        Parameters
        ----------
        host : str
            The hostname or IP address of the server
        port : int, optional
            The port to connect to, by default 7777
        auth_token : str, optional
            The authentication token, by default None.
            You can use the `password_login` or `passwordless_login` methods to request a token from the server.
        skip_ssl_verification : bool, optional
            Disable SSL certificate verification entirely, by default False.
            When True, ``init_certificate`` has no effect and all requests skip verification.
        """
        self.host: str = host
        self.port: int = port
        self.auth_token: str | None = auth_token
        self.skip_ssl_verification: bool = skip_ssl_verification
        self.cert_path: str | None = None
        self._ssl_context: ssl.SSLContext | None = None

    def _get_ssl(self) -> ssl.SSLContext | bool:
        if self.skip_ssl_verification:
            return False
        return self._ssl_context or False

    async def init_certificate(self) -> None:
        """
        Fetch and cache the server's SSL certificate for verified HTTPS requests.

        Downloads the server's self-signed certificate and saves it to a local
        ``certs/`` directory. Once called, all subsequent requests will verify
        against this certificate instead of skipping SSL verification.

        Raises
        ------
        ssl.SSLError
            If the certificate cannot be retrieved from the server.
        RuntimeError
            If ``skip_ssl_verification`` is True.
        """
        if self.skip_ssl_verification:
            raise RuntimeError("Cannot initialise certificate while skip_ssl_verification is enabled.")

        certs_dir = os.path.join(os.path.dirname(__file__), 'certs')
        os.makedirs(certs_dir, exist_ok=True)

        cert_path = os.path.join(certs_dir, f"{self.host.replace('.', '_')}_{self.port}.pem")

        if not os.path.exists(cert_path):
            pem_cert = await asyncio.to_thread(ssl.get_server_certificate, (self.host, self.port))
            with open(cert_path, 'w') as f:
                f.write(pem_cert)
            print(f"Certificate saved to {cert_path}")

        self.cert_path = cert_path
        ctx = ssl.create_default_context()
        ctx.load_verify_locations(cert_path)
        self._ssl_context = ctx

    async def _post(self, function, data=None, files=None):
        """
        Post a request to the API

        :param function: The function to call
        :param data: The data to send
        :param files: The files to send
        :return: The response data
        :raises APIError: If the API returns an error
        """
        url = f"https://{self.host}:{self.port}/api/v1"
        headers = {'Content-Type': 'application/json'}

        if self.auth_token:
            headers['Authorization'] = f'Bearer {self.auth_token}'

        payload = {'function': function, 'data': data} if data else {'function': function}

        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload, headers=headers, ssl=self._get_ssl()) as response:
                if response.status not in (200, 204):
                    error_data = await response.json(content_type=None)
                    raise APIError(
                        error_code=error_data.get('errorCode'),
                        message=error_data.get('errorMessage')
                    )

                if response.status == 204:
                    return {}

                content_type = response.headers.get('Content-Type', '')
                if 'application/json' in content_type:
                    result = await response.json(content_type=None)
                    if result.get('errorCode'):
                        raise APIError(result.get('errorMessage'))
                    return result.get('data')
                elif content_type == 'application/octet-stream':
                    return await response.read()
                else:
                    return await response.text()

    async def health_check(self, client_custom_data: str = '') -> Response:
        """
        Perform a health check on the server.

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
        response = await self._post('HealthCheck', {'ClientCustomData': client_custom_data})
        return Response(success=True, data=response)

    async def verify_authentication_token(self) -> Response:
        """
        Verify the authentication token.

        Returns
        -------
        Response
            A Response containing the message 'Token is valid'.

        Raises
        ------
        APIError
            If the API returns an error or if the token is invalid.
        """
        await self._post('VerifyAuthenticationToken')
        return Response(success=True, data={'message': 'Token is valid'})

    async def passwordless_login(self, minimum_privilege_level: MinimumPrivilegeLevel) -> Response:
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
            If the API returns an error or if the login is unsuccessful.
        """
        response = await self._post('PasswordlessLogin', {'MinimumPrivilegeLevel': minimum_privilege_level.value})
        self.auth_token = response['authenticationToken']
        return Response(success=True, data={'message': 'Successfully logged in, the token is now stored'})

    async def password_login(self, minimum_privilege_level: MinimumPrivilegeLevel, password: str) -> Response:
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
            If the API returns an error or if the login is unsuccessful.
        """
        response = await self._post('PasswordLogin', {
            'MinimumPrivilegeLevel': minimum_privilege_level.value,
            'Password': password
        })
        self.auth_token = response['authenticationToken']
        return Response(success=True, data={'message': 'Successfully logged in, the token is now stored'})

    async def query_server_state(self) -> Response:
        """
        Query the server state.

        Returns
        -------
        Response
            A Response containing the server state data.

        Raises
        ------
        APIError
            If the API returns an error.
        """
        response = await self._post('QueryServerState')
        return Response(success=True, data=response)

    async def get_server_options(self) -> Response:
        """
        Get the server options.

        Returns
        -------
        Response
            A Response containing the server options data.

        Raises
        ------
        APIError
            If the API returns an error.
        """
        response = await self._post('GetServerOptions')
        return Response(success=True, data=response)

    async def get_advanced_game_settings(self) -> Response:
        """
        Fetch advanced game settings.

        Returns
        -------
        Response
            A Response containing the advanced game settings.
        """
        response = await self._post('GetAdvancedGameSettings')
        return Response(success=True, data=response)

    async def apply_advanced_game_settings(self, settings: AdvancedGameSettings) -> Response:
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
        await self._post('ApplyAdvancedGameSettings', {'AdvancedGameSettings': settings.to_dict()})
        return Response(success=True, data={
            'message': 'Successfully applied advanced game settings to the server.',
            'settings': settings.to_dict()
        })

    async def claim_server(self, server_name: str, admin_password: str) -> Response:
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
        response = await self._post('ClaimServer', {
            'ServerName': server_name,
            'AdminPassword': admin_password
        })
        return Response(success=True, data=response)

    async def rename_server(self, server_name: str) -> Response:
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
        response = await self._post('RenameServer', {'ServerName': server_name})
        return Response(success=True, data=response)

    async def set_client_password(self, password: str) -> Response:
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
        response = await self._post('SetClientPassword', {'Password': password})
        return Response(success=True, data=response)

    async def set_admin_password(self, password: str, auth_token: str) -> Response:
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
        response = await self._post('SetAdminPassword', {
            'Password': password,
            'AuthenticationToken': auth_token
        })
        return Response(success=True, data=response)

    async def set_auto_load_session_name(self, session_name: str) -> Response:
        """
        Set the auto-load session name.

        Parameters
        ----------
        session_name : str
            The session name to auto-load.

        Returns
        -------
        Response
            A Response indicating the success of the operation.
        """
        response = await self._post('SetAutoLoadSessionName', {'SessionName': session_name})
        return Response(success=True, data=response)

    async def run_command(self, command: str) -> Response:
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
        response = await self._post('RunCommand', {'Command': command})
        return Response(success=True, data=response)

    async def shutdown(self) -> Response:
        """
        Shut down the server.

        Returns
        -------
        Response
            A Response indicating the success of the operation.
        """
        await self._post('Shutdown')
        return Response(success=True, data={
            'message': "Server is shutting down... Note: If the server is configured as a service and the restart "
                       "policy is set to 'always', it will restart automatically."
        })

    async def apply_server_options(self, options: ServerOptions) -> Response:
        """
        Apply server options.

        Parameters
        ----------
        options : ServerOptions
            The server options to apply.

        Returns
        -------
        Response
            A Response indicating the success of the operation.
        """
        await self._post('ApplyServerOptions', {'UpdatedServerOptions': options.to_dict()})
        return Response(success=True, data={
            'message': 'Successfully applied server options to the server.',
            'options': options.to_dict()
        })

    async def create_new_game(self, game_data: NewGameData) -> Response:
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
        response = await self._post('CreateNewGame', {'NewGameData': game_data.__dict__})
        return Response(success=True, data=response)

    async def save_game(self, save_name: str) -> Response:
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
        response = await self._post('SaveGame', {'SaveName': save_name})
        return Response(success=True, data=response)

    async def delete_save_file(self, save_name: str) -> Response:
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
        response = await self._post('DeleteSaveFile', {'SaveName': save_name})
        return Response(success=True, data=response)

    async def delete_save_session(self, session_name: str) -> Response:
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
        response = await self._post('DeleteSaveSession', {'SessionName': session_name})
        return Response(success=True, data=response)

    async def enumerate_sessions(self) -> Response:
        """
        Enumerate available sessions. You need admin privileges to call this function.

        Returns
        -------
        Response
            A Response containing the available sessions.
        """
        response = await self._post('EnumerateSessions')
        return Response(success=True, data=response)

    async def load_game(self, save_name: str, enable_advanced_game_settings: bool = False) -> Response:
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
        response = await self._post('LoadGame', {
            'SaveName': save_name,
            'EnableAdvancedGameSettings': enable_advanced_game_settings
        })
        return Response(success=True, data=response)

    async def upload_save_game(self, save_name: str, load_save_game: bool = False,
                               enable_advanced_game_settings: bool = False) -> Response:
        raise NotImplementedError('This method is not implemented yet')

    async def download_save_game(self, save_name: str) -> Response:
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
        response = await self._post('DownloadSaveGame', {'SaveName': save_name})
        return Response(success=True, data=response)
