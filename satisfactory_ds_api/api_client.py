from http.client import responses

import requests
from .data.minimum_privilege_level import MinimumPrivilegeLevel
from .data.response import Response
from .exceptions import APIError


class SatisfactoryAPI:
    def __init__(self, host, port=7777, auth_token=None):
        self.host = host
        self.port = port
        self.auth_token = auth_token

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

        response = requests.post(url, json=payload, headers=headers, files=files, verify=False)
        if response.status_code != 200 and response.status_code != 204:
            raise APIError(f"API error: {response.text}")

        if response.status_code == 204:
            return {}

        if response.json().get('errorCode'):
            raise APIError(response.json().get('errorMessage'))
        return response.json()

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
        self.auth_token = response['data']['authenticationToken']
        return Response(success=True, data=self.auth_token)

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
        self.auth_token = response['data']['authenticationToken']
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
