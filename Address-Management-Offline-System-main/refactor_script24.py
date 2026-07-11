import os
files = ['ui/address_view.py', 'ui/address_form.py']

view_old = '''        total_width = 55
        spaces_needed = max(2, total_width - len(no_line) - len(right_text))
        top_line = no_line + (" " * spaces_needed) + right_text

        addr_lines = []
        indent = "        "
        sub_indent = "           "
        to_val = rec.get("to_field", "").strip()
        if to_val and to_val.lower() not in ["to", "to,"]:
            addr_lines.append(f"{sub_indent}{to_val}")
        if rec.get("designation"):
            addr_lines.append(f"{sub_indent}{rec['designation']}")
        if rec.get("office_name"):
            addr_lines.append(f"{sub_indent}{rec['office_name']}")
        if rec.get("addr_line1"):
            addr_lines.append(f"{sub_indent}{rec['addr_line1']}")
        if rec.get("addr_line2"):
            addr_lines.append(f"{sub_indent}{rec['addr_line2']}")
        city_state = ", ".join(filter(None, [rec.get("city",""), rec.get("state","")]))
        if city_state:
            addr_lines.append(f"{sub_indent}{city_state}")
        if rec.get("pin_code"):
            addr_lines.append(f"{sub_indent}PIN Code: {rec['pin_code']}")

        lines = [
            top_line,
            date_line,
            "",
            "",
            f"{indent}To,",
        ] + addr_lines

        self.envelope_preview.setPlainText("\\n".join(lines))'''

view_new = '''        total_width = 75
        spaces_needed = max(2, total_width - len(no_line) - len(right_text))
        
        addr_lines = []
        to_val = rec.get("to_field", "").strip()
        if to_val and to_val.lower() not in ["to", "to,"]:
            addr_lines.append(to_val)
        if rec.get("designation"):
            addr_lines.append(rec['designation'])
        if rec.get("office_name"):
            addr_lines.append(rec['office_name'])
        if rec.get("addr_line1"):
            addr_lines.append(rec['addr_line1'])
        if rec.get("addr_line2"):
            addr_lines.append(rec['addr_line2'])
        city_state = ", ".join(filter(None, [rec.get("city",""), rec.get("state","")]))
        if city_state:
            addr_lines.append(city_state)
        if rec.get("pin_code"):
            addr_lines.append(f"PIN Code: {rec['pin_code']}")

        spc = "&nbsp;"
        indent_spaces = spc * 40
        top_spacing = spc * spaces_needed
        
        html = f"""
        <div style="font-family: 'Courier New', monospace; font-size: 13pt; line-height: 1.5;">
            <div style="font-weight: bold; color: #1a237e;">{no_line}{top_spacing}{right_text}</div>
            <div style="font-weight: bold; color: #1a237e;">{date_line}</div>
            <br>
            <div>{indent_spaces}To,</div>
        """
        for addr in addr_lines:
            html += f"            <div>{indent_spaces}{addr}</div>\\n"
        html += "        </div>"

        self.envelope_preview.setHtml(html)'''

with open('ui/address_view.py', 'r', encoding='utf-8') as f:
    c = f.read()
if view_old in c:
    c = c.replace(view_old, view_new)
    with open('ui/address_view.py', 'w', encoding='utf-8') as f:
        f.write(c)
        print('Updated address_view.py')
else:
    print('Failed to find old code in address_view.py')


form_old = '''        total_width = 55
        spaces_needed = max(2, total_width - len(ref) - len(right_text))
        top_line = ref + (" " * spaces_needed) + right_text

        addr_lines = []
        indent = "        "
        sub_indent = "           "
        to_val = self.to_field.text().strip()
        if to_val and to_val.lower() not in ["to", "to,"]:
            addr_lines.append(f"{sub_indent}{to_val}")
        if self.designation.text().strip():
            addr_lines.append(f"{sub_indent}{self.designation.text().strip()}")
        if self.office_name.text().strip():
            addr_lines.append(f"{sub_indent}{self.office_name.text().strip()}")
        if self.addr_line1.text().strip():
            addr_lines.append(f"{sub_indent}{self.addr_line1.text().strip()}")
        if self.addr_line2.text().strip():
            addr_lines.append(f"{sub_indent}{self.addr_line2.text().strip()}")

        city = self.city.text().strip()
        state = self.state.text().strip()
        if city or state:
            addr_lines.append(f"{sub_indent}{', '.join(filter(None, [city, state]))}")

        pin = self.pin_code.text().strip()
        if pin:
            addr_lines.append(f"{sub_indent}PIN Code: {pin}")

        lines = [
            top_line,
            date_line,
            "",
            "",
            f"{indent}To,",
        ] + addr_lines

        self.envelope_preview.setPlainText("\\n".join(lines))'''

form_new = '''        total_width = 75
        spaces_needed = max(2, total_width - len(ref) - len(right_text))
        
        addr_lines = []
        to_val = self.to_field.text().strip()
        if to_val and to_val.lower() not in ["to", "to,"]:
            addr_lines.append(to_val)
        if self.designation.text().strip():
            addr_lines.append(self.designation.text().strip())
        if self.office_name.text().strip():
            addr_lines.append(self.office_name.text().strip())
        if self.addr_line1.text().strip():
            addr_lines.append(self.addr_line1.text().strip())
        if self.addr_line2.text().strip():
            addr_lines.append(self.addr_line2.text().strip())

        city = self.city.text().strip()
        state = self.state.text().strip()
        if city or state:
            addr_lines.append(f"{', '.join(filter(None, [city, state]))}")

        pin = self.pin_code.text().strip()
        if pin:
            addr_lines.append(f"PIN Code: {pin}")

        spc = "&nbsp;"
        indent_spaces = spc * 40
        top_spacing = spc * spaces_needed
        
        html = f"""
        <div style="font-family: 'Courier New', monospace; font-size: 13pt; line-height: 1.5;">
            <div style="font-weight: bold; color: #1a237e;">{ref}{top_spacing}{right_text}</div>
            <div style="font-weight: bold; color: #1a237e;">{date_line}</div>
            <br>
            <div>{indent_spaces}To,</div>
        """
        for addr in addr_lines:
            html += f"            <div>{indent_spaces}{addr}</div>\\n"
        html += "        </div>"

        self.envelope_preview.setHtml(html)'''

with open('ui/address_form.py', 'r', encoding='utf-8') as f:
    c = f.read()
if form_old in c:
    c = c.replace(form_old, form_new)
    with open('ui/address_form.py', 'w', encoding='utf-8') as f:
        f.write(c)
        print('Updated address_form.py')
else:
    print('Failed to find old code in address_form.py')
