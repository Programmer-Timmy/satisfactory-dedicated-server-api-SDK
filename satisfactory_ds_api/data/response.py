import dataclasses


@dataclasses.dataclass
class Response:
    success: bool
    data: dict
