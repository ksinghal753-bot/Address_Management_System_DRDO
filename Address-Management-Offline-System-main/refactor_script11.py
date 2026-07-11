import os

file_path = r"c:\Users\KANIKA SINGHAL\OneDrive\Desktop\New folder\CANTEEN_MANAGEMENT_SYSTEM\ADRDE_DRDO\ADRDE_ADDRESS\ui\address_view.py"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Replace selection controls widget block
old_block = """        # Selection Controls (Hidden by default)
        self.selection_controls_widget = QWidget()
        selection_layout = QHBoxLayout(self.selection_controls_widget)
        selection_layout.setContentsMargins(0, 0, 0, 0)
        
        btn_style = "QPushButton { background-color: #FAFAFA; border: 1px solid #CCC; border-radius: 4px; padding: 6px 12px; font-weight: bold; } QPushButton:hover { background-color: #EEE; }"
        primary_btn_style = "QPushButton { background-color: #7A1212; color: white; border: 1px solid #7A1212; border-radius: 4px; padding: 6px 12px; font-weight: bold; } QPushButton:hover { background-color: #5C0D0D; }"
        
        self.btn_select_all = QPushButton("☑ Select All")
        self.btn_select_all.setStyleSheet(btn_style)
        self.btn_select_all.clicked.connect(self._select_all_records)
        
        self.btn_deselect_all = QPushButton("☐ Deselect All")
        self.btn_deselect_all.setStyleSheet(btn_style)
        self.btn_deselect_all.clicked.connect(self._deselect_all_records)
        
        self.btn_cancel_selection = QPushButton("🔄 Cancel Selection")
        self.btn_cancel_selection.setStyleSheet(btn_style)
        self.btn_cancel_selection.clicked.connect(self._cancel_selection_mode)
        
        self.btn_print_selected = QPushButton("🖨 Print Selected")
        self.btn_print_selected.setStyleSheet(primary_btn_style)
        self.btn_print_selected.clicked.connect(self._print_selected_list)
        
        selection_layout.addWidget(self.btn_select_all)
        selection_layout.addWidget(self.btn_deselect_all)
        selection_layout.addStretch(1)
        selection_layout.addWidget(self.btn_cancel_selection)
        selection_layout.addWidget(self.btn_print_selected)
        
        self.selection_controls_widget.setVisible(False)
        bottom_vbox.addWidget(self.selection_controls_widget)"""

new_block = """        # Selection Controls (Hidden by default)
        self.selection_controls_widget = QWidget()
        self.selection_controls_widget.setStyleSheet(f"background-color: {COLORS['surface']}; border: 1px solid #ddd; border-radius: 6px;")
        selection_layout = QVBoxLayout(self.selection_controls_widget)
        selection_layout.setContentsMargins(8, 8, 8, 8)
        selection_layout.setSpacing(6)
        
        # Row 1: Action Buttons
        action_row = QHBoxLayout()
        btn_style = "QPushButton { background-color: #FAFAFA; border: 1px solid #CCC; border-radius: 4px; padding: 6px 12px; font-weight: bold; } QPushButton:hover { background-color: #EEE; }"
        primary_btn_style = "QPushButton { background-color: #7A1212; color: white; border: 1px solid #7A1212; border-radius: 4px; padding: 6px 12px; font-weight: bold; } QPushButton:hover { background-color: #5C0D0D; }"
        
        self.btn_select_all = QPushButton("☑ Select All Rows")
        self.btn_select_all.setStyleSheet(btn_style)
        self.btn_select_all.clicked.connect(self._select_all_records)
        
        self.btn_deselect_all = QPushButton("☐ Deselect All Rows")
        self.btn_deselect_all.setStyleSheet(btn_style)
        self.btn_deselect_all.clicked.connect(self._deselect_all_records)
        
        self.btn_cancel_selection = QPushButton("🔄 Cancel Selection")
        self.btn_cancel_selection.setStyleSheet(btn_style)
        self.btn_cancel_selection.clicked.connect(self._cancel_selection_mode)
        
        self.btn_print_selected = QPushButton("🖨 Print Selected")
        self.btn_print_selected.setStyleSheet(primary_btn_style)
        self.btn_print_selected.clicked.connect(self._print_selected_list)
        
        lbl_info = QLabel("<b>1.</b> Select rows from table below.")
        lbl_info.setStyleSheet("color: #444;")
        
        action_row.addWidget(lbl_info)
        action_row.addStretch(1)
        action_row.addWidget(self.btn_select_all)
        action_row.addWidget(self.btn_deselect_all)
        action_row.addWidget(self.btn_cancel_selection)
        action_row.addWidget(self.btn_print_selected)
        selection_layout.addLayout(action_row)
        
        selection_layout.addWidget(HLine())
        
        # Row 2: Field Checkboxes
        fields_row = QHBoxLayout()
        lbl_fields = QLabel("<b>2.</b> Select fields to print:")
        lbl_fields.setStyleSheet("color: #444;")
        fields_row.addWidget(lbl_fields)
        
        self.field_checkboxes = {}
        self.field_definitions = [
            ("dept_name", "Dept"),
            ("to_field", "To"),
            ("designation", "Designation"),
            ("office_name", "Office"),
            ("address", "Address"),
            ("city_state", "City/State"),
            ("pin_code", "PIN"),
            ("email", "Email"),
            ("contact_no", "Contact"),
            ("fax", "Fax"),
            ("para_no", "PARA"),
            ("date_entry", "Date"),
            ("delivery_type", "By S/P")
        ]
        
        for key, label in self.field_definitions:
            cb = QCheckBox(label)
            cb.setChecked(True)
            cb.setStyleSheet("padding-right: 8px;")
            self.field_checkboxes[key] = cb
            fields_row.addWidget(cb)
            
        fields_row.addStretch(1)
        selection_layout.addLayout(fields_row)
        
        self.selection_controls_widget.setVisible(False)
        bottom_vbox.addWidget(self.selection_controls_widget)"""

if old_block in content:
    content = content.replace(old_block, new_block)
else:
    print("Could not find old_block")

# Modify _print_selected_list to use these checkboxes directly instead of showing a dialog
old_print_method = """    def _print_selected_list(self):
        checked = self._get_checked_records()
        if not checked:
            show_warning(self, "No Selection", "Please select at least one address to print.")
            return
            
        dlg = ColumnSelectionDialog(self)
        if dlg.exec() != QDialog.Accepted:
            return
            
        selected_cols = dlg.get_selected_columns()
        if not selected_cols:
            show_warning(self, "No Columns Selected", "Please select at least one column to print.")
            return
            
        path = self._get_print_path("AddressList")
        if not path:
            return
            
        from modules.print_module import generate_address_list_pdf
        ok, result = generate_address_list_pdf(checked, path, selected_cols)
        if ok:
            show_info(self, "PDF Generated / PDF बना", LABELS["print_success"])
            open_pdf(path)
            self._cancel_selection_mode()
        else:
            show_error(self, "Print Error / प्रिंट त्रुटि", result)"""

new_print_method = """    def _print_selected_list(self):
        checked = self._get_checked_records()
        if not checked:
            show_warning(self, "No Selection", "Please select at least one address to print.")
            return
            
        selected_cols = [key for key, _ in self.field_definitions if self.field_checkboxes[key].isChecked()]
        if not selected_cols:
            show_warning(self, "No Columns Selected", "Please select at least one column to print.")
            return
            
        path = self._get_print_path("AddressList")
        if not path:
            return
            
        from modules.print_module import generate_address_list_pdf
        ok, result = generate_address_list_pdf(checked, path, selected_cols)
        if ok:
            show_info(self, "PDF Generated / PDF बना", LABELS["print_success"])
            open_pdf(path)
            self._cancel_selection_mode()
        else:
            show_error(self, "Print Error / प्रिंट त्रुटि", result)"""

if old_print_method in content:
    content = content.replace(old_print_method, new_print_method)
else:
    print("Could not find _print_selected_list")

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
