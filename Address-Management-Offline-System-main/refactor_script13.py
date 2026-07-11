import os

file_path = r"c:\Users\KANIKA SINGHAL\OneDrive\Desktop\New folder\CANTEEN_MANAGEMENT_SYSTEM\ADRDE_DRDO\ADRDE_ADDRESS\ui\address_view.py"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Add ReferenceLabelPreviewDialog class before AddressView class

dialog_code = """class ReferenceLabelPreviewDialog(QDialog):
    def __init__(self, parent, records):
        super().__init__(parent)
        self.records = records
        self.setWindowTitle("Preview Reference Label(s) / संदर्भ लेबल पूर्वावलोकन")
        self.setMinimumSize(600, 700)
        
        layout = QVBoxLayout(self)
        
        # Info Label
        info = QLabel(f"Previewing {len(records)} label(s). NO: and Date: will be left blank for handwriting.")
        info.setStyleSheet("color: #444; font-size: 13px; font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(info)
        
        # Preview Text Area
        self.preview_area = QTextEdit()
        self.preview_area.setReadOnly(True)
        self.preview_area.setStyleSheet("background-color: #FAFAFA; border: 1px solid #CCC; font-family: monospace; font-size: 14px; padding: 10px;")
        
        preview_text = ""
        for rec in records:
            preview_text += "-" * 60 + "\\n"
            left = "NO: -            |  TO,\\nDate: -          |  "
            
            right_lines = []
            if rec.get("to_field"): right_lines.append(rec["to_field"])
            if rec.get("designation"): right_lines.append(rec["designation"])
            if rec.get("office_name"): right_lines.append(rec["office_name"])
            if rec.get("addr_line1"): right_lines.append(rec["addr_line1"])
            if rec.get("addr_line2"): right_lines.append(rec["addr_line2"])
            
            city_state_pin = ", ".join(filter(None, [rec.get("city", ""), rec.get("state", "")]))
            if rec.get("pin_code"):
                if city_state_pin:
                    city_state_pin += " - " + rec["pin_code"]
                else:
                    city_state_pin = "PIN: " + rec["pin_code"]
            if city_state_pin: right_lines.append(city_state_pin)
            
            for i, line in enumerate(right_lines):
                if i == 0:
                    preview_text += left + line + "\\n"
                elif i == 1:
                    preview_text += "                 |  " + line + "\\n"
                else:
                    preview_text += "                 |  " + line + "\\n"
            
            preview_text += "-" * 60 + "\\n\\n"
            
        self.preview_area.setPlainText(preview_text)
        layout.addWidget(self.preview_area, stretch=1)
        
        # Buttons
        btn_layout = QHBoxLayout()
        btn_layout.addStretch(1)
        
        self.btn_cancel = QPushButton("Cancel")
        self.btn_cancel.clicked.connect(self.reject)
        
        self.btn_print = QPushButton("🖨 Save to PDF")
        self.btn_print.setStyleSheet("QPushButton { background-color: #7A1212; color: white; border-radius: 4px; padding: 8px 16px; font-weight: bold; } QPushButton:hover { background-color: #5C0D0D; }")
        self.btn_print.clicked.connect(self.accept)
        
        btn_layout.addWidget(self.btn_cancel)
        btn_layout.addWidget(self.btn_print)
        layout.addLayout(btn_layout)

class AddressView(QWidget):"""

content = content.replace("class AddressView(QWidget):", dialog_code)

# 2. Update _print_selected_list to show dialog

old_print_logic = """        if getattr(self, "current_selection_mode", "list") == "label":
            path = self._get_print_path("ReferenceLabels")
            if not path:
                return
            from modules.print_module import generate_reference_labels_pdf
            ok, result = generate_reference_labels_pdf(checked, path)
            if ok:
                show_info(self, "PDF Generated / PDF बना", LABELS["print_success"])
                open_pdf(path)
                self._cancel_selection_mode()
            else:
                show_error(self, "Print Error / प्रिंट त्रुटि", result)
            return"""

new_print_logic = """        if getattr(self, "current_selection_mode", "list") == "label":
            # Show preview dialog first
            dialog = ReferenceLabelPreviewDialog(self, checked)
            if dialog.exec() == QDialog.Accepted:
                path = self._get_print_path("ReferenceLabels")
                if not path:
                    return
                from modules.print_module import generate_reference_labels_pdf
                ok, result = generate_reference_labels_pdf(checked, path)
                if ok:
                    show_info(self, "PDF Generated / PDF बना", LABELS["print_success"])
                    open_pdf(path)
                    self._cancel_selection_mode()
                else:
                    show_error(self, "Print Error / प्रिंट त्रुटि", result)
            return"""

content = content.replace(old_print_logic, new_print_logic)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
