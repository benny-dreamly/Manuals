from typing import Optional
from worlds.AutoWorld import World
from ..Helpers import clamp, get_items_with_value
from BaseClasses import MultiWorld, CollectionState

import re

# Sometimes you have a requirement that is just too messy or repetitive to write out with boolean logic.
# Define a function here, and you can use it in a requires string with {function_name()}.
def overfishedAnywhere(world: World, multiworld: MultiWorld, state: CollectionState, player: int):
    """Has the player collected all fish from any fishing log?"""
    for cat, items in world.item_name_groups:
        if cat.endswith("Fishing Log") and state.has_all(items, player):
            return True
    return False

# You can also pass an argument to your function, like {function_name(15)}
# Note that all arguments are strings, so you'll need to convert them to ints if you want to do math.
def anyClassLevel(world: World, multiworld: MultiWorld, state: CollectionState, player: int, level: str):
    """Has the player reached the given level in any class?"""
    for item in ["Figher Level", "Black Belt Level", "Thief Level", "Red Mage Level", "White Mage Level", "Black Mage Level"]:
        if state.count(item, player) >= int(level):
            return True
    return False

# You can also return a string from your function, and it will be evaluated as a requires string.
# def requiresMelee(world: World, multiworld: MultiWorld, state: CollectionState, player: int):
#     """Returns a requires string that checks if the player has unlocked the tank."""
#     return "|Figher Level:15| or |Black Belt Level:15| or |Thief Level:15|" e

def requiresSolve(world: World, multiworld: MultiWorld, state: CollectionState, player: int):
    """Returns a requires string that checks if the player needs the Solve command to continue."""
    return "{YamlEnabled(more_unlocks)} AND |Progressive Command:8|"

def requiresCell(world: World, multiworld: MultiWorld, state: CollectionState, player: int):
    """Returns a requires string that checks if the player has all rooms in the Cell to continue."""
    return "{YamlEnabled(Roomsanity)} AND |Progressive Room:2|"

def requiresNoOptions(world: World, multiworld: MultiWorld, state: CollectionState, player: int):
    """Returns a requires string that checks if the player has no options enabled that affect logic."""
    return "({YamlDisabled(more_unlocks)} AND {YamlDisabled(Roomsanity)})"

def requiresDecipher(world: World, multiworld: MultiWorld, state: CollectionState, player: int):
    """Returns a requires string that checks if the player needs the Decipher command to continue."""
    return "{YamlEnabled(more_unlocks)} AND |Progressive Command:10|"

def requiresHallwayLeadingToVaults(world: World, multiworld: MultiWorld, state: CollectionState, player: int):
    """Returns a requires string that checks if the player has all rooms in the hallway leading to the Vaults in order to continue."""
    return "{YamlEnabled(Roomsanity)} AND |Progressive Room:6|"

def requiresVaults(world: World, multiworld: MultiWorld, state: CollectionState, player: int):
    """Returns a requires string that checks if the player has all rooms in the Vaults in order to continue."""
    return "{YamlEnabled(Roomsanity)} AND |Progressive Room:10|"

def requiresMoreUnlocksOnly(world: World, multiworld: MultiWorld, state: CollectionState, player: int):
    """Returns a requires string that checks if the player only has the More Unlocks option enabled."""
    return "{YamlDisabled(Roomsanity)} AND {YamlEnabled(more_unlocks}"

def requiresUnlock(world: World, multiworld: MultiWorld, state: CollectionState, player: int):
    """Returns a requires string that checks if the player needs the Unlock command to continue."""
    return "{YamlEnabled(more_unlocks)} AND |Progressive Command:9|"

def canUnlockSafe(world: World, multiworld: MultiWorld, state: CollectionState, player: int):
    """Returns a requires string that checks if the player can unlock the safe to continue."""
    return "(({requiresNoOptions()} AND |Puzzle (1/4)|) OR ({requiresVaults()} AND {YamlDisabled(more_unlocks)} AND |Puzzle (1/4)|) OR ({YamlDisabled(Roomsanity)} AND {requiresUnlock()} AND |Puzzle (1/4)|) OR ({requiresVaults()} and {requiresUnlock()} AND |Puzzle (1/4)|))"

def canReassembleHint(world: World, multiworld: MultiWorld, state: CollectionState, player: int):
    """Returns a requires string that checks if the player can reassemble the hint to continue."""
    return "|Hint Fragment A| AND |Hint Fragment B| AND |Hint Fragment C| AND |Hint Fragment D| AND |Hint Fragment E| AND |Hint Fragment F| AND |Hint Fragment G| AND |Hint Fragment H| AND |Hint Fragment I| AND |Hint Fragment J| AND |Hint Fragment K| AND |Hint Fragment L| AND |Hint Fragment M| AND |Glue Stick|"

def requiresCloset(world: World, multiworld: MultiWorld, state: CollectionState, player: int):
    """Returns a requires string that checks if the player has all rooms in the Storage Closet to continue."""
    return "{YamlEnabled(Roomsanity)} AND |Progressive Room:21|"

def canDecipherHint(world: World, multiworld: MultiWorld, state: CollectionState, player: int):
    """Returns a requires string that checks if the player can decipher the third hint"""
    return "(({requiresNoOptions()} AND {canReassembleHint()}) OR ({requiresCloset()} AND {YamlDisabled(more_unlocks)} AND {canReassembleHint()}) OR ({YamlDisabled(Roomsanity)} AND {requiresGlue()} AND {canReassembleHint()}) OR ({requiresCloset()} AND {requiresGlue()} AND {canReassembleHint()}))"

def requiresGlue(world: World, multiworld: MultiWorld, state: CollectionState, player: int):
    """Returns a requires string that checks if the player needs the Glue command to continue."""
    return "{YamlEnabled(more_unlocks)} AND |Progressive Command:11|"

def requiresFill(world: World, multiworld: MultiWorld, state: CollectionState, player: int):
    """Returns a requires string that checks if the player needs the Fill command to continue."""
    return "{YamlEnabled(more_unlocks)} AND |Progressive Command:13|"

def requiresHallwayLeadingToStorageCloset(world: World, multiworld: MultiWorld, state: CollectionState, player: int):
    """Returns a requires string that checks if the player has all rooms in the hallway from Vaults to Storage Closet to continue."""
    return "{YamlEnabled(Roomsanity)} AND |Progressive Room:19|"

def canOpenTrapdoor(world: World, multiworld: MultiWorld, state: CollectionState, player: int):
    """Returns a requires string that checks if the player can open the Trapdoor to continue."""
    return "|Glue Stick| and |Broom| and |Magnifying Glass|"

def canOpenTrapdoorEvent(world: World, multiworld: MultiWorld, state: CollectionState, player: int):
    """Returns a requires string that checks if the player can open the Trapdoor to continue (same as canOpenTrapdoor)."""
    return "(({requiresNoOptions()} AND {canOpenTrapdoor()}) OR ({requiresCloset()} AND {YamlDisabled(more_unlocks)} AND {canOpenTrapdoor()}) OR ({requiresMoreUnlocksOnly()} AND {canOpenTrapdoor()}) OR ({requiresCloset()} AND {YamlEnabled(more_unlocks)} AND {canOpenTrapdoor()}))"

def canFillBucket(world: World, multiworld: MultiWorld, state: CollectionState, player: int):
    """Returns a requires string that checks if the player can fill the bucket with water to continue."""
    return "(({requiresNoOptions()} AND |Bucket|) OR ({requiresCloset()} AND {YamlDisabled(more_unlocks)} AND |Bucket|) OR ({YamlDisabled(Roomsanity)} AND {requiresFill()} AND |Bucket|) OR ({requiresCloset()} AND {requiresFill()} AND |Bucket|))"

def canLightFire(world: World, multiworld: MultiWorld, state: CollectionState, player: int):
    """Returns a requires string that checks if the player can light the fire in the storage room to continue."""
    return "(({requiresNoOptions()} AND |Broom| AND |Lighter|) OR ({requiresCloset()} AND {YamlDisabled(more_unlocks)} AND |Broom| AND |Lighter|) OR ({requiresMoreUnlocksOnly()} AND |Broom| AND |Lighter|) OR ({requiresCloset()} AND {YamlEnabled(more_unlocks)} AND |Broom| AND |Lighter|))"

def canExtinguishFire(world: World, multiworld: MultiWorld, state: CollectionState, player: int):
    """Returns a requires string that checks if the player can extingusih the fire in the storage room to continue."""
    return "|Bucket with Water| AND {canFillBucket()} AND {canLightFire()}"

def canSolveFinalPuzzle(world: World, multiworld: MultiWorld, state: CollectionState, player: int):
    """Returns a requires string that checks if the player can solve the final puzzle to continue."""
    return "|Puzzle Piece 4| AND |Puzzle (3/4)| AND {canExtinguishFire()}"

def canGetKey(world: World, multiworld: MultiWorld, state: CollectionState, player: int):
    """Returns a requires string that checks if the player can obtain the key from solving the final puzzle to continue."""
    return "|Puzzle (4/4)| AND {canSolveFinalPuzzle()}"

def canUnlockEscapeDoor(world: World, multiworld: MultiWorld, state: CollectionState, player: int):
    """Returns a requires string that checks if the player can unlock the final door in order to escape the basement and win the game."""
    return "(({requiresNoOptions()} AND |Key|) OR ({requiresCloset()} AND {YamlDisabled(more_unlocks)} AND |Key|) OR ({YamlDisabled(Roomsanity)} AND {requiresUnlock()} AND |Key|) OR ({requiresCloset()} AND {requiresUnlock()} AND |Key|))"