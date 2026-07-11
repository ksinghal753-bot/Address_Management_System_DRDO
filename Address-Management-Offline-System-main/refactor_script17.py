import os

# 1. Update address_view.py
file_path_view = r"c:\Users\KANIKA SINGHAL\OneDrive\Desktop\New folder\CANTEEN_MANAGEMENT_SYSTEM\ADRDE_DRDO\ADRDE_ADDRESS\ui\address_view.py"

with open(file_path_view, "r", encoding="utf-8") as f:
    content_view = f.read()

# Replace the layout of ReferenceLabelPreviewDialog
# We need to change the button placement and remove the duplicate "To"
old_dialog = """class ReferenceLabelPreviewDialog(QDialog):
    def __init__(self, parent, records):
        super().__init__(parent)
        self.records = records
        self.print_mode = "both"
        self.setWindowTitle("Preview Reference Label(s) / संदर्भ लेबल पूर्वावलोकन")
        self.setMinimumSize(500, 450)
        
        layout = QVBoxLayout(self)
        
        # Top Print Buttons
        top_btn_layout = QHBoxLayout()
        
        btn_style = "QPushButton { background-color: #7A1212; color: white; border-radius: 4px; padding: 6px 12px; font-weight: bold; } QPushButton:hover { background-color: #5C0D0D; }"
        
        self.btn_print_left = QPushButton("🖨 Print Left")
        self.btn_print_left.setStyleSheet(btn_style)
        self.btn_print_left.clicked.connect(self._do_print_left)
        
        self.btn_print_right = QPushButton("🖨 Print Right")
        self.btn_print_right.setStyleSheet(btn_style)
        self.btn_print_right.clicked.connect(self._do_print_right)
        
        self.btn_print_both = QPushButton("🖨 Print Both")
        self.btn_print_both.setStyleSheet(btn_style)
        self.btn_print_both.clicked.connect(self._do_print_both)
        
        top_btn_layout.addWidget(self.btn_print_left)
        top_btn_layout.addWidget(self.btn_print_right)
        top_btn_layout.addStretch(1)
        top_btn_layout.addWidget(self.btn_print_both)
        
        layout.addLayout(top_btn_layout)
        
        # Info Label
        info = QLabel(f"Previewing {len(records)} label(s). NO: and Date: auto-populated from record data.")
        info.setStyleSheet("color: #444; font-size: 13px; font-weight: bold; margin-bottom: 5px; margin-top: 10px;")
        layout.addWidget(info)
        
        # Preview Text Area
        self.preview_area = QTextEdit()
        self.preview_area.setReadOnly(True)
        self.preview_area.setStyleSheet("background-color: #FAFAFA; border: 1px solid #CCC; font-size: 14px; padding: 10px;")
        
        html = "<html><body style='font-family: sans-serif;'>"
        for rec in records:
            html += "<table width='100%' style='border: 1px dashed #888; margin-bottom: 15px; border-collapse: collapse;'>"
            html += "<tr>"
            
            from modules.print_module import format_ref_no
            ref_no = format_ref_no(rec.get("para_no", ""), rec.get("date_entry", ""))
            ref_parts = ref_no.split("\\n")
            no_line = ref_parts[0]
            date_line = ref_parts[1] if len(ref_parts) > 1 else ""
            
            # Left side (50%)
            html += "<td width='50%' style='padding: 15px; vertical-align: top; border-right: 1px solid #333;'>"
            html += f"<strong>{no_line}</strong><br>"
            html += f"<strong>{date_line}</strong>"
            html += "</td>"
            
            # Right side (50%)
            html += "<td width='50%' style='padding: 15px; vertical-align: top;'>"
            html += "<strong>TO,</strong><br>"
            
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
            
            html += "<br>".join(right_lines)
            html += "</td>"
            
            html += "</tr></table><br>"
            
        html += "</body></html>"
            
        self.preview_area.setHtml(html)
        layout.addWidget(self.preview_area, stretch=1)
        
        # Bottom Buttons
        btn_layout = QHBoxLayout()
        btn_layout.addStretch(1)
        
        self.btn_cancel = QPushButton("Cancel")
        self.btn_cancel.clicked.connect(self.reject)
        
        btn_layout.addWidget(self.btn_cancel)
        layout.addLayout(btn_layout)

    def _do_print_left(self):
        self.print_mode = "left"
        self.accept()
        
    def _do_print_right(self):
        self.print_mode = "right"
        self.accept()
        
    def _do_print_both(self):
        self.print_mode = "both"
        self.accept()"""

new_dialog = """class ReferenceLabelPreviewDialog(QDialog):
    def __init__(self, parent, records):
        super().__init__(parent)
        self.records = records
        self.print_mode = "both"
        self.setWindowTitle("Preview Reference Label(s) / संदर्भ लेबल पूर्वावलोकन")
        self.setMinimumSize(500, 450)
        
        layout = QVBoxLayout(self)
        
        btn_style = "QPushButton { background-color: #7A1212; color: white; border-radius: 4px; padding: 6px 12px; font-weight: bold; } QPushButton:hover { background-color: #5C0D0D; }"
        
        # Info Label
        info = QLabel(f"Previewing {len(records)} label(s). NO: and Date: auto-populated from record data.")
        info.setStyleSheet("color: #444; font-size: 13px; font-weight: bold; margin-bottom: 5px; margin-top: 5px;")
        layout.addWidget(info)
        
        # Top Print Buttons (Left & Right)
        top_btn_layout = QHBoxLayout()
        
        self.btn_print_left = QPushButton("🖨 Print Left")
        self.btn_print_left.setStyleSheet(btn_style)
        self.btn_print_left.clicked.connect(self._do_print_left)
        
        self.btn_print_right = QPushButton("🖨 Print Right")
        self.btn_print_right.setStyleSheet(btn_style)
        self.btn_print_right.clicked.connect(self._do_print_right)
        
        # Add buttons with stretches so Left is on the left half, Right is on the right half
        top_btn_layout.addStretch(1)
        top_btn_layout.addWidget(self.btn_print_left)
        top_btn_layout.addStretch(2)
        top_btn_layout.addWidget(self.btn_print_right)
        top_btn_layout.addStretch(1)
        
        layout.addLayout(top_btn_layout)
        
        # Preview Text Area
        self.preview_area = QTextEdit()
        self.preview_area.setReadOnly(True)
        self.preview_area.setStyleSheet("background-color: #FAFAFA; border: 1px solid #CCC; font-size: 14px; padding: 10px;")
        
        html = "<html><body style='font-family: sans-serif;'>"
        for rec in records:
            html += "<table width='100%' style='border: 1px dashed #888; margin-bottom: 15px; border-collapse: collapse;'>"
            html += "<tr>"
            
            from modules.print_module import format_ref_no
            ref_no = format_ref_no(rec.get("para_no", ""), rec.get("date_entry", ""))
            ref_parts = ref_no.split("\\n")
            no_line = ref_parts[0]
            date_line = ref_parts[1] if len(ref_parts) > 1 else ""
            
            # Left side (50%)
            html += "<td width='50%' style='padding: 15px; vertical-align: top; border-right: 1px solid #333;'>"
            html += f"<strong>{no_line}</strong><br>"
            html += f"<strong>{date_line}</strong>"
            html += "</td>"
            
            # Right side (50%)
            html += "<td width='50%' style='padding: 15px; vertical-align: top;'>"
            html += "<strong>TO,</strong><br>"
            
            right_lines = []
            
            # Skip appending "To" if it exists to avoid duplication
            to_field = rec.get("to_field", "").strip()
            if to_field and to_field.lower() != "to":
                right_lines.append(to_field)
                
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
            
            html += "<br>".join(right_lines)
            html += "</td>"
            
            html += "</tr></table><br>"
            
        html += "</body></html>"
            
        self.preview_area.setHtml(html)
        layout.addWidget(self.preview_area, stretch=1)
        
        # Bottom Buttons (Cancel & Print Both)
        btn_layout = QHBoxLayout()
        btn_layout.addStretch(1)
        
        self.btn_cancel = QPushButton("Cancel")
        self.btn_cancel.clicked.connect(self.reject)
        
        self.btn_print_both = QPushButton("🖨 Print Both")
        self.btn_print_both.setStyleSheet(btn_style)
        self.btn_print_both.clicked.connect(self._do_print_both)
        
        btn_layout.addWidget(self.btn_cancel)
        btn_layout.addWidget(self.btn_print_both)
        layout.addLayout(btn_layout)

    def _do_print_left(self):
        self.print_mode = "left"
        self.accept()
        
    def _do_print_right(self):
        self.print_mode = "right"
        self.accept()
        
    def _do_print_both(self):
        self.print_mode = "both"
        self.accept()"""

content_view = content_view.replace(old_dialog, new_dialog)

with open(file_path_view, "w", encoding="utf-8") as f:
    f.write(content_view)


# 2. Update print_module.py
file_path_print = r"c:\Users\KANIKA SINGHAL\OneDrive\Desktop\New folder\CANTEEN_MANAGEMENT_SYSTEM\ADRDE_DRDO\ADRDE_ADDRESS\modules\print_module.py"

with open(file_path_print, "r", encoding="utf-8") as f:
    content_print = f.read()

old_print_logic = """        for rec in records:
            ref_no = format_ref_no(rec.get("para_no", ""), rec.get("date_entry", ""))
            ref_parts = ref_no.split("\\n")
            no_line = ref_parts[0]
            date_line = ref_parts[1] if len(ref_parts) > 1 else ""
            
            if print_mode in ("both", "left"):
                left_content = f"{no_line}<br/>{date_line}"
            else:
                left_content = ""
                
            right_lines = ["TO,"]
            if rec.get("to_field"):
                right_lines.append(rec["to_field"])
            if rec.get("designation"):
                right_lines.append(rec["designation"])"""

new_print_logic = """        for rec in records:
            ref_no = format_ref_no(rec.get("para_no", ""), rec.get("date_entry", ""))
            ref_parts = ref_no.split("\\n")
            no_line = ref_parts[0]
            date_line = ref_parts[1] if len(ref_parts) > 1 else ""
            
            if print_mode in ("both", "left"):
                left_content = f"{no_line}<br/>{date_line}"
            else:
                left_content = ""
                
            right_lines = ["TO,"]
            
            to_field = rec.get("to_field", "").strip()
            if to_field and to_field.lower() != "to":
                right_lines.append(to_field)
                
            if rec.get("designation"):
                right_lines.append(rec["designation"])"""

content_print = content_print.replace(old_print_logic, new_print_logic)

with open(file_path_print, "w", encoding="utf-8") as f:
    f.write(content_print)
