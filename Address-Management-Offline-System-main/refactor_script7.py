import sys

function_code = """
def generate_address_list_pdf(records: list, output_path: str) -> tuple[bool, str]:
    \"\"\"Generate full address list PDF (table format) including Email, Contact, Fax.\"\"\"
    try:
        from reportlab.lib.pagesizes import landscape, A2
        # Use a very wide page (A2 Landscape) to fit all the columns comfortably
        doc = SimpleDocTemplate(
            output_path,
            pagesize=landscape(A2),
            topMargin=3.5*cm,
            bottomMargin=1.5*cm,
            leftMargin=2*cm,
            rightMargin=2*cm
        )
        styles = _get_styles()

        def header_footer(canvas, doc):
            _build_page_header(canvas, doc, "Complete Address List / पूर्ण पता सूची")

        elements = []
        elements.append(Spacer(1, 5*mm))

        col_headers = [
            Paragraph("#", styles["table_header"]),
            Paragraph("Dept\\nविभाग", styles["table_header"]),
            Paragraph("To\\nसेवा में", styles["table_header"]),
            Paragraph("Designation\\nपदनाम", styles["table_header"]),
            Paragraph("Office Name\\nकार्यालय", styles["table_header"]),
            Paragraph("Address\\nपता", styles["table_header"]),
            Paragraph("City, State\\nशहर, राज्य", styles["table_header"]),
            Paragraph("PIN\\nपिन", styles["table_header"]),
            Paragraph("Email\\nईमेल", styles["table_header"]),
            Paragraph("Contact\\nसंपर्क", styles["table_header"]),
            Paragraph("Fax\\nफैक्स", styles["table_header"]),
            Paragraph("PARA\\nपैरा", styles["table_header"]),
            Paragraph("Date\\nदिनांक", styles["table_header"]),
            Paragraph("By S/P\\nडाक", styles["table_header"]),
        ]

        table_data = [col_headers]
        for i, rec in enumerate(records, 1):
            addr = rec.get("addr_line1", "")
            if rec.get("addr_line2"):
                addr += "\\n" + rec["addr_line2"]
            try:
                d = datetime.strptime(rec.get("date_entry", ""), "%Y-%m-%d")
                date_str = d.strftime("%d-%m-%Y")
            except Exception:
                date_str = rec.get("date_entry", "")

            table_data.append([
                Paragraph(str(i), styles["table_cell"]),
                Paragraph(rec.get("dept_name", ""), styles["table_cell"]),
                Paragraph(rec.get("to_field", ""), styles["table_cell"]),
                Paragraph(rec.get("designation", ""), styles["table_cell"]),
                Paragraph(rec.get("office_name", ""), styles["table_cell"]),
                Paragraph(addr, styles["table_cell"]),
                Paragraph(f"{rec.get('city','')}, {rec.get('state','')}", styles["table_cell"]),
                Paragraph(rec.get("pin_code", ""), styles["table_cell"]),
                Paragraph(rec.get("email", ""), styles["table_cell"]),
                Paragraph(rec.get("contact_no", ""), styles["table_cell"]),
                Paragraph(rec.get("fax", ""), styles["table_cell"]),
                Paragraph(rec.get("para_no", ""), styles["table_cell"]),
                Paragraph(date_str, styles["table_cell"]),
                Paragraph(rec.get("delivery_type", "")[:12], styles["table_cell"]),
            ])

        # Widths for 14 columns
        col_widths = [0.8*cm, 2.5*cm, 2.5*cm, 3.5*cm, 4*cm, 6*cm, 3.5*cm, 1.8*cm, 4.5*cm, 3*cm, 3*cm, 1.5*cm, 2.2*cm, 2.5*cm]
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

with open(r"c:\Users\KANIKA SINGHAL\OneDrive\Desktop\New folder\CANTEEN_MANAGEMENT_SYSTEM\ADRDE_DRDO\ADRDE_ADDRESS\modules\print_module.py", "a", encoding="utf-8") as f:
    f.write("\n" + function_code + "\n")
