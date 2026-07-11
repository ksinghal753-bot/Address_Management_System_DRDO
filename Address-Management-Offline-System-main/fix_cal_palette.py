import os

palette_code = '''        palette = cal.palette()
        from PySide6.QtGui import QColor, QPalette
        palette.setColor(QPalette.Window, QColor(255, 255, 255))
        palette.setColor(QPalette.Base, QColor(255, 255, 255))
        palette.setColor(QPalette.WindowText, QColor(0, 0, 0))
        palette.setColor(QPalette.Text, QColor(0, 0, 0))
        palette.setColor(QPalette.Button, QColor(255, 255, 255))
        palette.setColor(QPalette.ButtonText, QColor(0, 0, 0))
        cal.setPalette(palette)'''

files_to_check = ['ui/address_view.py', 'ui/address_form.py']

for file in files_to_check:
    if not os.path.exists(file): continue
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
        
    lines = content.split('\n')
    new_lines = []
    
    for line in lines:
        new_lines.append(line)
        if 'cal.setStyle(QStyleFactory.create(' in line:
            indent = line.split('cal.')[0]
            for p_line in palette_code.split('\n'):
                # strip the 8 spaces and add indent
                new_lines.append(indent + p_line[8:])
            
    with open(file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(new_lines))
print('Done adding explicit QPalette to calendars!')
