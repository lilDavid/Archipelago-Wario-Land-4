from enum import IntEnum
from typing import NamedTuple

from .options import Difficulty, Logic
from .rules import Requirement, logic_mode, difficulty, has, has_all, has_any, not_difficulty


class TrickLevel(IntEnum):
    INTERMEDIATE = Logic.option_intermediate
    ADVANCED = Logic.option_advanced
    ANYTHING_GOES = Logic.option_anything_goes


class TrickData(NamedTuple):
    difficulty: TrickLevel
    rule: Requirement | None = None


def trick(name: str):
    trick_data = trick_table[name]
    rule = trick_data.rule
    if rule is None:
        return logic_mode(trick_data.difficulty)
    return logic_mode(trick_data.difficulty) & rule


trick_table = {
    # Push the professor onto the pipe and jump off of him as he jumps up to flip himself over
    "PTP switch staircase stomp jump": TrickData(TrickLevel.INTERMEDIATE, has("Stomp Jump")),

    # Throw an enemy down at the blocks in the switch room
    "MJ with grab": TrickData(TrickLevel.INTERMEDIATE, has("Grab")),

    # Throw an enemy into the ceiling and enter with Puffy Wario
    "MJ CD box with grab": TrickData(TrickLevel.INTERMEDIATE, has("Grab")),

    # It's easier to hit him quickly the closer he is to the vines when you hit him
    "Fast Cractus without stomp jump": TrickData(TrickLevel.INTERMEDIATE),

    # Throw the Yeti at the block.
    "40BF CD box with heavy grab": TrickData(TrickLevel.ADVANCED, has("Heavy Grab")),

    # Ground pound the switches in the maze puzzle room by getting a running start and stomp jumping on the glass ball
    # right after the glass bird spits it out.
    "40BF glass ball stomp jump": TrickData(TrickLevel.INTERMEDIATE, has_all(["Stomp Jump", "Ground Pound"])),

    # Lure the Ringosuki toward the water and grab the apple in midair.
    "TTL transformation puzzle without heavy grab": TrickData(TrickLevel.ADVANCED),

    # Carry the Ringosuki down the left tunnel by ground pounding the blocks, then throw it onto the ledge at just the
    # right time. Then break the hard block as Fat Wario.
    "TTL without super ground pound": TrickData(TrickLevel.ANYTHING_GOES, has_all(["Ground Pound", "Heavy Grab"])),

    # Throw one of the lower pinballs at the ones on the ledges.
    "PZ fruit room without ground pound": TrickData(TrickLevel.INTERMEDIATE),

    # Carry a Ringosuki to the top of the room to move the pinballs using Fat Wario jumps. There are Ringosukis already
    # there on Hard and S-Hard, so this trick only affects Normal.
    "PZ Normal jungle room with Fat Wario": TrickData(TrickLevel.INTERMEDIATE, has("Heavy Grab")),

    # Carry a pinball to the top of a room, throw it upward, and stomp-jump it in midair.
    "PZ Normal jungle room with minion jump": TrickData(TrickLevel.ADVANCED, has("Stomp Jump")),

    # Throw a pinball up in the right spot to break the blocks leading to the ball in the cage. Beware of getting stuck
    # in the hole because you won't be able to throw the ball at the blocks below you.
    "PZ escape without ground pound": TrickData(TrickLevel.ADVANCED),

    # In open portals, you can grab a toy car and throw it at the blocks you'd normally ground pound at the beginning of
    # the level. Ground pound is still required for the escape.
    "TBB front with grab": TrickData(TrickLevel.INTERMEDIATE, has("Grab")),

    # You can minion-jump on toy cars in several parts of the Bouncy Wario room to access the diamond or CD box before
    # starting the escape and break blocks you'd otherwise need to ground pound.
    "TBB bouncy room alcove with minion jumps": TrickData(TrickLevel.ADVANCED, has_all(["Grab", "Stomp Jump"])),

    # Throw a Toy Car at the gray blocks.
    "DW gray square room with grab": TrickData(TrickLevel.INTERMEDIATE, not_difficulty(Difficulty.option_normal) & has("Grab")),

    # Ground pound from the top of the room to knock down a toy car, then stomp-jump it for the diamond
    "DR toy car tower diamond without grab": TrickData(TrickLevel.INTERMEDIATE, has_all(["Super Ground Pound", "Head Smash"])),

    # Go up the left path, take damage from the spikes, break the leftmost block, then collect the diamond from above.
    "DR toy car tower diamond damage boost": TrickData(TrickLevel.ADVANCED),

    # Break the blocks with a toy car or your head before starting the escape.
    "DR escape without ground pound": TrickData(TrickLevel.INTERMEDIATE, has_any(["Grab", "Head Smash"])),

    # Break the blocks with shoulder bashes, using invulnerability frames to hit the second one through the spikes.
    "DR escape with only swim": TrickData(TrickLevel.ADVANCED),

    # Drop off the top of the ladder and immediately start a ground pound
    "DR switch room block no dash attack": TrickData(TrickLevel.ADVANCED, has("Super Ground Pound")),

    # Break the wooden boxes by throwing the mummy enemies.
    "AN Onomi room with grab": TrickData(TrickLevel.INTERMEDIATE, has("Grab")),

    # Access the switch on hard by throwing the Marumen upward, stomping it in midair, and starting a ground pound.
    "HH escape minion jump": TrickData(
        TrickLevel.ADVANCED,
        difficulty(Difficulty.option_hard) & has_all(["Grab", "Stomp Jump", "Super Ground Pound"]),
    ),

    # To jump off the waves, start walking before you jump. When the waves start oscillating, jump at the apex.
    "Catbat without stomp jump": TrickData(TrickLevel.ADVANCED),

    # Repeatedly jump out of the river with good timing.
    "GP current room skip": TrickData(TrickLevel.ADVANCED),

    # Use the jewel piece box as a platform to escape the area with the blue block. You can safely collect the item
    # after breaking the blocks below the blue block.
    # NOTE: This trick isn't documented because it isn't relevant in practice yet: reaching Golden Passage always
    # requires ground pound because of Cractus and Catbat
    "GP Keyzer puzzle without ground pound": TrickData(TrickLevel.ADVANCED, has("Grab")),
}
