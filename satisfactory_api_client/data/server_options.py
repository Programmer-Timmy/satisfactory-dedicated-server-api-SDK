from dataclasses import dataclass


@dataclass
class ServerOptions:
    """
    Represents the server settings of a Satisfactory server.

    Attributes

    """
    DSAutoPause: bool
    DSAutoSaveOnDisconnect: bool
    AutosaveInterval: float
    ServerRestartTimeSlot: float
    SendGameplayData: bool
    NetworkQuality: int

    def to_json(self) -> dict:
        """
        Converts the server settings to a JSON string.

        Returns
        -------
        str
            The server settings as a JSON string.
        """
        # Convert to a dictionary
        settings_dict = self.__dict__
        # Create a new dictionary with dot notation
        return {
            "serverOptions": {
                f"FG.{str(key)}": value for key, value in settings_dict.items()
            }
        }

