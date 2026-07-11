import os

# 1. Update address_view.py
file_path_view = r"c:\Users\KANIKA SINGHAL\OneDrive\Desktop\New folder\CANTEEN_MANAGEMENT_SYSTEM\ADRDE_DRDO\ADRDE_ADDRESS\ui\address_view.py"

with open(file_path_view, "r", encoding="utf-8") as f:
    content_view = f.read()

# Remove space between NO and Date in preview
old_left_td = """            html += "<td width='50%' style='padding: 15px; vertical-align: top; border-right: 1px solid #333;'>"
            html += "<div style='margin-bottom: 25px;'><strong>NO: -</strong></div>"
            html += "<div><strong>Date: -</strong></div>"
            html += "</td>" """

new_left_td = """            html += "<td width='50%' style='padding: 15px; vertical-align: top; border-right: 1px solid #333;'>"
            html += "<div><strong>NO: -</strong></div>"
            html += "<div><strong>Date: -</strong></div>"
            html += "</td>" """

content_view = content_view.replace(old_left_td, new_left_td)

# Rename Save to PDF to Print
old_btn = 'self.btn_print = QPushButton("🖨 Save to PDF")'
new_btn = 'self.btn_print = QPushButton("🖨 Print")'

content_view = content_view.replace(old_btn, new_btn)

with open(file_path_view, "w", encoding="utf-8") as f:
    f.write(content_view)


# 2. Update print_module.py
file_path_print = r"c:\Users\KANIKA SINGHAL\OneDrive\Desktop\New folder\CANTEEN_MANAGEMENT_SYSTEM\ADRDE_DRDO\ADRDE_ADDRESS\modules\print_module.py"

with open(file_path_print, "r", encoding="utf-8") as f:
    content_print = f.read()

# Update left_style to remove large spacing
old_left_style = """        left_style = ParagraphStyle(
            'LeftStyle',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=12,
            leading=24, # Large spacing for NO and Date
        )"""

new_left_style = """        left_style = ParagraphStyle(
            'LeftStyle',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=12,
            leading=16,
        )"""

content_print = content_print.replace(old_left_style, new_left_style)

# Update left_content to remove BR tags
old_left_content = '            left_content = "NO: -<br/><br/><br/>Date: -"'
new_left_content = '            left_content = "NO: -<br/>Date: -"'

content_print = content_print.replace(old_left_content, new_left_content)

# Update column widths to be exactly equal
old_table_def = '            tbl = Table(data, colWidths=[6*cm, 11*cm])'
# Total is 17cm, so 8.5 each
new_table_def = '            tbl = Table(data, colWidths=[8.5*cm, 8.5*cm])'

content_print = content_print.replace(old_table_def, new_table_def)

with open(file_path_print, "w", encoding="utf-8") as f:
    f.write(content_print)
