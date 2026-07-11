import os
import re

file_path = r"c:\Users\KANIKA SINGHAL\OneDrive\Desktop\New folder\CANTEEN_MANAGEMENT_SYSTEM\ADRDE_DRDO\ADRDE_ADDRESS\ui\address_view.py"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Add mode parameter to __init__
old_init = """    def __init__(self, role: str = "user", parent=None):
        super().__init__(parent)
        self.role = role
        self._records: list[dict] = []
        self._selected_record: dict | None = None
        self._build_ui()
        self._load_records()"""

new_init = """    def __init__(self, role: str = "user", mode: str = "view", parent=None):
        super().__init__(parent)
        self.role = role
        self.mode = mode
        self._records: list[dict] = []
        self._selected_record: dict | None = None
        self._build_ui()
        self._load_records()"""

content = content.replace(old_init, new_init)

# 2. Update Window Title based on Mode
old_title = """        title = QLabel("📋  Address Records / पता अभिलेख")"""
new_title = """        title_text = "📋  Address Records / पता अभिलेख"
        if self.mode == "search":
            title_text = "🔍  Search Address / पता खोजें"
        elif self.mode == "edit":
            title_text = "✏️  Edit Address / पता संपादित करें"
        elif self.mode == "delete":
            title_text = "🗑️  Delete Address / पता हटाएं"
            
        title = QLabel(title_text)"""

content = content.replace(old_title, new_title)

# 3. Add Edit/Delete buttons to the bottom action row and handle visibility
old_bottom_action = """        bottom_action_row = QHBoxLayout()
        bottom_action_row.addStretch(1)
        
        btn_action_style = (
            "QPushButton {"
            "  background-color: #7A1212;"
            "  color: #FFFFFF;"
            "  border: 1px solid #7A1212;"
            "  border-radius: 6px;"
            "  font-size: 13px;"
            "  font-weight: bold;"
            "  padding: 8px 16px;"
            "}"
            "QPushButton:hover {"
            "  background-color: #5C0D0D;"
            "}"
        )
        
        self.btn_print_label_corner = QPushButton("🏷️ Print Reference Label(s) / संदर्भ लेबल (केवल NO:- Date)")
        self.btn_print_label_corner.setCursor(Qt.PointingHandCursor)
        self.btn_print_label_corner.setStyleSheet(btn_action_style)
        self.btn_print_label_corner.clicked.connect(lambda: self._enter_selection_mode("label"))
        
        self.btn_print_list_corner = QPushButton("📄 Print List / पता सूची प्रिंट करें")
        self.btn_print_list_corner.setCursor(Qt.PointingHandCursor)
        self.btn_print_list_corner.setStyleSheet(btn_action_style)
        self.btn_print_list_corner.clicked.connect(lambda: self._enter_selection_mode("list"))
        
        bottom_action_row.addWidget(self.btn_print_label_corner)
        bottom_action_row.addWidget(self.btn_print_list_corner)

        bottom_vbox.addLayout(bottom_action_row)"""

new_bottom_action = """        bottom_action_row = QHBoxLayout()
        bottom_action_row.addStretch(1)
        
        btn_action_style = (
            "QPushButton {"
            "  background-color: #7A1212;"
            "  color: #FFFFFF;"
            "  border: 1px solid #7A1212;"
            "  border-radius: 6px;"
            "  font-size: 13px;"
            "  font-weight: bold;"
            "  padding: 8px 16px;"
            "}"
            "QPushButton:hover {"
            "  background-color: #5C0D0D;"
            "}"
        )

        self.edit_btn = QPushButton("✏️ Edit Selected / चयनित संपादित करें")
        self.edit_btn.setCursor(Qt.PointingHandCursor)
        self.edit_btn.setStyleSheet("background-color: #2563EB; color: white; border-radius: 6px; padding: 8px 16px; font-weight: bold;")
        self.edit_btn.clicked.connect(self._edit_selected)
        self.edit_btn.setEnabled(False)

        self.del_btn = QPushButton("🗑️ Delete Selected / चयनित हटाएं")
        self.del_btn.setCursor(Qt.PointingHandCursor)
        self.del_btn.setStyleSheet("background-color: #DC2626; color: white; border-radius: 6px; padding: 8px 16px; font-weight: bold;")
        self.del_btn.clicked.connect(self._delete_selected)
        self.del_btn.setEnabled(False)

        self.btn_print_label_corner = QPushButton("🏷️ Print Reference Label(s) / संदर्भ लेबल (केवल NO:- Date)")
        self.btn_print_label_corner.setCursor(Qt.PointingHandCursor)
        self.btn_print_label_corner.setStyleSheet(btn_action_style)
        self.btn_print_label_corner.clicked.connect(lambda: self._enter_selection_mode("label"))
        
        self.btn_print_list_corner = QPushButton("📄 Print List / पता सूची प्रिंट करें")
        self.btn_print_list_corner.setCursor(Qt.PointingHandCursor)
        self.btn_print_list_corner.setStyleSheet(btn_action_style)
        self.btn_print_list_corner.clicked.connect(lambda: self._enter_selection_mode("list"))
        
        # Add buttons conditionally based on mode
        if self.mode == "edit":
            bottom_action_row.addWidget(self.edit_btn)
        elif self.mode == "delete":
            bottom_action_row.addWidget(self.del_btn)
        elif self.mode == "view":
            bottom_action_row.addWidget(self.btn_print_label_corner)
            bottom_action_row.addWidget(self.btn_print_list_corner)
        
        bottom_vbox.addLayout(bottom_action_row)"""

content = content.replace(old_bottom_action, new_bottom_action)

# Update _set_action_btns so it doesn't crash if buttons don't exist
old_set_action_btns = """        if sel_count == 0:
            self.view_btn.setEnabled(False)
            self.preview_open_btn.setEnabled(False)
            if self.role == "admin":
                self.edit_btn.setEnabled(False)
                self.del_btn.setEnabled(False)
            return

        self.view_btn.setEnabled(True)
        self.preview_open_btn.setEnabled(sel_count == 1)
        if self.role == "admin":
            self.edit_btn.setEnabled(sel_count == 1)
            self.del_btn.setEnabled(sel_count >= 1)"""

new_set_action_btns = """        if sel_count == 0:
            if hasattr(self, 'view_btn'): self.view_btn.setEnabled(False)
            if hasattr(self, 'preview_open_btn'): self.preview_open_btn.setEnabled(False)
            if self.role == "admin":
                if hasattr(self, 'edit_btn'): self.edit_btn.setEnabled(False)
                if hasattr(self, 'del_btn'): self.del_btn.setEnabled(False)
            return

        if hasattr(self, 'view_btn'): self.view_btn.setEnabled(True)
        if hasattr(self, 'preview_open_btn'): self.preview_open_btn.setEnabled(sel_count == 1)
        if self.role == "admin":
            if hasattr(self, 'edit_btn'): self.edit_btn.setEnabled(sel_count == 1)
            if hasattr(self, 'del_btn'): self.del_btn.setEnabled(sel_count >= 1)"""

content = content.replace(old_set_action_btns, new_set_action_btns)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
