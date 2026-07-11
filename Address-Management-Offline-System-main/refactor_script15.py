import os

# 1. Update address_view.py
file_path_view = r"c:\Users\KANIKA SINGHAL\OneDrive\Desktop\New folder\CANTEEN_MANAGEMENT_SYSTEM\ADRDE_DRDO\ADRDE_ADDRESS\ui\address_view.py"

with open(file_path_view, "r", encoding="utf-8") as f:
    content_view = f.read()

# Replace the layout of ReferenceLabelPreviewDialog
old_dialog = """class ReferenceLabelPreviewDialog(QDialog):
    def __init__(self, parent, records):
        super().__init__(parent)
        self.records = records
        self.setWindowTitle("Preview Reference Label(s) / संदर्भ लेबल पूर्वावलोकन")
        self.setMinimumSize(500, 400)
        
        layout = QVBoxLayout(self)
        
        # Info Label
        info = QLabel(f"Previewing {len(records)} label(s). NO: and Date: will be left blank for handwriting.")
        info.setStyleSheet("color: #444; font-size: 13px; font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(info)
        
        # Preview Text Area
        self.preview_area = QTextEdit()
        self.preview_area.setReadOnly(True)
        self.preview_area.setStyleSheet("background-color: #FAFAFA; border: 1px solid #CCC; font-size: 14px; padding: 10px;")
        
        html = "<html><body style='font-family: sans-serif;'>"
        for rec in records:
            html += "<table width='100%' style='border: 1px dashed #888; margin-bottom: 15px; border-collapse: collapse;'>"
            html += "<tr>"
            
            # Left side (50%)
            html += "<td width='50%' style='padding: 15px; vertical-align: top; border-right: 1px solid #333;'>"
            html += "<div><strong>NO: -</strong></div>"
            html += "<div><strong>Date: -</strong></div>"
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
        
        # Buttons
        btn_layout = QHBoxLayout()
        btn_layout.addStretch(1)
        
        self.btn_cancel = QPushButton("Cancel")
        self.btn_cancel.clicked.connect(self.reject)
        
        self.btn_print = QPushButton("🖨 Print")
        self.btn_print.setStyleSheet("QPushButton { background-color: #7A1212; color: white; border-radius: 4px; padding: 8px 16px; font-weight: bold; } QPushButton:hover { background-color: #5C0D0D; }")
        self.btn_print.clicked.connect(self.accept)
        
        btn_layout.addWidget(self.btn_cancel)
        btn_layout.addWidget(self.btn_print)
        layout.addLayout(btn_layout)"""

new_dialog = """class ReferenceLabelPreviewDialog(QDialog):
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
        info = QLabel(f"Previewing {len(records)} label(s). NO: and Date: will be left blank for handwriting.")
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
            
            # Left side (50%)
            html += "<td width='50%' style='padding: 15px; vertical-align: top; border-right: 1px solid #333;'>"
            html += "<div><strong>NO: -</strong></div>"
            html += "<div><strong>Date: -</strong></div>"
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

content_view = content_view.replace(old_dialog, new_dialog)

# Update _print_selected_list to pass print_mode
old_print_call = """                from modules.print_module import generate_reference_labels_pdf
                ok, result = generate_reference_labels_pdf(checked, path)"""
new_print_call = """                from modules.print_module import generate_reference_labels_pdf
                ok, result = generate_reference_labels_pdf(checked, path, dialog.print_mode)"""

content_view = content_view.replace(old_print_call, new_print_call)

with open(file_path_view, "w", encoding="utf-8") as f:
    f.write(content_view)


# 2. Update print_module.py
file_path_print = r"c:\Users\KANIKA SINGHAL\OneDrive\Desktop\New folder\CANTEEN_MANAGEMENT_SYSTEM\ADRDE_DRDO\ADRDE_ADDRESS\modules\print_module.py"

with open(file_path_print, "r", encoding="utf-8") as f:
    content_print = f.read()

# Update function definition and logic
old_func = """def generate_reference_labels_pdf(records: list, output_path: str) -> tuple[bool, str]:
    \"\"\"Generate reference labels matching the user's sketch.\"\"\"
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import cm
        from reportlab.lib import colors

        doc = SimpleDocTemplate(
            output_path,
            pagesize=A4,
            rightMargin=1.5*cm,
            leftMargin=1.5*cm,
            topMargin=1.5*cm,
            bottomMargin=1.5*cm
        )
        
        styles = getSampleStyleSheet()
        left_style = ParagraphStyle(
            'LeftStyle',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=12,
            leading=16,
        )
        right_style = ParagraphStyle(
            'RightStyle',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=12,
            leading=16,
        )

        elements = []

        for rec in records:
            left_content = "NO: -<br/>Date: -"
            
            right_lines = ["TO,"]
            if rec.get("to_field"):
                right_lines.append(rec["to_field"])
            if rec.get("designation"):
                right_lines.append(rec["designation"])
            if rec.get("office_name"):
                right_lines.append(rec["office_name"])
            if rec.get("addr_line1"):
                right_lines.append(rec["addr_line1"])
            if rec.get("addr_line2"):
                right_lines.append(rec["addr_line2"])
                
            city_state_pin = ", ".join(filter(None, [rec.get("city", ""), rec.get("state", "")]))
            if rec.get("pin_code"):
                if city_state_pin:
                    city_state_pin += " - " + rec["pin_code"]
                else:
                    city_state_pin = "PIN: " + rec["pin_code"]
            if city_state_pin:
                right_lines.append(city_state_pin)
                
            right_content = "<br/>".join(right_lines)
            
            data = [
                [Paragraph(left_content, left_style), Paragraph(right_content, right_style)]
            ]
            
            # Table layout with a vertical line
            tbl = Table(data, colWidths=[8.5*cm, 8.5*cm])
            tbl.setStyle(TableStyle([
                ('VALIGN', (0,0), (-1,-1), 'TOP'),
                ('LINEBEFORE', (1,0), (1,-1), 1, colors.black),
                ('LEFTPADDING', (1,0), (1,-1), 15),
                ('RIGHTPADDING', (0,0), (0,-1), 15),
                ('TOPPADDING', (0,0), (-1,-1), 20),
                ('BOTTOMPADDING', (0,0), (-1,-1), 20),
            ]))
            
            elements.append(tbl)
            elements.append(Spacer(1, 2*cm))
            
        doc.build(elements)
        return True, output_path
    except Exception as e:
        return False, str(e)"""

new_func = """def generate_reference_labels_pdf(records: list, output_path: str, print_mode: str = "both") -> tuple[bool, str]:
    \"\"\"Generate reference labels matching the user's sketch, with modes left/right/both.\"\"\"
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import cm
        from reportlab.lib import colors

        doc = SimpleDocTemplate(
            output_path,
            pagesize=A4,
            rightMargin=1.5*cm,
            leftMargin=1.5*cm,
            topMargin=1.5*cm,
            bottomMargin=1.5*cm
        )
        
        styles = getSampleStyleSheet()
        left_style = ParagraphStyle(
            'LeftStyle',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=12,
            leading=16,
        )
        right_style = ParagraphStyle(
            'RightStyle',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=12,
            leading=16,
        )

        elements = []

        for rec in records:
            left_content = "NO: -<br/>Date: -" if print_mode in ("both", "left") else ""
            
            right_lines = ["TO,"]
            if rec.get("to_field"):
                right_lines.append(rec["to_field"])
            if rec.get("designation"):
                right_lines.append(rec["designation"])
            if rec.get("office_name"):
                right_lines.append(rec["office_name"])
            if rec.get("addr_line1"):
                right_lines.append(rec["addr_line1"])
            if rec.get("addr_line2"):
                right_lines.append(rec["addr_line2"])
                
            city_state_pin = ", ".join(filter(None, [rec.get("city", ""), rec.get("state", "")]))
            if rec.get("pin_code"):
                if city_state_pin:
                    city_state_pin += " - " + rec["pin_code"]
                else:
                    city_state_pin = "PIN: " + rec["pin_code"]
            if city_state_pin:
                right_lines.append(city_state_pin)
                
            right_content = "<br/>".join(right_lines) if print_mode in ("both", "right") else ""
            
            data = [
                [Paragraph(left_content, left_style) if left_content else "", 
                 Paragraph(right_content, right_style) if right_content else ""]
            ]
            
            # Table layout
            tbl = Table(data, colWidths=[8.5*cm, 8.5*cm])
            
            t_styles = [
                ('VALIGN', (0,0), (-1,-1), 'TOP'),
                ('LEFTPADDING', (1,0), (1,-1), 15),
                ('RIGHTPADDING', (0,0), (0,-1), 15),
                ('TOPPADDING', (0,0), (-1,-1), 20),
                ('BOTTOMPADDING', (0,0), (-1,-1), 20),
            ]
            
            if print_mode == "both":
                t_styles.append(('LINEBEFORE', (1,0), (1,-1), 1, colors.black))
                
            tbl.setStyle(TableStyle(t_styles))
            
            elements.append(tbl)
            elements.append(Spacer(1, 2*cm))
            
        doc.build(elements)
        return True, output_path
    except Exception as e:
        return False, str(e)"""

content_print = content_print.replace(old_func, new_func)

with open(file_path_print, "w", encoding="utf-8") as f:
    f.write(content_print)
