import os

# 1. Update address_view.py
file_path_view = r"c:\Users\KANIKA SINGHAL\OneDrive\Desktop\New folder\CANTEEN_MANAGEMENT_SYSTEM\ADRDE_DRDO\ADRDE_ADDRESS\ui\address_view.py"

with open(file_path_view, "r", encoding="utf-8") as f:
    content_view = f.read()

old_loop = '''        for rec in records:
            html += "<table width='100%' style='border: 1px dashed #888; margin-bottom: 15px; border-collapse: collapse;'>"
            html += "<tr>"
            
            # Left side (50%)
            html += "<td width='50%' style='padding: 15px; vertical-align: top; border-right: 1px solid #333;'>"
            html += "<div><strong>NO: -</strong></div>"
            html += "<div><strong>Date: -</strong></div>"
            html += "</td>"
            
            # Right side (50%)
            html += "<td width='50%' style='padding: 15px; vertical-align: top;'>"
            html += "<strong>TO,</strong><br>"'''

new_loop = '''        for rec in records:
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
            html += "<strong>TO,</strong><br>"'''

content_view = content_view.replace(old_loop, new_loop)

# Update the Info Label which says "NO: and Date: will be left blank"
old_info = 'info = QLabel(f"Previewing {len(records)} label(s). NO: and Date: will be left blank for handwriting.")'
new_info = 'info = QLabel(f"Previewing {len(records)} label(s). NO: and Date: auto-populated from record data.")'
content_view = content_view.replace(old_info, new_info)

with open(file_path_view, "w", encoding="utf-8") as f:
    f.write(content_view)


# 2. Update print_module.py
file_path_print = r"c:\Users\KANIKA SINGHAL\OneDrive\Desktop\New folder\CANTEEN_MANAGEMENT_SYSTEM\ADRDE_DRDO\ADRDE_ADDRESS\modules\print_module.py"

with open(file_path_print, "r", encoding="utf-8") as f:
    content_print = f.read()

old_print_logic = """        for rec in records:
            left_content = "NO: -<br/>Date: -" if print_mode in ("both", "left") else ""
            
            right_lines = ["TO,"]"""

new_print_logic = """        for rec in records:
            ref_no = format_ref_no(rec.get("para_no", ""), rec.get("date_entry", ""))
            ref_parts = ref_no.split("\\n")
            no_line = ref_parts[0]
            date_line = ref_parts[1] if len(ref_parts) > 1 else ""
            
            if print_mode in ("both", "left"):
                left_content = f"{no_line}<br/>{date_line}"
            else:
                left_content = ""
                
            right_lines = ["TO,"]"""

content_print = content_print.replace(old_print_logic, new_print_logic)

with open(file_path_print, "w", encoding="utf-8") as f:
    f.write(content_print)
