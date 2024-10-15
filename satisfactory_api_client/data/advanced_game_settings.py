from dataclasses import dataclass, asdict
@dataclass
class AdvancedGameSettings:
    """
    Represents the advanced game settings of a Satisfactory server.

    You only need to set the attributes you want to change.

    Attributes
    ----------
    NoPower: bool | None
        If enabled, power requirements are disabled.

    DisableArachnidCreatures: bool | None
        If enabled, arachnid creatures are disabled.

    NoUnlockCost: bool | None
        If enabled, unlock costs are disabled.

    SetGamePhase: int | None
        The game phase to set.

    GiveAllTiers: bool | None
        If enabled, all tiers are given.

    UnlockAllResearchSchematics: bool | None
        If enabled, all research schematics are unlocked.

    UnlockInstantAltRecipes: bool | None
        If enabled, instant alternate recipes are unlocked.

    UnlockAllResourceSinkSchematics: bool | None
        If enabled, all resource sink schematics are unlocked.

    GiveItems: str | None
        The items to give.

    NoBuildCost: bool | None
        If enabled, build costs are disabled.

    GodMode: bool | None
        If enabled, god mode is enabled.

    FlightMode: bool | None
        If enabled, flight mode is enabled.

    """
    NoPower: bool | None = None
    DisableArachnidCreatures: bool | None = None
    NoUnlockCost: bool | None = None
    SetGamePhase: int | None = None
    GiveAllTiers: bool | None = None
    UnlockAllResearchSchematics: bool | None = None
    UnlockInstantAltRecipes: bool | None = None
    UnlockAllResourceSinkSchematics: bool | None = None
    GiveItems: str | None = None
    NoBuildCost: bool | None = None
    GodMode: bool | None = None
    FlightMode: bool | None = None

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
