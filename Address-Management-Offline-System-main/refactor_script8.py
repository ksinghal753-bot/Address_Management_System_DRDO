import os

file_path = r"c:\Users\KANIKA SINGHAL\OneDrive\Desktop\New folder\CANTEEN_MANAGEMENT_SYSTEM\ADRDE_DRDO\ADRDE_ADDRESS\modules\print_module.py"

with open(file_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if line.startswith("def generate_address_list_pdf"):
        lines = lines[:i]
        break

new_function = """def generate_address_list_pdf(records: list, output_path: str, selected_columns: list = None) -> tuple[bool, str]:
    \"\"\"Generate full address list PDF (table format) including selected columns.\"\"\"
    try:
        from reportlab.lib.pagesizes import landscape, A2, A3, A4
        styles = _get_styles()

        def header_footer(canvas, doc):
            _build_page_header(canvas, doc, "Complete Address List / पूर्ण पता सूची")

        elements = []
        elements.append(Spacer(1, 5*mm))

        all_cols_def = [
            ("dept_name", "Dept\\nविभाग", 2.5*cm),
            ("to_field", "To\\nसेवा में", 2.5*cm),
            ("designation", "Designation\\nपदनाम", 3.5*cm),
            ("office_name", "Office Name\\nकार्यालय", 4*cm),
            ("address", "Address\\nपता", 6*cm),
            ("city_state", "City, State\\nशहर, राज्य", 3.5*cm),
            ("pin_code", "PIN\\nपिन", 1.8*cm),
            ("email", "Email\\nईमेल", 4.5*cm),
            ("contact_no", "Contact\\nसंपर्क", 3*cm),
            ("fax", "Fax\\nफैक्स", 3*cm),
            ("para_no", "PARA\\nपैरा", 1.5*cm),
            ("date_entry", "Date\\nदिनांक", 2.2*cm),
            ("delivery_type", "By S/P\\nडाक", 2.5*cm)
        ]

        if not selected_columns:
            selected_columns = [c[0] for c in all_cols_def]

        active_cols = [c for c in all_cols_def if c[0] in selected_columns]
        
        # Calculate total width to pick a page size
        total_w = 0.8*cm + sum([c[2] for c in active_cols])
        # A4 Landscape width is ~29.7cm
        # A3 Landscape width is ~42cm
        # A2 Landscape width is ~59.4cm
        if total_w < 25*cm:
            psize = landscape(A4)
        elif total_w < 38*cm:
            psize = landscape(A3)
        else:
            psize = landscape(A2)

        doc = SimpleDocTemplate(
            output_path,
            pagesize=psize,
            topMargin=3.5*cm,
            bottomMargin=1.5*cm,
            leftMargin=2*cm,
            rightMargin=2*cm
        )

        col_headers = [Paragraph("#", styles["table_header"])]
        for c in active_cols:
            col_headers.append(Paragraph(c[1], styles["table_header"]))

        table_data = [col_headers]
        for i, rec in enumerate(records, 1):
            row = [Paragraph(str(i), styles["table_cell"])]
            for col_id, _, _ in active_cols:
                if col_id == "address":
                    addr = rec.get("addr_line1", "")
                    if rec.get("addr_line2"):
                        addr += "\\n" + rec["addr_line2"]
                    row.append(Paragraph(addr, styles["table_cell"]))
                elif col_id == "city_state":
                    row.append(Paragraph(f"{rec.get('city','')}, {rec.get('state','')}", styles["table_cell"]))
                elif col_id == "date_entry":
                    try:
                        d = datetime.strptime(rec.get("date_entry", ""), "%Y-%m-%d")
                        date_str = d.strftime("%d-%m-%Y")
                    except Exception:
                        date_str = rec.get("date_entry", "")
                    row.append(Paragraph(date_str, styles["table_cell"]))
                elif col_id == "delivery_type":
                    row.append(Paragraph(rec.get("delivery_type", "")[:12], styles["table_cell"]))
                else:
                    row.append(Paragraph(rec.get(col_id, ""), styles["table_cell"]))
            table_data.append(row)

        col_widths = [0.8*cm] + [c[2] for c in active_cols]
        tbl = Table(table_data, colWidths=col_widths, repeatRows=1)
        tbl.setStyle(TableStyle([
            ("BACKGROUND",    (0, 0), (-1, 0),   NAVY),
            ("TEXTCOLOR",     (0, 0), (-1, 0),   WHITE),
            ("ROWBACKGROUNDS",(0, 1), (-1, -1),  [WHITE, colors.HexColor("#EDF2F7")]),
            ("GRID",          (0, 0), (-1, -1),  0.5, colors.HexColor("#B0B8C4")),
            ("VALIGN",        (0, 0), (-1, -1),  "TOP"),
            ("TOPPADDING",    (0, 0), (-1, -1),  4),
            ("BOTTOMPADDING", (0, 0), (-1, -1),  4),
            ("LEFTPADDING",   (0, 0), (-1, -1),  4),
            ("RIGHTPADDING",  (0, 0), (-1, -1),  4),
            ("LINEBELOW",     (0, 0), (-1, 0),   2, GOLD),
        ]))
        elements.append(tbl)
        doc.build(elements, onFirstPage=header_footer, onLaterPages=header_footer)
        return True, output_path
    except Exception as e:
        return False, str(e)
"""

with open(file_path, "w", encoding="utf-8") as f:
    f.writelines(lines)
    f.write(new_function)
