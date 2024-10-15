from satisfactory_api_client import SatisfactoryAPI
from satisfactory_api_client.data import MinimumPrivilegeLevel
from satisfactory_api_client.data.server_options import ServerOptions

api = SatisfactoryAPI("192.168.2.11")

api.password_login(MinimumPrivilegeLevel.ADMINISTRATOR, "uvL5k91hRvhWskFWLWSR")
print(api.get_server_options())

serveroptions = ServerOptions(
    DSAutoPause=True
)

print(api.apply_server_options(serveroptions))
print(api.get_server_options())
