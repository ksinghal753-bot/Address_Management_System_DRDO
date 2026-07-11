import os

file_path = r"c:\Users\KANIKA SINGHAL\OneDrive\Desktop\New folder\CANTEEN_MANAGEMENT_SYSTEM\ADRDE_DRDO\ADRDE_ADDRESS\ui\user_dashboard.py"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

old_menu = """        menu_items = [
            ("🔍", "Search Address / पता खोजें", "Search for existing address records", self._open_view, COLORS["primary"]),
            ("🖨️", "Print Address / पता प्रिंट करें", "Print address labels and lists", self._open_view, COLORS["primary"]),
            ("👁️", "View Address / पता देखें", "View all address records", self._open_view, COLORS["primary"]),
            ("🚪", LABELS["logout"], "Logout from the system", self._do_logout, COLORS["error"]),
        ]"""

new_menu = """        menu_items = [
            ("🔍", "Search Address / पता खोजें", "Search for existing address records", self._open_search, COLORS["primary"]),
            ("🖨️", "Print Address / पता प्रिंट करें", "Print address labels and lists", self._open_view, COLORS["primary"]),
            ("👁️", "View Address / पता देखें", "View all address records", self._open_view, COLORS["primary"]),
            ("🚪", LABELS["logout"], "Logout from the system", self._do_logout, COLORS["error"]),
        ]"""

content = content.replace(old_menu, new_menu)

old_open_view = """    def _open_view(self):
        from ui.address_view import AddressView
        view = AddressView(role="user")
        view.go_back.connect(self._go_to_previous_screen)
        self._push_screen(view)"""

new_open_view = """    def _open_search(self):
        from ui.address_view import AddressView
        view = AddressView(role="user", mode="search")
        view.go_back.connect(self._go_to_previous_screen)
        self._push_screen(view)

    def _open_view(self):
        from ui.address_view import AddressView
        view = AddressView(role="user", mode="view")
        view.go_back.connect(self._go_to_previous_screen)
        self._push_screen(view)"""

content = content.replace(old_open_view, new_open_view)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
