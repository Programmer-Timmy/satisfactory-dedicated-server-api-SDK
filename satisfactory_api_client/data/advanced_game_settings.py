from dataclasses import dataclass, asdict
@dataclass
class AdvancedGameSettings:
    """
    Represents the advanced game settings of a Satisfactory server.

    Attributes
    ----------
    NoPower: bool
        If enabled, power re

    """
    NoPower: bool
    DisableArachnidCreatures: bool
    NoUnlockCost: bool
    SetGamePhase: int
    GiveAllTiers: bool
    UnlockAllResearchSchematics: bool
    UnlockInstantAltRecipes: bool
    UnlockAllResourceSinkSchematics: bool
    GiveItems: str
    NoBuildCost: bool
    GodMode: bool
    FlightMode: bool

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
            "advancedGameSettings": {
                f"FG.GameRules.{str(key)}": value for key, value in settings_dict.items()
            }
        }
