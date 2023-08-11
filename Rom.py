import enum
import hashlib
import itertools
import logging
import typing
from pathlib import Path

import bsdiff4

import Utils
from BaseClasses import MultiWorld
from Patch import APDeltaPatch


MD5_US_EU = "5fe47355a33e3fabec2a1607af88a404"


class WL4DeltaPatch(APDeltaPatch):
    hash = MD5_US_EU
    game = "Wario Land 4"
    patch_file_ending = ".apwl4"
    result_file_ending = ".gba"

    @classmethod
    def get_source_data(cls) -> bytes:
        return get_base_rom_bytes()


class AddressSpace(enum.Enum):
    SystemBus = 0x0000000
    ROM = 0x8000000


class LocalRom():
    def __init__(self, file: Path, name=None, hash=None):
        self.name = name
        self.hash = hash

        patch_path = Path(__file__).parent / "data" / "basepatch.bsdiff"
        with open(file, "rb") as rom_file, open(patch_path, "rb") as patch_file:
            rom_bytes = rom_file.read()
            patch_bytes = patch_file.read()
            self.buffer = bytearray(bsdiff4.patch(rom_bytes, patch_bytes))

    def read_bit(self, address: int, bit_number: int, space: AddressSpace = AddressSpace.SystemBus) -> bool:
        offset = AddressSpace.ROM.value - space.value
        address -= offset
        bitflag = (1 << bit_number)
        return ((self.buffer[address] & bitflag) != 0)

    def read_byte(self, address: int, space: AddressSpace = AddressSpace.SystemBus) -> int:
        offset = AddressSpace.ROM.value - space.value
        address -= offset
        return self.buffer[address]

    def read_bytes(self, startaddress: int, length: int, space: AddressSpace = AddressSpace.SystemBus) -> bytes:
        offset = AddressSpace.ROM.value - space.value
        startaddress -= offset
        return self.buffer[startaddress:startaddress + length]
    
    def read_halfword(self, address: int, space: AddressSpace = AddressSpace.SystemBus) -> int:
        assert address % 2 == 0, f"Misaligned halfword address: {address:x}"
        halfword = self.read_bytes(address, 2, space)
        return int.from_bytes(halfword, "little")
    
    def read_word(self, address: int, space: AddressSpace = AddressSpace.SystemBus) -> int:
        assert address % 4 == 0, f"Misaligned word address: {address:x}"
        word = self.read_bytes(address, 4, space)
        return int.from_bytes(word, "little")

    def write_byte(self, address: int, value: int, space: AddressSpace = AddressSpace.SystemBus):
        offset = AddressSpace.ROM.value - space.value
        address -= offset
        assert address >= 0, f"Address out of bounds: {address:x}"
        self.buffer[address] = value

    def write_bytes(self, startaddress: int, values, space: AddressSpace = AddressSpace.SystemBus):
        offset = AddressSpace.ROM.value - space.value
        startaddress -= offset
        assert startaddress >= 0, f"Address out of bounds: {startaddress:x}"
        self.buffer[startaddress:startaddress + len(values)] = values
    
    def write_halfword(self, address: int, value: int, space: AddressSpace = AddressSpace.SystemBus):
        assert address % 2 == 0, f"Misaligned halfword address: {address:x}"
        halfword = value.to_bytes(2, "little")
        self.write_bytes(address, halfword, space)
    
    def write_word(self, address: int, value: int, space: AddressSpace = AddressSpace.SystemBus):
        assert address % 4 == 0, f"Misaligned word address: {address:x}"
        word = value.to_bytes(4, "little")
        self.write_bytes(address, word, space)

    def write_to_file(self, file: Path):
        with open(file, 'wb') as stream:
            stream.write(self.buffer)


def _get_symbols(symbol_file: Path) -> typing.Dict[str, int]:
    symbols = {}
    with open(symbol_file, 'r') as stream:
        for line in stream:
            try:
                addr, label, *_ = line.split()
            except ValueError:
                continue

            # These labels are either generated by assembler directives or are
            # file/function local. Either way, not useful here
            if label[0] in ('@', '.'):
                continue

            addr = int(addr, base=16)
            symbols[label] = addr
    return symbols


def _get_charset(charset_file: Path) -> typing.Dict[str, int]:
    charset = {}
    with open(charset_file, 'r', encoding="utf-8") as stream:
        for line in stream:
            try:
                byte, character = line.strip().split("=")
            except ValueError:
                continue

            byte = int(byte, base=16)
            charset[character] = byte
    return charset


symbols = _get_symbols(Path(__file__).parent / "data/basepatch.sym")
charset = _get_charset(Path(__file__).parent / "data/charset.tbl")


# Unused; written only for my future reference
def shuffle_keyzer(rom: LocalRom, world: MultiWorld, player: int):
    # Use setting world.keyzer[player]
    rom.write_halfword(0x8075F18, 0x7849)  # ldrb r1, [r1, #1]  ; ItemGetFlgSet_LoadSavestateInfo2RAM()
    rom.write_halfword(0x808127C, 0x7848)  # ldrb r0, [r1, #1]  ; SeisanSave()
    rom.write_halfword(0x8081282, 0x7048)  # strb r0, [r1, #1]  ; SeisanSave()

    # TODO skip cutscene so Wario doesn't walk through locked doors


class MultiworldItem(typing.NamedTuple):
    receiver: str
    name: str


def fill_items(rom: LocalRom, world: MultiWorld, player: int):
    # Place item IDs and collect multiworld entries
    multiworld_items = {}
    for location in world.get_locations(player):
        itemid = location.item.code if location.item is not None else ...
        locationid = location.address
        playerid = location.item.player
        if itemid is None or locationid is None:
            continue
        locationid = locationid & 0xFF

        if location.native_item:
            itemid = itemid & 0xFF
        else:
            itemid = 0xF0
        itemname = location.item.name
        
        if playerid == player:
            playername = None
        else:
            playername = world.player_name[playerid]
            # There's no limit for the receivers' names, but limit them anyway
            # for consistency with the senders' names.
            if len(playername) > 16:
                playername = playername[:16]
            
        location_offset = symbols["itemlocationtable"] + locationid
        rom.write_byte(location_offset, itemid)

        if playername is not None:
            multiworld_items[locationid] = MultiworldItem(playername, itemname)
        else:
            multiworld_items[locationid] = None
    
    strings = create_strings(rom, multiworld_items)
    debug_string_list = [f'String addresses for player {world.player_name[player]}:']
    for str, addr in strings.items():
        debug_string_list.append(f'\t{repr(str)}: 0x{addr:x}')
    logging.debug('\n'.join(debug_string_list))
    write_multiworld_table(rom, multiworld_items, strings)


def create_strings(rom: LocalRom,
                   multiworld_items: typing.Dict[int, typing.Optional[MultiworldItem]]
                   ) -> typing.Dict[typing.Optional[str], int]:
    receivers = set()
    items = set()
    address = symbols["multiworldstringdump"]
    for item in filter(lambda i: i is not None, multiworld_items.values()):
        receivers.add(item.receiver)
        items.add(item.name)
        address += 8

    strings = {None: 0}  # Map a string to its address in game
    for string in itertools.chain(receivers, items):
        if string not in strings:
            # Cache, encode, and write the string, terminating with 0xFE
            strings[string] = address
            for c in string:
                rom.write_byte(address, charset.get(c, 0xFF))                
                address += 1
            rom.write_byte(address, 0xFE)
            address += 1
    return strings


def write_multiworld_table(rom: LocalRom,
                           multiworld_items: typing.Dict[int, typing.Optional[MultiworldItem]],
                           strings: typing.Dict[typing.Optional[str], int]):
    table_address = symbols["itemextdatatable"]
    entry_address = symbols["multiworldstringdump"]
    for locationid, item in multiworld_items.items():
        locationaddr = table_address + 4 * locationid
        if item is None:
            rom.write_word(locationaddr, 0)
        else:
            rom.write_word(locationaddr, entry_address)
            rom.write_word(entry_address, strings[item.receiver])
            rom.write_word(entry_address + 4, strings[item.name])
            entry_address += 8


def patch_rom(rom: LocalRom, world: MultiWorld, player: int):
    fill_items(rom, world, player)

    # Write player name and number
    player_name = bytes(world.player_name[player], "utf-8")
    if len(player_name) > 16:
        player_name = player_name[:16]
    rom.write_bytes(symbols["playername"], player_name)
    rom.write_byte(symbols["playerid"], player)
    
    # Set deathlink
    rom.write_byte(symbols["deathlinkflag"], world.death_link[player].value)
    
    # Force difficulty level
    mov_r0 = 0x2000 | world.difficulty[player].value # mov r0, #(world.difficulty[player].value)
    rom.write_halfword(0x8091558, mov_r0)  # SramtoWork_Load(): Force difficulty (anti-cheese)

    rom.write_halfword(0x8091F8E, 0x2001)  # movs r0, r1  ; ReadySub_Level(): Allow selecting S-Hard 
    rom.write_halfword(0x8091FCC, 0x46C0)  # nop  ; ReadySub_Level(): Force cursor to difficulty
    rom.write_halfword(0x8091FD2, 0xE007)  # b 0x8091FE4
    cmp_r0 = 0x2800 | world.difficulty[player].value  # cmp r0, #(world.difficulty[player].value)
    rom.write_halfword(0x8091FE4, cmp_r0)

    rom.write_halfword(0x8092268, 0x2001)  # movs r0, #1  ; ReadyObj_Win1Set(): Display S-Hard


def get_base_rom_bytes(file_name: str = "") -> bytes:
    base_rom_bytes = getattr(get_base_rom_bytes, "base_rom_bytes", None)
    if not base_rom_bytes:
        file_path = get_base_rom_path(file_name)
        base_rom_bytes = bytes(open(file_path, "rb").read())

        basemd5 = hashlib.md5()
        basemd5.update(base_rom_bytes)
        if MD5_US_EU != basemd5.hexdigest():
            raise Exception("Supplied base ROM does not match US/EU version."
                            "Please provide the correct ROM version")
        
        get_base_rom_bytes.base_rom_bytes = base_rom_bytes
    return base_rom_bytes


def get_base_rom_path(file_name: str = "") -> Path:
    options = Utils.get_options()
    if not file_name:
        file_name = options["wl4_options"]["rom_file"]

    file_path = Path(file_name)
    if file_path.exists():
        return file_path
    else:
        return Path(Utils.user_path(file_name))
