import os

file_path = r"c:\Users\KANIKA SINGHAL\OneDrive\Desktop\New folder\CANTEEN_MANAGEMENT_SYSTEM\ADRDE_DRDO\ADRDE_ADDRESS\ui\admin_dashboard.py"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Replace menu_items
old_menu = """        menu_items = [
            ("➕", "Add Address / पता जोड़ें", "Add new address records", self._open_add, COLORS["success"]),
            ("🔍", "Search Address / पता खोजें", "Search for existing address records", self._open_view, COLORS["primary"]),
            ("✏️", "Edit Address / पता संपादित करें", "Edit existing address records", self._open_view, COLORS["primary"]),
            ("🗑️", "Delete Address / पता हटाएं", "Delete address records", self._open_view, COLORS["error"]),
            ("🖨️", "Print Address / पता प्रिंट करें", "Print address labels and lists", self._open_view, COLORS["primary"]),
            ("👁️", "View Address / पता देखें", "View all address records", self._open_view, COLORS["primary"]),
            ("🏢", LABELS["manage_depts"], "Add / Edit departments", self._open_depts, COLORS["primary_light"]),
            ("👥", LABELS["manage_users"], "Add / Edit user accounts", self._open_users, COLORS["primary_light"]),
        ]"""

new_menu = """        menu_items = [
            ("➕", "Add Address / पता जोड़ें", "Add new address records", self._open_add, COLORS["success"]),
            ("🔍", "Search Address / पता खोजें", "Search for existing address records", self._open_search, COLORS["primary"]),
            ("✏️", "Edit Address / पता संपादित करें", "Edit existing address records", self._open_edit_list, COLORS["primary"]),
            ("🗑️", "Delete Address / पता हटाएं", "Delete address records", self._open_delete, COLORS["error"]),
            ("🖨️", "Print Address / पता प्रिंट करें", "Print address labels and lists", self._open_view, COLORS["primary"]),
            ("👁️", "View Address / पता देखें", "View all address records", self._open_view, COLORS["primary"]),
            ("🏢", LABELS["manage_depts"], "Add / Edit departments", self._open_depts, COLORS["primary_light"]),
            ("👥", LABELS["manage_users"], "Add / Edit user accounts", self._open_users, COLORS["primary_light"]),
        ]"""

content = content.replace(old_menu, new_menu)

# Add the missing _open_* methods
old_open_view = """    def _open_view(self):
        from ui.address_view import AddressView
        view = AddressView(role="admin")
        view.go_back.connect(self._go_to_previous_screen)
        view.add_new.connect(self._open_add)
        view.edit_record.connect(self._open_edit)
        self._push_screen(view)"""

new_open_view = """    def _open_search(self):
        from ui.address_view import AddressView
        view = AddressView(role="admin", mode="search")
        view.go_back.connect(self._go_to_previous_screen)
        self._push_screen(view)

    def _open_edit_list(self):
        from ui.address_view import AddressView
        view = AddressView(role="admin", mode="edit")
        view.go_back.connect(self._go_to_previous_screen)
        view.edit_record.connect(self._open_edit)
        self._push_screen(view)

    def _open_delete(self):
        from ui.address_view import AddressView
        view = AddressView(role="admin", mode="delete")
        view.go_back.connect(self._go_to_previous_screen)
        self._push_screen(view)

    def _open_view(self):
        from ui.address_view import AddressView
        view = AddressView(role="admin", mode="view")
        view.go_back.connect(self._go_to_previous_screen)
        self._push_screen(view)"""

content = content.replace(old_open_view, new_open_view)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
