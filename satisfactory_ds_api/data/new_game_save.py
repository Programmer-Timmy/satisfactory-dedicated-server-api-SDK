from dataclasses import dataclass
from typing import Optional
from .advanced_game_settings import AdvancedGameSettings


@dataclass
class NewGameData:
    """
    New game data for a Satisfactory Dedicated Server

    Attributes
    ----------
    SessionName : str
        The name of the session
    MapName : Optional[str]
        The name of the map
    StartingLocation : Optional[str]
        The starting location of the session
    SkipOnboarding : Optional[bool]
        Whether to skip the onboarding process
    AdvancedGameSettings : Optional[AdvancedGameSettings]
        Advanced game settings for the server
    CustomOptionsOnlyForModding : Optional[dict]
        Custom options only for mod
    """
    SessionName: str
    MapName: Optional[str] = None
    StartingLocation: Optional[str] = None
    SkipOnboarding: Optional[bool] = None
    AdvancedGameSettings: Optional[AdvancedGameSettings] = None
    CustomOptionsOnlyForModding: Optional[dict] = None