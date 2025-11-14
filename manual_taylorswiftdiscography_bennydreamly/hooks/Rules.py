from typing import Optional
from worlds.AutoWorld import World
from ..Helpers import clamp, get_items_with_value, is_option_enabled
from BaseClasses import MultiWorld, CollectionState

import re

# Sometimes you have a requirement that is just too messy or repetitive to write out with boolean logic.
# Define a function here, and you can use it in a requires string with {function_name()}.
def overfishedAnywhere(world: World, state: CollectionState, player: int):
    """Has the player collected all fish from any fishing log?"""
    for cat, items in world.item_name_groups:
        if cat.endswith("Fishing Log") and state.has_all(items, player):
            return True
    return False

# You can also pass an argument to your function, like {function_name(15)}
# Note that all arguments are strings, so you'll need to convert them to ints if you want to do math.
def anyClassLevel(state: CollectionState, player: int, level: str):
    """Has the player reached the given level in any class?"""
    for item in ["Figher Level", "Black Belt Level", "Thief Level", "Red Mage Level", "White Mage Level", "Black Mage Level"]:
        if state.count(item, player) >= int(level):
            return True
    return False

# You can also return a string from your function, and it will be evaluated as a requires string.
def requiresMelee():
    """Returns a requires string that checks if the player has unlocked the tank."""
    return "|Figher Level:15| or |Black Belt Level:15| or |Thief Level:15|"

def hasAllAlbums(world: World, state: CollectionState, player: int):
    """Are all the enabled albums unlocked?"""
    multiworld = world.multiworld

    required_albums = []

    re_recordings = is_option_enabled(multiworld, player, "include_re_recordings")
    debut = is_option_enabled(multiworld, player, "include_debut")
    fearless = is_option_enabled(multiworld, player, "include_fearless")
    fearless_tv = is_option_enabled(multiworld, player, "include_fearless_tv")
    speak_now = is_option_enabled(multiworld, player, "include_speak_now")
    speak_now_tv = is_option_enabled(multiworld, player, "include_speak_now_tv")
    red = is_option_enabled(multiworld, player, "include_red")
    red_tv = is_option_enabled(multiworld, player, "include_red_tv")
    include_1989 = is_option_enabled(multiworld, player, "include_1989")
    include_1989_tv = is_option_enabled(multiworld, player, "include_1989_tv")
    reputation = is_option_enabled(multiworld, player, "include_reputation")
    lover = is_option_enabled(multiworld, player, "include_lover")
    folklore = is_option_enabled(multiworld, player, "include_folklore")
    evermore = is_option_enabled(multiworld, player, "include_evermore")
    midnights = is_option_enabled(multiworld, player, "include_midnights")
    ttpd = is_option_enabled(multiworld, player, "include_ttpd")

    if debut:
        required_albums.append("Taylor Swift")

    if fearless:
        required_albums.append("Fearless")

    if speak_now:
        required_albums.append("Speak Now")

    if red:
        required_albums.append("Red")

    if include_1989:
        required_albums.append("1989")

    if reputation:
        required_albums.append("Reputation")

    if lover:
        required_albums.append("Lover")

    if folklore:
        required_albums.append("Folklore")

    if evermore:
        required_albums.append("Evermore")

    if midnights:
        required_albums.append("Midnights")

    if ttpd:
        required_albums.append("The Tortured Poets Department")

    if re_recordings:
        if fearless_tv:
            required_albums.append("Fearless (Taylor's Version)")

        if speak_now_tv:
            required_albums.append("Speak Now (Taylor's Version)")

        if red_tv:
            required_albums.append("Red (Taylor's Version)")

        if include_1989_tv:
            required_albums.append("1989 (Taylor's Version)")

    return all(state.has(album) for album in required_albums)