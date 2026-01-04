from __future__ import annotations

from typing import overload

from BaseClasses import CollectionState, Item, ItemClassification, MultiWorld

from test.bases import WorldTestBase


class WL4TestBase(WorldTestBase):
    game = "Wario Land 4"
    player = 1
    multiworld: MultiWorld

    starting_regions: list[str] = []
    _state_cache = {}

    def get_state(self, items):
        if (self.multiworld, tuple(self.starting_regions), tuple(items)) in self._state_cache:
            return self._state_cache[self.multiworld, tuple(self.starting_regions), tuple(items)]
        state = CollectionState(self.multiworld)
        for region_name in self.starting_regions:
            region = self.multiworld.get_region(region_name, 1)
            state.reachable_regions[1].add(region)
            for exit in region.exits:
                if exit.connected_region is not None:
                    state.blocked_connections[1].add(exit)
        for item in items:
            item.classification = ItemClassification.progression
            state.collect(item)
        state.sweep_for_advancements()
        self._state_cache[self.multiworld, tuple(self.starting_regions), tuple(items)] = state
        return state

    def get_path(self, state, region):
        def flist_to_iter(node):
            while node:
                value, node = node
                yield value

        from itertools import zip_longest
        reversed_path_as_flist = state.path.get(region, (region, None))
        string_path_flat = reversed(list(map(str, flist_to_iter(reversed_path_as_flist))))
        # Now we combine the flat string list into (region, exit) pairs
        pathsiter = iter(string_path_flat)
        pathpairs = zip_longest(pathsiter, pathsiter)
        return list(pathpairs)

    def run_location_tests(self, access_pool):
        for i, (location, access, *item_pool) in enumerate(access_pool):
            items = item_pool[0]
            all_except = item_pool[1] if len(item_pool) > 1 else None
            state = self._get_items(item_pool, all_except)
            path = self.get_path(state, self.multiworld.get_location(location, 1).parent_region)
            with self.subTest(msg="Reach Location", location=location, access=access, items=items,
                              all_except=all_except, path=path, entry=i):

                self.assertEqual(self.multiworld.get_location(location, 1).can_reach(state), access,
                                 f"failed {self.multiworld.get_location(location, 1)} with: {item_pool}")

            # check for partial solution
            if not all_except and access:  # we are not supposed to be able to reach location with partial inventory
                for missing_item in item_pool[0]:
                    with self.subTest(msg="Location reachable without required item", location=location,
                                      items=item_pool[0], missing_item=missing_item, entry=i):
                        state = self._get_items_partial(item_pool, missing_item)

                        self.assertEqual(self.multiworld.get_location(location, 1).can_reach(state), False,
                                         f"failed {self.multiworld.get_location(location, 1)}: succeeded with "
                                         f"{missing_item} removed from: {item_pool}")

    def run_entrance_tests(self, access_pool):
        for i, (entrance, access, *item_pool) in enumerate(access_pool):
            items = item_pool[0]
            all_except = item_pool[1] if len(item_pool) > 1 else None
            state = self._get_items(item_pool, all_except)
            path = self.get_path(state, self.multiworld.get_entrance(entrance, 1).parent_region)
            with self.subTest(msg="Reach Entrance", entrance=entrance, access=access, items=items,
                              all_except=all_except, path=path, entry=i):

                self.assertEqual(self.multiworld.get_entrance(entrance, 1).can_reach(state), access)

            # check for partial solution
            if not all_except and access:  # we are not supposed to be able to reach location with partial inventory
                for missing_item in item_pool[0]:
                    with self.subTest(msg="Entrance reachable without required item", entrance=entrance,
                                      items=item_pool[0], missing_item=missing_item, entry=i):
                        state = self._get_items_partial(item_pool, missing_item)
                        self.assertEqual(self.multiworld.get_entrance(entrance, 1).can_reach(state), False,
                                         f"failed {self.multiworld.get_entrance(entrance, 1)} with: {item_pool}")

    @overload
    def _create_items(self, items: str, player: int) -> Item:
        ...

    @overload
    def _create_items(self, items: list[str], player: int) -> list[Item]:
        ...

    def _create_items(self, items: str | list[str], player: int):
        singleton = False
        if isinstance(items, str):
            items = [items]
            singleton = True
        ret = [self.multiworld.worlds[player].create_item(item) for item in items]
        if singleton:
            return ret[0]
        return ret

    def _get_items(self, item_pool, all_except):
        if all_except and len(all_except) > 0:
            items = self.multiworld.itempool[:]
            items = [item for item in items if item.name not in all_except]
            items.extend(self._create_items(item_pool[0], 1))
        else:
            items = self._create_items(item_pool[0], 1)
        return self.get_state(items)

    def _get_items_partial(self, item_pool, missing_item):
        new_items = item_pool[0].copy()
        new_items.remove(missing_item)
        items = self._create_items(new_items, 1)
        return self.get_state(items)
