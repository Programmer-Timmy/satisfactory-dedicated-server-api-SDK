import urllib3
from .api_client import SatisfactoryAPI
from .async_api_client import AsyncSatisfactoryAPI
from .exceptions import APIError, InvalidParameterError


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

