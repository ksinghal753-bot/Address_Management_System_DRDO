import os

file_path_view = r"c:\Users\KANIKA SINGHAL\OneDrive\Desktop\New folder\CANTEEN_MANAGEMENT_SYSTEM\ADRDE_DRDO\ADRDE_ADDRESS\ui\address_view.py"

with open(file_path_view, "r", encoding="utf-8") as f:
    content_view = f.read()

# 1. Wrap fields row in a QWidget to easily hide/show it
old_fields_row = """        # Row 2: Field Checkboxes
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
        selection_layout.addLayout(fields_row)"""

new_fields_row = """        # Row 2: Field Checkboxes
        self.fields_container = QWidget()
        fields_row = QHBoxLayout(self.fields_container)
        fields_row.setContentsMargins(0, 0, 0, 0)
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
        selection_layout.addWidget(self.fields_container)"""

content_view = content_view.replace(old_fields_row, new_fields_row)

# 2. Add Print Label button next to Print List button
old_print_btns = """        # Print List Button at bottom right
        bottom_action_row = QHBoxLayout()
        bottom_action_row.addStretch(1)
        self.btn_print_list_corner = QPushButton("📄 Print List / पता सूची प्रिंट करें")
        self.btn_print_list_corner.setCursor(Qt.PointingHandCursor)
        self.btn_print_list_corner.setStyleSheet(
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
        self.btn_print_list_corner.clicked.connect(self._enter_selection_mode)
        bottom_action_row.addWidget(self.btn_print_list_corner)"""

new_print_btns = """        # Print List and Label Buttons at bottom right
        bottom_action_row = QHBoxLayout()
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
        bottom_action_row.addWidget(self.btn_print_list_corner)"""

content_view = content_view.replace(old_print_btns, new_print_btns)

# 3. Update _enter_selection_mode and _cancel_selection_mode
old_enter_selection = """    def _enter_selection_mode(self):
        self.btn_print_list_corner.setVisible(False)
        self.selection_controls_widget.setVisible(True)

    def _cancel_selection_mode(self):
        self.selection_controls_widget.setVisible(False)
        self.btn_print_list_corner.setVisible(True)
        self._deselect_all_records()"""

new_enter_selection = """    def _enter_selection_mode(self, mode="list"):
        self.current_selection_mode = mode
        self.btn_print_list_corner.setVisible(False)
        self.btn_print_label_corner.setVisible(False)
        self.selection_controls_widget.setVisible(True)
        if mode == "label":
            self.fields_container.setVisible(False)
            self.btn_print_selected.setText("🖨 Print Selected Labels")
        else:
            self.fields_container.setVisible(True)
            self.btn_print_selected.setText("🖨 Print Selected List")

    def _cancel_selection_mode(self):
        self.selection_controls_widget.setVisible(False)
        self.btn_print_list_corner.setVisible(True)
        self.btn_print_label_corner.setVisible(True)
        self._deselect_all_records()"""

content_view = content_view.replace(old_enter_selection, new_enter_selection)

# 4. Update _print_selected_list
old_print_selected = """    def _print_selected_list(self):
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

new_print_selected = """    def _print_selected_list(self):
        checked = self._get_checked_records()
        if not checked:
            show_warning(self, "No Selection", "Please select at least one address to print.")
            return
            
        if getattr(self, "current_selection_mode", "list") == "label":
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

content_view = content_view.replace(old_print_selected, new_print_selected)

with open(file_path_view, "w", encoding="utf-8") as f:
    f.write(content_view)

# --- modules/print_module.py update ---

file_path_print = r"c:\Users\KANIKA SINGHAL\OneDrive\Desktop\New folder\CANTEEN_MANAGEMENT_SYSTEM\ADRDE_DRDO\ADRDE_ADDRESS\modules\print_module.py"

with open(file_path_print, "r", encoding="utf-8") as f:
    content_print = f.read()

new_label_function = """
def generate_reference_labels_pdf(records: list, output_path: str) -> tuple[bool, str]:
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
            leading=24, # Large spacing for NO and Date
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
            left_content = "NO: -<br/><br/><br/>Date: -"
            
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
            tbl = Table(data, colWidths=[6*cm, 11*cm])
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
        return False, str(e)
"""

if "def generate_reference_labels_pdf" not in content_print:
    with open(file_path_print, "a", encoding="utf-8") as f:
        f.write(new_label_function)
