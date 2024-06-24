# Object classes from AP that represent different types of options that you can create
from Options import FreeText, NumericOption, Toggle, DefaultOnToggle, Choice, TextChoice, Range, NamedRange, OptionSet
from enum import Enum, IntEnum

# These helper methods allow you to determine if an option has been set, or what its value is, for any player in the multiworld
from ..Helpers import is_option_enabled, get_option_value



####################################################################
# NOTE: At the time that options are created, Manual has no concept of the multiworld or its own world.
#       Options are defined before the world is even created.
#
# Example of creating your own option:
#
#   class MakeThePlayerOP(Toggle):
#       """Should the player be overpowered? Probably not, but you can choose for this to do... something!"""
#       display_name = "Make me OP"
#
#   options["make_op"] = MakeThePlayerOP
#
#
# Then, to see if the option is set, you can call is_option_enabled or get_option_value.
#####################################################################


# To add an option, use the before_options_defined hook below and something like this:
#   options["total_characters_to_win_with"] = TotalCharactersToWinWith
#
class TotalCharactersToWinWith(Range):
    """Instead of having to beat the game with all characters, you can limit locations to a subset of character victory locations."""
    display_name = "Number of characters to beat the game with before victory"
    range_start = 10
    range_end = 50
    default = 50

class TwoPointCampusDLC(Enum):
    BASE_GAME = "Base Game"
    SPACE_ACADEMY = "Space Academy"
    SCHOOL_SPIRITS = "School Spirits"
    MEDICAL_SCHOOL = "Medical School"

class DLC(OptionSet):
    """What part of the game do you want to include?
    Base Game (default): only include the base game and exclude all dlc
    Space Academy: include the base game and the Space Academy DLC
    School Spirits: include the base game and the School Spirits DLC
    Medical School: include the base game and the Medical School DLC
    """
    display_name = "Enabled DLC"
    default = {"Base Game"}
    valid_keys = {
        "Base Game", "Space Academy", "School Spirits", "Medical School"
    }



# This is called before any manual options are defined, in case you want to define your own with a clean slate or let Manual define over them
def before_options_defined(options: dict) -> dict:
    return options

# This is called after any manual options are defined, in case you want to see what options are defined or want to modify the defined options
def after_options_defined(options: dict) -> dict:
    options["enable_dlc"] = DLC
    return options