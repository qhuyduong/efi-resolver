from binaryninja import BinaryView, BinaryReader, Symbol, SymbolType, VoidType, log_info, log_warn
import os
import struct
import uuid

guids = None

def init_guid_mapping():
    global guids
    if guids is not None:
        return

    guids = {}

    efi_defs = open(os.path.join(os.path.dirname(__file__), "types", "efi.c"), "r").readlines()

    for line in efi_defs:
        if line.startswith("///@guid"):
            guid = line.split("///@guid")[1].replace("{", "").replace("}", "").strip().split(",")
            guid = [int(x, 16) for x in guid]
            guid = struct.pack("<IHHBBBBBBBB", *guid)
        elif line.startswith("EFI_GUID"):
            name = line.split(" ")[1].strip().rstrip(";")
            guids[guid] = name

def apply_guid_name(bv: BinaryView, name: str, address: int):
    """Check if there is a function at the address. If not, then apply the EFI_GUID type and name it

    :param name: Name/symbol to apply to the GUID
    :param address: Address of the GUID
    """

    # Just to avoid a unlikely false positive and screwing up disassembly
    if bv.get_functions_at(address) != []:
        log_warn(f"There is code at {address}, not applying GUID type and name")
        return

    bv.define_user_symbol(Symbol(SymbolType.DataSymbol, address, name))
    type = bv.parse_type_string("EFI_GUID")
    bv.define_user_data_var(address, type[0])

def find_known_guids(bv: BinaryView):
    """Search for known GUIDs and apply names to matches not within a function"""
    br = BinaryReader(bv)

    for seg in bv.segments:
        for address in range(seg.start, seg.end):
            br.seek(address)
            data = br.read(16)
            if not data or len(data) != 16:
                continue

            name = guids.get(data)

            if name:
                var = bv.get_data_var_at(address) 
                if var is None or isinstance(var.type, VoidType):
                    log_info(f"Found {name} at {hex(address)} ({uuid.UUID(bytes_le=data)})")
                    apply_guid_name(bv, name, address)
