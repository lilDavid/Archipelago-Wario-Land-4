import itertools
from unittest import TestCase

from ..data import Passage
from ..items import get_jewel_pieces_by_passage
from ..locations import get_level_locations, location_table
from ..options import Difficulty
from ..region_data import LocationType, level_table


main_levels = ["Palm Tree Paradise", "Wildflower Fields", "Mystic Lake", "Monsoon Jungle",
               "The Curious Factory", "The Toxic Landfill", "40 Below Fridge", "Pinball Zone",
               "Toy Block Tower", "The Big Board", "Doodle Woods", "Domino Row",
               "Crescent Moon Village", "Arabian Night", "Fiery Cavern", "Hotel Horror"]

class TestHelpers(TestCase):
    def test_item_filter(self):
        """Ensure item filters and item names match."""
        for passage in Passage:
            with self.subTest(passage.long_name()):
                pieces = get_jewel_pieces_by_passage(passage)
                assert all(map(lambda p: passage.short_name() in p, pieces))

    def test_location_filter(self):
        """Test that the location filter and location names match"""
        with self.subTest("Hall of Hieroglyphs"):
            checks = get_level_locations(Passage.ENTRY, 0)
            assert all(map(lambda l: l.startswith("Hall of Hieroglyphs"), checks))

        for passage in range(1, 5):
            for level in range(4):
                level_name = main_levels[passage * 4 - 4 + level]
                with self.subTest(level_name):
                    checks = get_level_locations(Passage(passage), level)
                    assert all(map(lambda l: l.startswith(level_name), checks))

        with self.subTest("Golden Passage"):
            checks = get_level_locations(Passage.GOLDEN, 0)
            assert all(map(lambda l: l.startswith("Golden Passage"), checks))


class TestLocationExistence(TestCase):
    def _test_locations_match(self, difficulty):
        locations_from_table = {
            name
            for name, data in location_table.items()
            if difficulty in data.difficulties and data.level < 4
        }
        locations_from_tree = {
            f"{level_name} - {location.name}"
            for level_name, level in level_table.items()
            for region in level.regions
            for location in region.locations
            if difficulty in location.difficulties and location.type not in (LocationType.KEYZER, LocationType.SWITCH)
        }
        self.assertEqual(locations_from_table, locations_from_tree)

    def test_normal_locations_match(self):
        self._test_locations_match(Difficulty.option_normal)

    def test_hard_locations_match(self):
        self._test_locations_match(Difficulty.option_hard)

    def test_s_hard_locations_match(self):
        self._test_locations_match(Difficulty.option_s_hard)
