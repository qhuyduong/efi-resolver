from binaryninja import PluginCommand, BinaryView, BackgroundTaskThread, log_alert
from .protocols import init_protocol_mapping, define_handle_protocol_types, define_open_protocol_types, define_locate_protocol_types
from .guids import init_guid_mapping, find_known_guids
from .system_table import import_types_from_headers, retype_entry_function, propagate_system_table_pointer

def resolve_efi(bv: BinaryView):
    class Task(BackgroundTaskThread):
        def __init__(self, bv: BinaryView):
            super().__init__("Initializing EFI protocol mappings...", True)
            self.bv = bv

        def run(self):
            if not init_protocol_mapping():
                return

            init_guid_mapping()

            import_types_from_headers(self.bv)

            if "EFI_SYSTEM_TABLE" not in self.bv.types:
                log_alert("This binary is not using the EFI platform. Use Open with Options when loading the binary to select the EFI platform.")
                return

            self.bv.begin_undo_actions()
            try:
                retype_entry_function(self.bv)

                find_known_guids(self.bv)

                self.progress = "Propagating EFI system table pointers..."
                if not propagate_system_table_pointer(self.bv, self):
                    return

                self.progress = "Defining types for uses of HandleProtocol..."
                if not define_handle_protocol_types(self.bv, self):
                    return

                self.progress = "Defining types for uses of OpenProtocol..."
                if not define_open_protocol_types(self.bv, self):
                    return

                self.progress = "Defining types for uses of LocateProtocol..."
                if not define_locate_protocol_types(self.bv, self):
                    return
            finally:
                self.bv.commit_undo_actions()

    Task(bv).start()

PluginCommand.register("Resolve EFI Protocols", "Automatically resolve usage of EFI protocols", resolve_efi)
