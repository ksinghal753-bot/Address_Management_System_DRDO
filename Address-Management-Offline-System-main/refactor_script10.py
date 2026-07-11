import os

file_path = r"c:\Users\KANIKA SINGHAL\OneDrive\Desktop\New folder\CANTEEN_MANAGEMENT_SYSTEM\ADRDE_DRDO\ADRDE_ADDRESS\ui\address_view.py"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Add selection controls right above the table in bottom_vbox
table_setup_code = """        # Address table
        self.table = QTableWidget()"""

selection_controls_code = """        # Selection Controls (Hidden by default)
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
        bottom_vbox.addWidget(self.selection_controls_widget)

        # Address table
        self.table = QTableWidget()"""

content = content.replace(table_setup_code, selection_controls_code)

# 2. Change btn_print_list_corner to call _enter_selection_mode
content = content.replace("self.btn_print_list_corner.clicked.connect(self._print_list)", "self.btn_print_list_corner.clicked.connect(self._enter_selection_mode)")

# 3. Add the new methods before _print_list
new_methods = """    def _enter_selection_mode(self):
        self.btn_print_list_corner.setVisible(False)
        self.selection_controls_widget.setVisible(True)

    def _cancel_selection_mode(self):
        self.selection_controls_widget.setVisible(False)
        self.btn_print_list_corner.setVisible(True)
        self._deselect_all_records()

    def _select_all_records(self):
        self.table.blockSignals(True)
        for row in range(self.table.rowCount()):
            item = self.table.item(row, 1)
            if item:
                item.setCheckState(Qt.Checked)
        self.table.blockSignals(False)
        self._set_action_btns()

    def _deselect_all_records(self):
        self.table.blockSignals(True)
        for row in range(self.table.rowCount()):
            item = self.table.item(row, 1)
            if item:
                item.setCheckState(Qt.Unchecked)
        self.table.blockSignals(False)
        self._set_action_btns()

    def _print_selected_list(self):
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
            show_error(self, "Print Error / प्रिंट त्रुटि", result)

    def _print_list(self):"""

content = content.replace("    def _print_list(self):", new_methods)

# Wait, the PrintOptionsDialog also has a Print List button. We should change its connection.
content = content.replace("self.btn_list.clicked.connect(lambda: self.done_with_option(\"list\"))", "self.btn_list.clicked.connect(lambda: self.done_with_option(\"list\"))")

# Wait, in _show_print_dialog:
# elif opt == "list":
#     self._print_list()
# We should change this to self._enter_selection_mode()
content = content.replace("elif opt == \"list\":\n                self._print_list()", "elif opt == \"list\":\n                self._enter_selection_mode()")


with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
