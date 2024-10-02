import json
from dataclasses import dataclass, asdict

@dataclass
class AdvancedGameRules:
    NoPower: str
    DisableArachnidCreatures: str
    NoUnlockCost: str
    SetGamePhase: str
    GiveAllTiers: str
    UnlockAllResearchSchematics: str
    UnlockInstantAltRecipes: str
    UnlockAllResourceSinkSchematics: str
    GiveItems: str
    NoBuildCost: str
    GodMode: str
    FlightMode: str

@dataclass
class AdvancedGameSettings:
    creativeModeEnabled: bool
    advancedGameSettings: AdvancedGameRules

    def to_json(self) -> str:
        # Convert to a dictionary
        settings_dict = asdict(self)
        # Create a new dictionary with dot notation
        formatted_dict = {
            "creativeModeEnabled": settings_dict["creativeModeEnabled"],
            "advancedGameSettings": {
                f"FG.GameRules.{key}": value for key, value in settings_dict["advancedGameSettings"].items()
            }
        }
        # Convert the formatted dictionary to a JSON string
        return json.dumps(formatted_dict, indent=4)