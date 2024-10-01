# Satisfactory Dedicated Server API Client

This Python package provides a client for interacting with the Satisfactory Dedicated Server API. The client allows for managing various aspects of the server, including querying server state, logging in, adjusting game settings, handling save files, and issuing administrative commands.

## Features

- Perform health checks on the server
- Log in with or without a password to obtain an authentication token
- Query and modify server state and options
- Manage advanced game settings
- Create, load, save, and delete game sessions
- Set client and admin passwords
- Run server commands and shut down the server

## Installation

To install this package, use:

```bash
pip install satisfactory-api-client
```

## Requirements

- Python 3.8+
- `requests` library

## Usage

### Initializing the Client

The `SatisfactoryAPI` class is the main entry point for interacting with the server API.

```python
from satisfactory_api_client import SatisfactoryAPI

# Initialize the API client
api = SatisfactoryAPI(host='your-server-ip', port=7777, auth_token='your-auth-token')
```

### Login

You can log in to the server using passwordless or password-based methods.

```python
from satisfactory_api_client.data import MinimumPrivilegeLevel

# Passwordless login
response = api.passwordless_login(MinimumPrivilegeLevel.ADMIN)

# Password login
response = api.password_login(MinimumPrivilegeLevel.ADMIN, password='your-admin-password')
```

### Health Check

To verify that the server is running and responsive, you can perform a health check:

```python
response = api.health_check()
print(response.data)
```

### Server Options

You can query the server's current options and apply new ones:

```python
# Get server options
response = api.get_server_options()
print(response.data)

# Apply new server options
new_options = {"server_name": "New Server Name"}
response = api.apply_server_options(new_options)
```

### Advanced Game Settings

Fetch and apply advanced game settings:

```python
from satisfactory_api_client.data import AdvancedGameSettings

# Get advanced game settings
response = api.get_advanced_game_settings()
print(response.data)

# Apply advanced game settings
new_settings = AdvancedGameSettings(your_custom_settings)
response = api.apply_advanced_game_settings(new_settings)
```

### Managing Game Sessions

You can create, load, save, and delete game sessions.

```python
from satisfactory_api_client.data import NewGameData

# Create a new game
new_game_data = NewGameData(save_name="MyNewGame", ...)
response = api.create_new_game(new_game_data)

# Load a saved game
response = api.load_game("MySaveGame")

# Save the current game
response = api.save_game("MySaveGame")

# Delete a save file
response = api.delete_save_file("MySaveGame")
```

### Running Commands and Managing the Server

You can run commands on the server or shut it down:

```python
# Run a server command
response = api.run_command("SomeCommand")

# Shutdown the server
response = api.shutdown()
```

## Methods

### Authentication

- `passwordless_login(minimum_privilege_level: MinimumPrivilegeLevel)`: Log in without a password.
- `password_login(minimum_privilege_level: MinimumPrivilegeLevel, password: str)`: Log in using a password.

### Server Management

- `health_check(client_custom_data: str = '')`: Perform a health check on the server.
- `shutdown()`: Shut down the server.

### Game Management

- `create_new_game(game_data: NewGameData)`: Create a new game session.
- `load_game(save_name: str, enable_advanced_game_settings: bool = False)`: Load a saved game.
- `save_game(save_name: str)`: Save the current game session.
- `delete_save_file(save_name: str)`: Delete a saved game.
- `enumerate_sessions()`: List all available game sessions.

### Server Settings

- `get_server_options()`: Get current server settings.
- `apply_server_options(options: dict)`: Apply new server settings.
- `get_advanced_game_settings()`: Get advanced game settings.
- `apply_advanced_game_settings(settings: AdvancedGameSettings)`: Apply new advanced game settings.

### Commands

- `run_command(command: str)`: Run a server command.

## Error Handling

Errors returned by the API will raise an `APIError` exception, which contains the error message from the server.

```python
try:
    response = api.some_method()
except APIError as e:
    print(f"Error: {e}")
```

## Contributing

Contributions are welcome! If you find a bug or have a feature request, please create an issue on the GitHub repository.

## License

This project is licensed under the MIT License. See the LICENSE file for details.