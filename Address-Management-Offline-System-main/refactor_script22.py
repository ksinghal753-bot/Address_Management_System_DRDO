import os

file_path = r"c:\Users\KANIKA SINGHAL\OneDrive\Desktop\New folder\CANTEEN_MANAGEMENT_SYSTEM\ADRDE_DRDO\ADRDE_ADDRESS\ui\address_view.py"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Remove the old action grid code
old_code_start = """        # Action Grid for compactness
        top_actions = QHBoxLayout()
        top_actions.setSpacing(6)

        self.clear_sel_btn = QPushButton("🧹 Clear Selection")
        self.clear_sel_btn.setObjectName("secondaryButton")
        self.clear_sel_btn.clicked.connect(self._clear_selection)
        top_actions.addWidget(self.clear_sel_btn)

        self.print_btn = QPushButton("🖨️ Print")
        self.print_btn.setObjectName("primaryPrintButton")
        self.print_btn.clicked.connect(self._show_print_dialog)
        top_actions.addWidget(self.print_btn)

        search_vbox.addLayout(top_actions)
        search_vbox.addWidget(HLine())"""

new_code_start = """        # Reverting to the 1st screenshot layout (Grid of 6 buttons)
        grid = QGridLayout()
        grid.setSpacing(6)
        
        self.add_btn = QPushButton("➕ Add Address")
        self.add_btn.setStyleSheet("background-color: #1f6b2e; color: white; border-radius: 6px; padding: 8px; font-weight: bold;")
        self.add_btn.clicked.connect(self.add_new.emit)
        
        self.edit_btn = QPushButton("✏️ Edit Address")
        self.edit_btn.setObjectName("secondaryButton")
        self.edit_btn.clicked.connect(self._edit_selected)
        self.edit_btn.setEnabled(False)

        self.del_btn = QPushButton("🗑️ Delete")
        self.del_btn.setObjectName("secondaryButton")
        self.del_btn.clicked.connect(self._delete_selected)
        self.del_btn.setEnabled(False)

        self.view_btn = QPushButton("👁️ View")
        self.view_btn.setObjectName("secondaryButton")
        self.view_btn.clicked.connect(self._view_selected)
        self.view_btn.setEnabled(False)

        self.clear_sel_btn = QPushButton("🧹 Clear")
        self.clear_sel_btn.setObjectName("secondaryButton")
        self.clear_sel_btn.clicked.connect(self._clear_search)
        self.clear_sel_btn.clicked.connect(self._clear_selection)

        self.print_btn = QPushButton("🖨️ Print")
        self.print_btn.setStyleSheet("background-color: #8B0000; color: white; border-radius: 6px; padding: 8px; font-weight: bold;")
        # Note: using the same action as the old print_btn. If _show_print_dialog doesn't exist, we fallback.
        if hasattr(self, '_show_print_dialog'):
            self.print_btn.clicked.connect(self._show_print_dialog)
        else:
            self.print_btn.clicked.connect(self._print_single)

        grid.addWidget(self.add_btn, 0, 0)
        grid.addWidget(self.edit_btn, 0, 1)
        grid.addWidget(self.del_btn, 0, 2)
        grid.addWidget(self.view_btn, 1, 0)
        grid.addWidget(self.clear_sel_btn, 1, 1)
        grid.addWidget(self.print_btn, 1, 2)

        search_vbox.addLayout(grid)
        search_vbox.addWidget(HLine())"""

content = content.replace(old_code_start, new_code_start)

# Also I need to remove the Edit Selected and Delete Selected from the bottom row that I added in the previous script!
# They look weird if they are at the top AND bottom.
old_bottom_code = """        self.edit_btn = QPushButton("✏️ Edit Selected / चयनित संपादित करें")
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
            bottom_action_row.addWidget(self.btn_print_list_corner)"""

new_bottom_code = """        self.btn_print_label_corner = QPushButton("🏷️ Print Reference Label(s) / संदर्भ लेबल (केवल NO:- Date)")
        self.btn_print_label_corner.setCursor(Qt.PointingHandCursor)
        self.btn_print_label_corner.setStyleSheet(btn_action_style)
        self.btn_print_label_corner.clicked.connect(lambda: self._enter_selection_mode("label"))
        
        self.btn_print_list_corner = QPushButton("📄 Print List / पता सूची प्रिंट करें")
        self.btn_print_list_corner.setCursor(Qt.PointingHandCursor)
        self.btn_print_list_corner.setStyleSheet(btn_action_style)
        self.btn_print_list_corner.clicked.connect(lambda: self._enter_selection_mode("list"))
        
        bottom_action_row.addWidget(self.btn_print_label_corner)
        bottom_action_row.addWidget(self.btn_print_list_corner)"""

content = content.replace(old_bottom_code, new_bottom_code)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
