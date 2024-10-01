from enum import Enum

class MinimumPrivilegeLevel(Enum):
    NOT_AUTHENTICATED = 'NotAuthenticated'
    CLIENT = 'Client'
    ADMINISTRATOR = 'Administrator'
    INITIAL_ADMIN = 'InitialAdmin'
    API_TOKEN = 'APIToken'
