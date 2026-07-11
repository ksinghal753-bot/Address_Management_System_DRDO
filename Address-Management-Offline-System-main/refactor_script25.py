import re

with open('ui/address_view.py', 'r', encoding='utf-8') as f:
    c = f.read()

old_get_print = '''    def _get_print_path(self, suffix: str) -> str | None:
        out_dir = get_default_output_dir()
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        default_name = os.path.join(out_dir, f"ADRDE_{suffix}_{ts}.pdf")
        path, _ = QFileDialog.getSaveFileName(
            self, "Save PDF / PDF सहेजें",
            default_name,
            "PDF Files (*.pdf)"
        )
        return path if path else None'''

new_get_print = '''    def _get_print_path(self, suffix: str, default_ext=".pdf", no_dialog=False) -> str | None:
        out_dir = get_default_output_dir()
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        default_name = os.path.join(out_dir, f"ADRDE_{suffix}_{ts}{default_ext}")
        if no_dialog:
            return default_name
            
        ext_filter = "PDF Files (*.pdf)" if default_ext == ".pdf" else "Excel Files (*.xlsx)"
        title = "Save PDF / PDF सहेजें" if default_ext == ".pdf" else "Save Excel / Excel सहेजें"
        path, _ = QFileDialog.getSaveFileName(
            self, title,
            default_name,
            ext_filter
        )
        return path if path else None'''

if old_get_print in c:
    c = c.replace(old_get_print, new_get_print)
    with open('ui/address_view.py', 'w', encoding='utf-8') as f:
        f.write(c)
    print("Successfully replaced _get_print_path")
else:
    print("Could not find _get_print_path string")

