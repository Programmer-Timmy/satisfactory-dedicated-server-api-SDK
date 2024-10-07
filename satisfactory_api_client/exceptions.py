class APIError(Exception):
    """
    Exception raised for API errors.

    Attributes
    ----------
    error_code : str
        The error code
    message : str
        The error message
    """

    error_code: str
    message: str

    def __init__(self, error_code: str, message: str):
        self.error_code = error_code
        self.message = message
        super().__init__(message)

    def __str__(self):
        """Return a string representation of the error."""
        return f'{self.error_code}: {self.message}'

    def __dict__(self):
        """Return a dictionary representation of the error."""
        return {
            'error_code': self.error_code,
            'message': self.message
        }




class InvalidParameterError(APIError):
    """Exception raised for invalid parameters."""
    pass
