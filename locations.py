from typing import NamedTuple, Optional, Sequence

from BaseClasses import Location, Region

from .data import ItemFlag, Passage, ap_id_offset
from .options import Difficulty


class LocationData(NamedTuple):
    passage: Passage
    level: int
    flag: ItemFlag
    difficulties: Sequence[int]

    def level_id(self):
        return (self.passage, self.level, self.flag)

    def to_ap_id(self):
        return (ap_id_offset +
                ((self.passage * 6 + self.level) << 8) +
                sum(1 << difficulty << 5 for difficulty in self.difficulties) +
                self.flag.bit_length())


_NORMAL = (Difficulty.option_normal,)
_HARD = (Difficulty.option_hard,)
_S_HARD = (Difficulty.option_s_hard,)
_EASIER = _NORMAL + _HARD
_HARDER = _HARD + _S_HARD
_ALL = _NORMAL + _HARD + _S_HARD


    # Location                                                          Passage       Level  Bit in level data       Difficulties
location_table = {
    # Entry Passage
    # Hall of Hieroglyphs
    'Hall of Hieroglyphs - First Jewel Box':               LocationData(Passage.ENTRY,    0, ItemFlag.JEWEL_NE,      _ALL),
    'Hall of Hieroglyphs - Second Jewel Box':              LocationData(Passage.ENTRY,    0, ItemFlag.JEWEL_SE,      _ALL),
    'Hall of Hieroglyphs - Third Jewel Box':               LocationData(Passage.ENTRY,    0, ItemFlag.JEWEL_SW,      _ALL),
    'Hall of Hieroglyphs - Fourth Jewel Box':              LocationData(Passage.ENTRY,    0, ItemFlag.JEWEL_NW,      _ALL),
    'Hall of Hieroglyphs - Full Health Item Box':          LocationData(Passage.ENTRY,    0, ItemFlag.FULL_HEALTH,   _ALL),

    # Emerald Passage
    # Palm Tree Paradise
    'Palm Tree Paradise - First Box':                      LocationData(Passage.EMERALD,  0, ItemFlag.JEWEL_NE,      _NORMAL),
    'Palm Tree Paradise - Ledge Box':                      LocationData(Passage.EMERALD,  0, ItemFlag.JEWEL_NE,      _HARD),
    'Palm Tree Paradise - Dead End Box':                   LocationData(Passage.EMERALD,  0, ItemFlag.JEWEL_NE,      _S_HARD),
    'Palm Tree Paradise - Box Before Cave':                LocationData(Passage.EMERALD,  0, ItemFlag.JEWEL_SE,      _NORMAL),
    'Palm Tree Paradise - Hidden Box':                     LocationData(Passage.EMERALD,  0, ItemFlag.JEWEL_SE,      _HARDER),
    'Palm Tree Paradise - Platform Cave Jewel Box':        LocationData(Passage.EMERALD,  0, ItemFlag.JEWEL_SW,      _ALL),
    'Palm Tree Paradise - Ladder Cave Box':                LocationData(Passage.EMERALD,  0, ItemFlag.JEWEL_NW,      _ALL),
    'Palm Tree Paradise - CD Box':                         LocationData(Passage.EMERALD,  0, ItemFlag.CD,            _ALL),
    'Palm Tree Paradise - Full Health Item Box':           LocationData(Passage.EMERALD,  0, ItemFlag.FULL_HEALTH,   _ALL),

    # Wildflower Fields
    'Wildflower Fields - Current Cave Box':                LocationData(Passage.EMERALD,  1, ItemFlag.JEWEL_NE,      _ALL),
    'Wildflower Fields - Sunflower Jewel Box':             LocationData(Passage.EMERALD,  1, ItemFlag.JEWEL_SE,      _NORMAL),
    'Wildflower Fields - Sunflower Box':                   LocationData(Passage.EMERALD,  1, ItemFlag.JEWEL_SE,      _HARDER),
    'Wildflower Fields - Slope Room Box':                  LocationData(Passage.EMERALD,  1, ItemFlag.JEWEL_SW,      _NORMAL),
    'Wildflower Fields - 8-Shaped Cave Box':               LocationData(Passage.EMERALD,  1, ItemFlag.JEWEL_SW,      _HARDER),
    'Wildflower Fields - Beezley Box':                     LocationData(Passage.EMERALD,  1, ItemFlag.JEWEL_NW,      _ALL),
    'Wildflower Fields - CD Box':                          LocationData(Passage.EMERALD,  1, ItemFlag.CD,            _ALL),
    'Wildflower Fields - Full Health Item Box':            LocationData(Passage.EMERALD,  1, ItemFlag.FULL_HEALTH,   _NORMAL),

    # Mystic Lake
    'Mystic Lake - Air Pocket Box':                        LocationData(Passage.EMERALD,  2, ItemFlag.JEWEL_NE,      _NORMAL),
    'Mystic Lake - Large Cave Box':                        LocationData(Passage.EMERALD,  2, ItemFlag.JEWEL_NE,      _HARDER),
    'Mystic Lake - Hill Room Box':                         LocationData(Passage.EMERALD,  2, ItemFlag.JEWEL_SE,      _NORMAL),
    'Mystic Lake - Small Cave Box':                        LocationData(Passage.EMERALD,  2, ItemFlag.JEWEL_SE,      _HARD),
    'Mystic Lake - Rock Cave Box':                         LocationData(Passage.EMERALD,  2, ItemFlag.JEWEL_SE,      _S_HARD),
    'Mystic Lake - Cavern Box':                            LocationData(Passage.EMERALD,  2, ItemFlag.JEWEL_SW,      _NORMAL),
    'Mystic Lake - Spring Cave Box':                       LocationData(Passage.EMERALD,  2, ItemFlag.JEWEL_SW,      _HARDER),
    'Mystic Lake - Box Before Bridge':                     LocationData(Passage.EMERALD,  2, ItemFlag.JEWEL_NW,      _NORMAL),
    'Mystic Lake - Lake Exit Bubble Box':                  LocationData(Passage.EMERALD,  2, ItemFlag.JEWEL_NW,      _HARDER),
    'Mystic Lake - CD Box':                                LocationData(Passage.EMERALD,  2, ItemFlag.CD,            _ALL),
    'Mystic Lake - Full Health Item Box':                  LocationData(Passage.EMERALD,  2, ItemFlag.FULL_HEALTH,   _ALL),

    # Monsoon Jungle
    'Monsoon Jungle - Spiky Box':                          LocationData(Passage.EMERALD,  3, ItemFlag.JEWEL_NE,      _NORMAL),
    'Monsoon Jungle - Escape Climb Box':                   LocationData(Passage.EMERALD,  3, ItemFlag.JEWEL_NE,      _HARD),
    'Monsoon Jungle - Brown Pipe Cave Box':                LocationData(Passage.EMERALD,  3, ItemFlag.JEWEL_NE,      _S_HARD),
    'Monsoon Jungle - Fat Plummet Box':                    LocationData(Passage.EMERALD,  3, ItemFlag.JEWEL_SE,      _ALL),
    'Monsoon Jungle - Descent Box':                        LocationData(Passage.EMERALD,  3, ItemFlag.JEWEL_SW,      _NORMAL),
    'Monsoon Jungle - Puffy Hallway Box':                  LocationData(Passage.EMERALD,  3, ItemFlag.JEWEL_SW,      _HARDER),
    'Monsoon Jungle - Buried Cave Box':                    LocationData(Passage.EMERALD,  3, ItemFlag.JEWEL_NW,      _ALL),
    'Monsoon Jungle - CD Box':                             LocationData(Passage.EMERALD,  3, ItemFlag.CD,            _ALL),
    'Monsoon Jungle - Full Health Item Box':               LocationData(Passage.EMERALD,  3, ItemFlag.FULL_HEALTH,   _ALL),

    'Cractus - 0:55':                                      LocationData(Passage.EMERALD,  4, ItemFlag.JEWEL_NE,      _ALL),
    'Cractus - 0:35':                                      LocationData(Passage.EMERALD,  4, ItemFlag.JEWEL_SE,      _ALL),
    'Cractus - 0:15':                                      LocationData(Passage.EMERALD,  4, ItemFlag.JEWEL_SW,      _ALL),

    # Ruby Passage
    # The Curious Factory
    'The Curious Factory - First Drop Box':                LocationData(Passage.RUBY,     0, ItemFlag.JEWEL_NE,      _NORMAL),
    'The Curious Factory - Thin Gap Box':                  LocationData(Passage.RUBY,     0, ItemFlag.JEWEL_NE,      _HARDER),
    'The Curious Factory - Early Escape Box':              LocationData(Passage.RUBY,     0, ItemFlag.JEWEL_SE,      _NORMAL),
    'The Curious Factory - Conveyor Room Box':             LocationData(Passage.RUBY,     0, ItemFlag.JEWEL_SE,      _HARDER),
    'The Curious Factory - Late Escape Box':               LocationData(Passage.RUBY,     0, ItemFlag.JEWEL_SW,      _NORMAL),
    'The Curious Factory - Underground Chamber Box':       LocationData(Passage.RUBY,     0, ItemFlag.JEWEL_SW,      _HARDER),
    'The Curious Factory - Frog Switch Room Box':          LocationData(Passage.RUBY,     0, ItemFlag.JEWEL_NW,      _NORMAL),
    'The Curious Factory - Gear Elevator Box':             LocationData(Passage.RUBY,     0, ItemFlag.JEWEL_NW,      _HARDER),
    'The Curious Factory - CD Box':                        LocationData(Passage.RUBY,     0, ItemFlag.CD,            _ALL),

    # The Toxic Landfill
    'The Toxic Landfill - Portal Room Box':                LocationData(Passage.RUBY,     1, ItemFlag.JEWEL_NE,      _NORMAL),
    'The Toxic Landfill - Box Above Portal':               LocationData(Passage.RUBY,     1, ItemFlag.JEWEL_NE,      _HARDER),
    'The Toxic Landfill - Fat Room Box':                   LocationData(Passage.RUBY,     1, ItemFlag.JEWEL_SE,      _ALL),
    'The Toxic Landfill - Spring Room Box':                LocationData(Passage.RUBY,     1, ItemFlag.JEWEL_SW,      _NORMAL),
    'The Toxic Landfill - Current Circle Box':             LocationData(Passage.RUBY,     1, ItemFlag.JEWEL_SW,      _HARDER),
    'The Toxic Landfill - Ledge Box':                      LocationData(Passage.RUBY,     1, ItemFlag.JEWEL_NW,      _NORMAL),
    'The Toxic Landfill - Transformation Puzzle Box':      LocationData(Passage.RUBY,     1, ItemFlag.JEWEL_NW,      _HARDER),
    'The Toxic Landfill - CD Box':                         LocationData(Passage.RUBY,     1, ItemFlag.CD,            _ALL),
    'The Toxic Landfill - Full Health Item Box':           LocationData(Passage.RUBY,     1, ItemFlag.FULL_HEALTH,   _NORMAL),

    # 40 Below Fridge
    '40 Below Fridge - Looping Room Box':                  LocationData(Passage.RUBY,     2, ItemFlag.JEWEL_NE,      _ALL),
    '40 Below Fridge - Maze Room Box':                     LocationData(Passage.RUBY,     2, ItemFlag.JEWEL_SE,      _ALL),
    '40 Below Fridge - Snowman Puzzle Lower Box':          LocationData(Passage.RUBY,     2, ItemFlag.JEWEL_SW,      _ALL),
    '40 Below Fridge - Snowman Puzzle Upper Box':          LocationData(Passage.RUBY,     2, ItemFlag.JEWEL_NW,      _ALL),
    '40 Below Fridge - CD Box':                            LocationData(Passage.RUBY,     2, ItemFlag.CD,            _ALL),

    # Pinball Zone
    'Pinball Zone - Rolling Room Box':                     LocationData(Passage.RUBY,     3, ItemFlag.JEWEL_NE,      _EASIER),
    'Pinball Zone - Switch Room Box':                      LocationData(Passage.RUBY,     3, ItemFlag.JEWEL_NE,      _S_HARD),
    'Pinball Zone - Fruit Room Box':                       LocationData(Passage.RUBY,     3, ItemFlag.JEWEL_SE,      _ALL),
    'Pinball Zone - Jungle Room Box':                      LocationData(Passage.RUBY,     3, ItemFlag.JEWEL_SW,      _ALL),
    'Pinball Zone - Snow Room Box':                        LocationData(Passage.RUBY,     3, ItemFlag.JEWEL_NW,      _ALL),
    'Pinball Zone - CD Box':                               LocationData(Passage.RUBY,     3, ItemFlag.CD,            _ALL),
    'Pinball Zone - Full Health Item Box':                 LocationData(Passage.RUBY,     3, ItemFlag.FULL_HEALTH,   _EASIER),
    'Pinball Zone - Pink Room Full Health Item Box':       LocationData(Passage.RUBY,     3, ItemFlag.FULL_HEALTH,   _S_HARD),
    'Pinball Zone - Rolling Room Full Health Item Box':    LocationData(Passage.RUBY,     3, ItemFlag.FULL_HEALTH_2, _S_HARD),

    'Cuckoo Condor - 0:55':                                LocationData(Passage.RUBY,     4, ItemFlag.JEWEL_NE,      _ALL),
    'Cuckoo Condor - 0:35':                                LocationData(Passage.RUBY,     4, ItemFlag.JEWEL_SE,      _ALL),
    'Cuckoo Condor - 0:15':                                LocationData(Passage.RUBY,     4, ItemFlag.JEWEL_SW,      _ALL),

    # Topaz Passage
    # Toy Block Tower
    'Toy Block Tower - Toy Car Overhang Box':              LocationData(Passage.TOPAZ,    0, ItemFlag.JEWEL_NE,      _EASIER),
    'Toy Block Tower - Tower Exterior Top Box':            LocationData(Passage.TOPAZ,    0, ItemFlag.JEWEL_NE,      _S_HARD),
    'Toy Block Tower - Hidden Tower Room Box':             LocationData(Passage.TOPAZ,    0, ItemFlag.JEWEL_SE,      _NORMAL),
    'Toy Block Tower - Digging Room Box':                  LocationData(Passage.TOPAZ,    0, ItemFlag.JEWEL_SE,      _HARDER),
    'Toy Block Tower - Fire Box':                          LocationData(Passage.TOPAZ,    0, ItemFlag.JEWEL_SW,      _NORMAL),
    'Toy Block Tower - Hidden Falling Block Door Box':     LocationData(Passage.TOPAZ,    0, ItemFlag.JEWEL_SW,      _HARD),
    'Toy Block Tower - Bonfire Block Box':                 LocationData(Passage.TOPAZ,    0, ItemFlag.JEWEL_SW,      _S_HARD),
    'Toy Block Tower - Red Pipe Box':                      LocationData(Passage.TOPAZ,    0, ItemFlag.JEWEL_NW,      _NORMAL),
    'Toy Block Tower - Escape Ledge Box':                  LocationData(Passage.TOPAZ,    0, ItemFlag.JEWEL_NW,      _HARDER),
    'Toy Block Tower - CD Box':                            LocationData(Passage.TOPAZ,    0, ItemFlag.CD,            _ALL),
    'Toy Block Tower - Full Health Item Box':              LocationData(Passage.TOPAZ,    0, ItemFlag.FULL_HEALTH,   _EASIER),

    # The Big Board
    'The Big Board - First Box':                           LocationData(Passage.TOPAZ,    1, ItemFlag.JEWEL_NE,      _NORMAL),
    'The Big Board - Hard Fire Room Box':                  LocationData(Passage.TOPAZ,    1, ItemFlag.JEWEL_NE,      _HARDER),
    'The Big Board - Normal Fire Room Box':                LocationData(Passage.TOPAZ,    1, ItemFlag.JEWEL_SE,      _NORMAL),
    'The Big Board - Hard Enemy Room Box':                 LocationData(Passage.TOPAZ,    1, ItemFlag.JEWEL_SE,      _HARDER),
    'The Big Board - Normal Enemy Room Box':               LocationData(Passage.TOPAZ,    1, ItemFlag.JEWEL_SW,      _NORMAL),
    'The Big Board - Fat Room Box':                        LocationData(Passage.TOPAZ,    1, ItemFlag.JEWEL_SW,      _HARDER),
    'The Big Board - Toy Car Box':                         LocationData(Passage.TOPAZ,    1, ItemFlag.JEWEL_NW,      _NORMAL),
    'The Big Board - Flat Room Box':                       LocationData(Passage.TOPAZ,    1, ItemFlag.JEWEL_NW,      _HARDER),
    'The Big Board - CD Box':                              LocationData(Passage.TOPAZ,    1, ItemFlag.CD,            _ALL),
    'The Big Board - Full Health Item Box':                LocationData(Passage.TOPAZ,    1, ItemFlag.FULL_HEALTH,   _EASIER),

    # Doodle Woods
    'Doodle Woods - Box Behind Wall':                      LocationData(Passage.TOPAZ,    2, ItemFlag.JEWEL_NE,      _NORMAL),
    'Doodle Woods - Gray Square Box':                      LocationData(Passage.TOPAZ,    2, ItemFlag.JEWEL_NE,      _HARDER),
    'Doodle Woods - Orange Escape Box':                    LocationData(Passage.TOPAZ,    2, ItemFlag.JEWEL_SE,      _NORMAL),
    'Doodle Woods - Pink Circle Box':                      LocationData(Passage.TOPAZ,    2, ItemFlag.JEWEL_SE,      _HARDER),
    'Doodle Woods - Buried Door Box':                      LocationData(Passage.TOPAZ,    2, ItemFlag.JEWEL_SW,      _NORMAL),
    'Doodle Woods - Purple Square Box':                    LocationData(Passage.TOPAZ,    2, ItemFlag.JEWEL_SW,      _HARDER),
    'Doodle Woods - Blue Escape Box':                      LocationData(Passage.TOPAZ,    2, ItemFlag.JEWEL_NW,      _NORMAL),
    'Doodle Woods - Blue Circle Box':                      LocationData(Passage.TOPAZ,    2, ItemFlag.JEWEL_NW,      _HARDER),
    'Doodle Woods - CD Box':                               LocationData(Passage.TOPAZ,    2, ItemFlag.CD,            _ALL),

    # Domino Row
    'Domino Row - Racing Box':                             LocationData(Passage.TOPAZ,    3, ItemFlag.JEWEL_NE,      _ALL),
    'Domino Row - Rolling Box':                            LocationData(Passage.TOPAZ,    3, ItemFlag.JEWEL_SE,      _ALL),
    'Domino Row - Swimming Detour Box':                    LocationData(Passage.TOPAZ,    3, ItemFlag.JEWEL_SW,      _EASIER),
    'Domino Row - Swimming Room Escape Box':               LocationData(Passage.TOPAZ,    3, ItemFlag.JEWEL_SW,      _S_HARD),
    'Domino Row - Keyzer Room Box':                        LocationData(Passage.TOPAZ,    3, ItemFlag.JEWEL_NW,      _ALL),
    'Domino Row - CD Box':                                 LocationData(Passage.TOPAZ,    3, ItemFlag.CD,            _ALL),

    'Aerodent - 0:55':                                     LocationData(Passage.TOPAZ,    4, ItemFlag.JEWEL_NE,      _ALL),
    'Aerodent - 0:35':                                     LocationData(Passage.TOPAZ,    4, ItemFlag.JEWEL_SE,      _ALL),
    'Aerodent - 0:15':                                     LocationData(Passage.TOPAZ,    4, ItemFlag.JEWEL_SW,      _ALL),

    # Sapphire Passage
    # Crescent Moon Village
    'Crescent Moon Village - Agile Bat Box':               LocationData(Passage.SAPPHIRE, 0, ItemFlag.JEWEL_NE,      _NORMAL),
    'Crescent Moon Village - Agile Bat Hidden Box':        LocationData(Passage.SAPPHIRE, 0, ItemFlag.JEWEL_NE,      _HARDER),
    'Crescent Moon Village - Metal Platform Box':          LocationData(Passage.SAPPHIRE, 0, ItemFlag.JEWEL_SE,      _NORMAL),
    'Crescent Moon Village - Metal Platform Rolling Box':  LocationData(Passage.SAPPHIRE, 0, ItemFlag.JEWEL_SE,      _HARDER),
    'Crescent Moon Village - Rolling Box':                 LocationData(Passage.SAPPHIRE, 0, ItemFlag.JEWEL_SW,      _NORMAL),
    'Crescent Moon Village - !-Switch Rolling Box':        LocationData(Passage.SAPPHIRE, 0, ItemFlag.JEWEL_SW,      _HARDER),
    'Crescent Moon Village - Sewer Box':                   LocationData(Passage.SAPPHIRE, 0, ItemFlag.JEWEL_NW,      _ALL),
    'Crescent Moon Village - CD Box':                      LocationData(Passage.SAPPHIRE, 0, ItemFlag.CD,            _ALL),

    # Arabian Night
    'Arabian Night - Onomi Box':                           LocationData(Passage.SAPPHIRE, 1, ItemFlag.JEWEL_NE,      _ALL),
    'Arabian Night - Flying Carpet Overhang Box':          LocationData(Passage.SAPPHIRE, 1, ItemFlag.JEWEL_SE,      _NORMAL),
    'Arabian Night - Flying Carpet Dash Attack Box':       LocationData(Passage.SAPPHIRE, 1, ItemFlag.JEWEL_SE,      _HARDER),
    'Arabian Night - Zombie Plummet Box':                  LocationData(Passage.SAPPHIRE, 1, ItemFlag.JEWEL_SW,      _NORMAL),
    'Arabian Night - Kool-Aid Box':                        LocationData(Passage.SAPPHIRE, 1, ItemFlag.JEWEL_SW,      _HARDER),
    'Arabian Night - Sewer Box':                           LocationData(Passage.SAPPHIRE, 1, ItemFlag.JEWEL_NW,      _ALL),
    'Arabian Night - CD Box':                              LocationData(Passage.SAPPHIRE, 1, ItemFlag.CD,            _ALL),

    # Fiery Cavern
    'Fiery Cavern - Lava Dodging Box':                     LocationData(Passage.SAPPHIRE, 2, ItemFlag.JEWEL_NE,      _NORMAL),
    'Fiery Cavern - Ice Beyond Door Box':                  LocationData(Passage.SAPPHIRE, 2, ItemFlag.JEWEL_NE,      _HARDER),
    'Fiery Cavern - Long Lava Geyser Box':                 LocationData(Passage.SAPPHIRE, 2, ItemFlag.JEWEL_SE,      _ALL),
    'Fiery Cavern - Ice Detour Box':                       LocationData(Passage.SAPPHIRE, 2, ItemFlag.JEWEL_SW,      _ALL),
    'Fiery Cavern - Snowman Box':                          LocationData(Passage.SAPPHIRE, 2, ItemFlag.JEWEL_NW,      _ALL),
    'Fiery Cavern - CD Box':                               LocationData(Passage.SAPPHIRE, 2, ItemFlag.CD,            _ALL),

    # Hotel Horror
    'Hotel Horror - 1F Hallway Box':                       LocationData(Passage.SAPPHIRE, 3, ItemFlag.JEWEL_NE,      _NORMAL),
    'Hotel Horror - Room 102 Box':                         LocationData(Passage.SAPPHIRE, 3, ItemFlag.JEWEL_NE,      _HARDER),
    'Hotel Horror - 2F Hallway Box':                       LocationData(Passage.SAPPHIRE, 3, ItemFlag.JEWEL_SE,      _NORMAL),
    'Hotel Horror - Room 303 Box':                         LocationData(Passage.SAPPHIRE, 3, ItemFlag.JEWEL_SE,      _HARDER),
    'Hotel Horror - 3F Hallway Box':                       LocationData(Passage.SAPPHIRE, 3, ItemFlag.JEWEL_SW,      _NORMAL),
    'Hotel Horror - Room 402 Box':                         LocationData(Passage.SAPPHIRE, 3, ItemFlag.JEWEL_SW,      _HARDER),
    'Hotel Horror - 4F Hallway Box':                       LocationData(Passage.SAPPHIRE, 3, ItemFlag.JEWEL_NW,      _NORMAL),
    'Hotel Horror - Exterior Box':                         LocationData(Passage.SAPPHIRE, 3, ItemFlag.JEWEL_NW,      _HARDER),
    'Hotel Horror - CD Box':                               LocationData(Passage.SAPPHIRE, 3, ItemFlag.CD,            _ALL),

    'Catbat - 0:55':                                       LocationData(Passage.SAPPHIRE, 4, ItemFlag.JEWEL_NE,      _ALL),
    'Catbat - 0:35':                                       LocationData(Passage.SAPPHIRE, 4, ItemFlag.JEWEL_SE,      _ALL),
    'Catbat - 0:15':                                       LocationData(Passage.SAPPHIRE, 4, ItemFlag.JEWEL_SW,      _ALL),

    # Golden Pyramid
    # Golden Passage
    'Golden Passage - Current Puzzle Box':                 LocationData(Passage.GOLDEN,   0, ItemFlag.JEWEL_NE,      _ALL),
    'Golden Passage - River Box':                          LocationData(Passage.GOLDEN,   0, ItemFlag.JEWEL_SE,      _ALL),
    'Golden Passage - Bat Room Box':                       LocationData(Passage.GOLDEN,   0, ItemFlag.JEWEL_SW,      _ALL),
    'Golden Passage - Mad Scienstein Box':                 LocationData(Passage.GOLDEN,   0, ItemFlag.JEWEL_NW,      _ALL),
}


location_name_to_id = {name: data.to_ap_id() for name, data in location_table.items()}


class WL4Location(Location):
    game: str = 'Wario Land 4'
    passage: Optional[int]
    level: Optional[int]
    flag: Optional[int]
    difficulty: Sequence[int]

    def __init__(self, player: int, name: str, parent: Optional[Region] = None):
        super().__init__(player, name, location_name_to_id.get(name, None), parent)
        self.passage, self.level, self.flag, self.difficulty = location_table[name]

    def entry_offset(self):
        if self.is_event:
            return None
        return self.flag.bit_length() - (1 if self.flag < ItemFlag.KEYZER else 2)

    def level_offset(self):
        if self.is_event:
            return None
        return (self.passage * 5 + self.level) * (len(ItemFlag) - 1)

def get_level_locations(passage: Passage, level: int):
    return map(lambda l: l[0], get_level_location_data(passage, level))

def get_level_location_data(passage: Passage, level: int):
    return filter(lambda l: l[1].level_id() == (passage, level), location_table.items())
