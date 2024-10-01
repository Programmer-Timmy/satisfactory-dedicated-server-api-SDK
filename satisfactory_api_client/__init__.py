import urllib3
from .api_client import SatisfactoryAPI
from .exceptions import APIError, InvalidParameterError


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

