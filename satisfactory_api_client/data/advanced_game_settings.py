from dataclasses import dataclass, asdict
@dataclass
class AdvancedGameSettings:
    """
    Represents the advanced game settings of a Satisfactory server.

    Attributes
    ----------
    NoPower: bool
        If enabled, power requirements are disabled.
    DisableArachnidCreatures: bool
        If enabled, arachnid creatures are disabled.
    NoUnlockCost: bool
        If enabled, unlock costs are disabled.
    SetGamePhase: int
        The game phase to set.
    GiveAllTiers: bool
        If enabled, all tiers are given.
    UnlockAllResearchSchematics: bool
        If enabled, all research schematics are unlocked.
    UnlockInstantAltRecipes: bool
        If enabled, instant alternate recipes are unlocked.
    UnlockAllResourceSinkSchematics: bool
        If enabled, all resource sink schematics are unlocked.
    GiveItems: str
        The items to give.
    NoBuildCost: bool
        If enabled, build costs are disabled.
    GodMode: bool
        If enabled, god mode is enabled.
    FlightMode: bool
        If enabled, flight mode is enabled.
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
        dict
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
