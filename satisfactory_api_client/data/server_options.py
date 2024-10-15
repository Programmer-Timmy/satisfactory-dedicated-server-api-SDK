from dataclasses import dataclass


@dataclass
class ServerOptions:
    """
    Represents the server settings of a Satisfactory server.

    You only need to set the attributes you want to change.

    Attributes
    ----------
    DSAutoPause: bool | None
        If enabled, the server will automatically pause when no players are connected.

    DSAutoSaveOnDisconnect: bool | None
        If enabled, the server will automatically save when a player disconnects.

    AutosaveInterval: float | None
        The interval at which the server will automatically save the game.

    ServerRestartTimeSlot: float | None
        The time slot at which the server will restart.

    SendGameplayData: bool | None
        If enabled, the server will send gameplay data.

    NetworkQuality: int | None
        The network quality of the server.
    """
    DSAutoPause: bool | None = None
    DSAutoSaveOnDisconnect: bool | None = None
    AutosaveInterval: float | None = None
    ServerRestartTimeSlot: float | None = None
    SendGameplayData: bool | None = None
    NetworkQuality: int | None = None

    def to_dict(self) -> dict:
        """
        Converts the server settings to a dictionary in the required format.

        Returns
        -------
        dict
            The server settings as a dictionary.
        """
        settings_dict = self.__dict__
        return {
            f"FG.{str(key)}": str(value) for key, value in settings_dict.items() if value is not None
        }

