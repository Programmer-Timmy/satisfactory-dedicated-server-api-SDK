import json
from dataclasses import dataclass, asdict

@dataclass
class AdvancedGameRules:
    NoPower: bool
    DisableArachnidCreatures: bool
    NoUnlockCost: bool
    SetGamePhase: str
    GiveAllTiers: bool
    UnlockAllResearchSchematics: bool
    UnlockInstantAltRecipes: bool
    UnlockAllResourceSinkSchematics: bool
    GiveItems: str
    NoBuildCost: bool
    GodMode: bool
    FlightMode: bool

@dataclass
class AdvancedGameSettings:
    """
    Represents the advanced game settings of a Satisfactory server.

    Attributes
    ----------
    creativeModeEnabled : bool
        Whether or not creative mode is enabled.
    advancedGameSettings : AdvancedGameRules
        The advanced game settings.
    """
    creativeModeEnabled: bool
    advancedGameSettings: AdvancedGameRules

    def to_json(self) -> dict:
        """
        Converts the advanced game settings to a JSON string.

        Returns
        -------
        str
            The advanced game settings as a JSON string.
        """
        # Convert to a dictionary
        settings_dict = asdict(self)
        # Create a new dictionary with dot notation
        return {
            "creativeModeEnabled": settings_dict["creativeModeEnabled"],
            "advancedGameSettings": {
                f"FG.GameRules.{key}": value for key, value in settings_dict["advancedGameSettings"].items()
            }
        }
