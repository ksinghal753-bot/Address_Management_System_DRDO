import os

file_path = r"c:\Users\KANIKA SINGHAL\OneDrive\Desktop\New folder\CANTEEN_MANAGEMENT_SYSTEM\ADRDE_DRDO\ADRDE_ADDRESS\ui\address_view.py"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

dialog_code = """
class ColumnSelectionDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Select Columns / कॉलम चुनें")
        self.resize(320, 450)
        self.setStyleSheet(f"background-color: {COLORS['surface']};")
        
        layout = QVBoxLayout(self)
        
        title = QLabel("Select Columns to Print")
        title.setStyleSheet(f"font-size: 14px; font-weight: bold; color: {COLORS['primary']};")
        layout.addWidget(title)
        
        self.checkboxes = {}
        
        self.columns = [
            ("dept_name", "Dept / विभाग"),
            ("to_field", "To / सेवा में"),
            ("designation", "Designation / पदनाम"),
            ("office_name", "Office Name / कार्यालय"),
            ("address", "Address / पता"),
            ("city_state", "City, State / शहर, राज्य"),
            ("pin_code", "PIN / पिन"),
            ("email", "Email / ईमेल"),
            ("contact_no", "Contact / संपर्क"),
            ("fax", "Fax / फैक्स"),
            ("para_no", "PARA / पैरा"),
            ("date_entry", "Date / दिनांक"),
            ("delivery_type", "By S/P / डाक")
        ]
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("border: 1px solid #ddd; background-color: #fff;")
        
        inner_widget = QWidget()
        inner_layout = QVBoxLayout(inner_widget)
        
        for key, label in self.columns:
            cb = QCheckBox(label)
            cb.setChecked(True)
            cb.setStyleSheet("font-size: 12px; padding: 2px;")
            self.checkboxes[key] = cb
            inner_layout.addWidget(cb)
            
        inner_layout.addStretch(1)
        scroll.setWidget(inner_widget)
        layout.addWidget(scroll, stretch=1)
        
        btn_layout = QHBoxLayout()
        self.btn_ok = QPushButton("Print / प्रिंट")
        self.btn_ok.setStyleSheet("background-color: #7A1212; color: #fff; font-weight: bold; padding: 6px; border-radius: 4px;")
        self.btn_ok.clicked.connect(self.accept)
        
        self.btn_cancel = QPushButton("Cancel / रद्द करें")
        self.btn_cancel.setStyleSheet("background-color: #f0f0f0; border: 1px solid #ccc; padding: 6px; border-radius: 4px;")
        self.btn_cancel.clicked.connect(self.reject)
        
        btn_layout.addWidget(self.btn_ok)
        btn_layout.addWidget(self.btn_cancel)
        layout.addLayout(btn_layout)
        
    def get_selected_columns(self):
        return [key for key, label in self.columns if self.checkboxes[key].isChecked()]
"""

if "class PrintOptionsDialog(QDialog):" in content:
    content = content.replace("class PrintOptionsDialog(QDialog):", dialog_code + "\nclass PrintOptionsDialog(QDialog):")
else:
    print("Could not find PrintOptionsDialog")

old_print_list = """    def _print_list(self):
        checked = self._get_checked_records()
        records = checked if checked else (
            [self._selected_record] if self._selected_record else self._records
        )
        if not records:
            show_info(self, "No Records", LABELS["no_records"])
            return
        path = self._get_print_path("AddressList")
        if not path:
            return
        # Import dynamically or assure it's imported at top
        from modules.print_module import generate_address_list_pdf
        ok, result = generate_address_list_pdf(records, path)
        if ok:
            show_info(self, "PDF Generated / PDF बना", LABELS["print_success"])
            open_pdf(path)
        else:
            show_error(self, "Print Error / प्रिंट त्रुटि", result)"""

new_print_list = """    def _print_list(self):
        checked = self._get_checked_records()
        records = checked if checked else (
            [self._selected_record] if self._selected_record else self._records
        )
        if not records:
            show_info(self, "No Records", LABELS["no_records"])
            return
            
        dlg = ColumnSelectionDialog(self)
        if dlg.exec() != QDialog.Accepted:
            return
            
        selected_cols = dlg.get_selected_columns()
        if not selected_cols:
            show_warning(self, "No Columns Selected / कोई कॉलम नहीं चुना गया", "Please select at least one column to print.")
            return
            
        path = self._get_print_path("AddressList")
        if not path:
            return
            
        from modules.print_module import generate_address_list_pdf
        ok, result = generate_address_list_pdf(records, path, selected_cols)
        if ok:
            show_info(self, "PDF Generated / PDF बना", LABELS["print_success"])
            open_pdf(path)
        else:
            show_error(self, "Print Error / प्रिंट त्रुटि", result)"""

if old_print_list in content:
    content = content.replace(old_print_list, new_print_list)
else:
    print("Could not find _print_list")
    
with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
