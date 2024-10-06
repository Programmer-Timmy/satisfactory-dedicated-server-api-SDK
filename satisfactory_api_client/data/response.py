import dataclasses


@dataclasses.dataclass
class Response:
    """
    Represents the response from the Satisfactory API.

    Attributes
    ----------
    success : bool
        Whether the request was successful.
    data : dict | str
        The data returned from the API.
    """
    success: bool
    data: dict | bytes
