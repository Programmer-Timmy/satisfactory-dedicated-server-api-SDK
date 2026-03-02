# Satisfactory Dedicated Server API Client

This Python package provides a client for interacting with the Satisfactory Dedicated Server API. The client allows for managing various aspects of the server, including querying server state, logging in, adjusting game settings, handling save files, and issuing administrative commands.

Both a **synchronous** (`SatisfactoryAPI`) and an **asynchronous** (`AsyncSatisfactoryAPI`) client are provided.

## Features

- Perform health checks on the server
- Log in with or without a password to obtain an authentication token
- Query and modify server state and options
- Manage advanced game settings
- Create, load, save, and delete game sessions
- Set client and admin passwords
- Run server commands and shut down the server
- SSL certificate pinning for self-signed server certificates
- Full async support via `AsyncSatisfactoryAPI`

## Installation

To install this package, use:

```bash
pip install satisfactory-api-client
```

## Requirements

- Python 3.10+
- `requests` library
- `aiohttp` library (for async client)

## Usage

### Initializing the Client

```python
from satisfactory_api_client import SatisfactoryAPI

# Basic initialization
api = SatisfactoryAPI(host='your-server-ip')

# Custom port
api = SatisfactoryAPI(host='your-server-ip', port=15000)

# With an existing auth token
api = SatisfactoryAPI(host='your-server-ip', auth_token='your-token')

# Skip SSL verification (not recommended for production)
api = SatisfactoryAPI(host='your-server-ip', skip_ssl_verification=True)
```

### SSL Certificate Pinning

Satisfactory dedicated servers use self-signed certificates. You can pin the server's certificate so that requests are verified against it instead of skipping SSL entirely:

```python
api = SatisfactoryAPI(host='your-server-ip')

# Fetches and saves the certificate to certs/<host>_<port>.pem
# All subsequent requests will be verified against it
api.init_certificate()
```

The certificate is saved locally and reused on future runs. If `skip_ssl_verification=True` is set, calling `init_certificate()` raises a `RuntimeError`.

### Login

```python
from satisfactory_api_client.data import MinimumPrivilegeLevel

# Passwordless login
response = api.passwordless_login(MinimumPrivilegeLevel.ADMINISTRATOR)

# Password login
response = api.password_login(MinimumPrivilegeLevel.ADMINISTRATOR, password='your-admin-password')

# Verify the stored token
response = api.verify_authentication_token()
print(response.data)
```

#### Minimum Privilege Levels

The `MinimumPrivilegeLevel` enum specifies the type of token to obtain:

| Level | Description |
|---|---|
| `NOT_AUTHENTICATED` | No authentication required |
| `CLIENT` | Standard client access |
| `ADMINISTRATOR` | Full administrative access |
| `INITIAL_ADMIN` | Initial setup admin access |
| `API_TOKEN` | API token access |

### Health Check

```python
response = api.health_check()
print(response.data)
```

### Querying Server State

```python
response = api.query_server_state()
print(response.data)
```

### Server Options

```python
# Get server options
response = api.get_server_options()
print(response.data)

# Apply new server options
from satisfactory_api_client.data import ServerOptions
response = api.apply_server_options(ServerOptions(...))
```

### Advanced Game Settings

```python
from satisfactory_api_client.data import AdvancedGameSettings

# Get advanced game settings
response = api.get_advanced_game_settings()
print(response.data)

# Apply advanced game settings
response = api.apply_advanced_game_settings(AdvancedGameSettings(...))
```

### Managing Game Sessions

```python
from satisfactory_api_client.data import NewGameData

# Create a new game
response = api.create_new_game(NewGameData(save_name="MyNewGame", ...))

# Load a saved game
response = api.load_game("MySaveGame")

# Save the current game
response = api.save_game("MySaveGame")

# Delete a save file
response = api.delete_save_file("MySaveGame")

# List all sessions (requires admin)
response = api.enumerate_sessions()
```

### Running Commands and Shutdown

```python
response = api.run_command("SomeCommand")
response = api.shutdown()
```

---

## Async Client

`AsyncSatisfactoryAPI` mirrors the full API of `SatisfactoryAPI` but uses `async`/`await` via `aiohttp`. All methods, including `init_certificate`, are async.

### Initializing the Async Client

```python
from satisfactory_api_client import AsyncSatisfactoryAPI

api = AsyncSatisfactoryAPI(host='your-server-ip')

# Skip SSL verification
api = AsyncSatisfactoryAPI(host='your-server-ip', skip_ssl_verification=True)
```

### SSL Certificate Pinning (async)

```python
api = AsyncSatisfactoryAPI(host='your-server-ip')
await api.init_certificate()
```

### Example

```python
import asyncio
from satisfactory_api_client import AsyncSatisfactoryAPI
from satisfactory_api_client.data import MinimumPrivilegeLevel

async def main():
    api = AsyncSatisfactoryAPI(host='your-server-ip')
    await api.init_certificate()

    await api.password_login(MinimumPrivilegeLevel.ADMINISTRATOR, password='your-password')

    state = await api.query_server_state()
    print(state.data)

asyncio.run(main())
```

All methods on `AsyncSatisfactoryAPI` are `async def` and must be awaited.

---

## Methods Reference

### Authentication

| Method | Description |
|---|---|
| `passwordless_login(minimum_privilege_level)` | Log in without a password |
| `password_login(minimum_privilege_level, password)` | Log in with a password |
| `verify_authentication_token()` | Verify the stored token is valid |

### SSL

| Method | Description |
|---|---|
| `init_certificate()` | Fetch and pin the server's SSL certificate |

### Server Management

| Method | Description |
|---|---|
| `health_check(client_custom_data='')` | Check server health (no token required) |
| `query_server_state()` | Get the current server and session state |
| `claim_server(server_name, admin_password)` | Claim an unclaimed server |
| `rename_server(server_name)` | Rename the server |
| `run_command(command)` | Execute a console command |
| `shutdown()` | Shut down the server |

### Server Settings

| Method | Description |
|---|---|
| `get_server_options()` | Get current server options |
| `apply_server_options(options)` | Apply new server options |
| `get_advanced_game_settings()` | Get advanced game settings |
| `apply_advanced_game_settings(settings)` | Apply advanced game settings |
| `set_client_password(password)` | Set the client password |
| `set_admin_password(password, auth_token)` | Set the admin password |
| `set_auto_load_session_name(session_name)` | Set the session to auto-load on start |

### Game Management

| Method | Description |
|---|---|
| `create_new_game(game_data)` | Start a new game session |
| `load_game(save_name, enable_advanced_game_settings)` | Load a saved game |
| `save_game(save_name)` | Save the current game |
| `delete_save_file(save_name)` | Delete a save file |
| `delete_save_session(session_name)` | Delete all saves for a session |
| `enumerate_sessions()` | List all saved sessions (admin required) |
| `download_save_game(save_name)` | Download a save file as bytes |

---

## Error Handling

All API errors raise `APIError`:

```python
from satisfactory_api_client import APIError

try:
    response = api.some_method()
except APIError as e:
    print(f"Error: {e}")
```

---

## Contributing

Contributions are welcome! If you find a bug or have a feature request, please create an issue on the GitHub repository.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgements

This package is not affiliated with or endorsed by Coffee Stain Studios. Satisfactory is a trademark of Coffee Stain Studios AB.

## References

- [Satisfactory Dedicated Server API Documentation](https://satisfactory.wiki.gg/wiki/Dedicated_servers/HTTPS_API)
