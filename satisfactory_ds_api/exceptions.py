class APIError(Exception):
    """Exception raised for API errors."""
    pass

class InvalidParameterError(APIError):
    """Exception raised for invalid parameters."""
    pass
