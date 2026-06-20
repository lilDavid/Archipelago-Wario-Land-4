from ..bases import WL4TestBase


class TestPyramidAccess(WL4TestBase):
    pass


class TestVanillaPyramid(TestPyramidAccess):
    def test_pyramid_access(self):
        self.run_entrance_tests([
            ["Golden Pyramid Entrance", False, []],
            ["Golden Pyramid Entrance", False,
             ["Entry Passage Clear", "Ruby Passage Clear", "Topaz Passage Clear", "Sapphire Passage Clear"]],
            ["Golden Pyramid Entrance", False,
             ["Entry Passage Clear", "Emerald Passage Clear", "Topaz Passage Clear", "Sapphire Passage Clear"]],
            ["Golden Pyramid Entrance", False,
             ["Entry Passage Clear", "Emerald Passage Clear", "Ruby Passage Clear", "Sapphire Passage Clear"]],
            ["Golden Pyramid Entrance", False,
             ["Entry Passage Clear", "Emerald Passage Clear", "Ruby Passage Clear", "Topaz Passage Clear"]],
            ["Golden Pyramid Entrance", True,
             ["Emerald Passage Clear", "Ruby Passage Clear", "Topaz Passage Clear", "Sapphire Passage Clear"]],
        ])


class TestAnyPassageBoss(TestPyramidAccess):
    options = {"required_bosses": 1}

    def test_pyramid_access(self):
        self.run_entrance_tests([
            ["Golden Pyramid Entrance", False, []],
            ["Golden Pyramid Entrance", False, ["Entry Passage Clear"]],
            ["Golden Pyramid Entrance", True, ["Emerald Passage Clear"]],
            ["Golden Pyramid Entrance", True, ["Ruby Passage Clear"]],
            ["Golden Pyramid Entrance", True, ["Topaz Passage Clear"]],
            ["Golden Pyramid Entrance", True, ["Sapphire Passage Clear"]],
        ])


class TestNoPassageBosses(TestPyramidAccess):
    options = {"required_bosses": 0}

    def test_pyramid_access(self):
        self.run_entrance_tests([
            ["Golden Pyramid Entrance", True, []],
        ])

class TestAllBosses(TestPyramidAccess):
    options = {"required_bosses": 5, "include_entry_passage": True}

    def test_pyramid_access(self):
        self.run_entrance_tests([
            ["Golden Pyramid Entrance", False, []],
            ["Golden Pyramid Entrance", False,
             ["Emerald Passage Clear", "Ruby Passage Clear", "Topaz Passage Clear", "Sapphire Passage Clear"]],
            ["Golden Pyramid Entrance", False,
             ["Entry Passage Clear", "Ruby Passage Clear", "Topaz Passage Clear", "Sapphire Passage Clear"]],
            ["Golden Pyramid Entrance", False,
             ["Entry Passage Clear", "Emerald Passage Clear", "Topaz Passage Clear", "Sapphire Passage Clear"]],
            ["Golden Pyramid Entrance", False,
             ["Entry Passage Clear", "Emerald Passage Clear", "Ruby Passage Clear", "Sapphire Passage Clear"]],
            ["Golden Pyramid Entrance", False,
             ["Entry Passage Clear", "Emerald Passage Clear", "Ruby Passage Clear", "Topaz Passage Clear"]],
            ["Golden Pyramid Entrance", True,
             ["Entry Passage Clear", "Emerald Passage Clear", "Ruby Passage Clear", "Topaz Passage Clear", "Sapphire Passage Clear"]],
        ])


class TestAny4Bosses(TestPyramidAccess):
    options = {"required_bosses": 4, "include_entry_passage": True}

    def test_pyramid_access(self):
        self.run_entrance_tests([
            ["Golden Pyramid Entrance", False, []],
            ["Golden Pyramid Entrance", True,
             ["Emerald Passage Clear", "Ruby Passage Clear", "Topaz Passage Clear", "Sapphire Passage Clear"]],
            ["Golden Pyramid Entrance", True,
             ["Entry Passage Clear", "Ruby Passage Clear", "Topaz Passage Clear", "Sapphire Passage Clear"]],
            ["Golden Pyramid Entrance", True,
             ["Entry Passage Clear", "Emerald Passage Clear", "Topaz Passage Clear", "Sapphire Passage Clear"]],
            ["Golden Pyramid Entrance", True,
             ["Entry Passage Clear", "Emerald Passage Clear", "Ruby Passage Clear", "Sapphire Passage Clear"]],
            ["Golden Pyramid Entrance", True,
             ["Entry Passage Clear", "Emerald Passage Clear", "Ruby Passage Clear", "Topaz Passage Clear"]],
        ])


class TestAnyBoss(TestPyramidAccess):
    options = {"required_bosses": 1, "include_entry_passage": True}

    def test_pyramid_access(self):
        self.run_entrance_tests([
            ["Golden Pyramid Entrance", False, []],
            ["Golden Pyramid Entrance", True, ["Entry Passage Clear"]],
            ["Golden Pyramid Entrance", True, ["Emerald Passage Clear"]],
            ["Golden Pyramid Entrance", True, ["Ruby Passage Clear"]],
            ["Golden Pyramid Entrance", True, ["Topaz Passage Clear"]],
            ["Golden Pyramid Entrance", True, ["Sapphire Passage Clear"]],
        ])


class TestNoBosses(TestPyramidAccess):
    options = {"required_bosses": 0, "include_entry_passage": True}

    def test_pyramid_access(self):
        self.run_entrance_tests([
            ["Golden Pyramid Entrance", True, []],
        ])

