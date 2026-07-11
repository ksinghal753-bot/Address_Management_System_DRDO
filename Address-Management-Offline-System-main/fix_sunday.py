import os

sunday_code = '''
        from PySide6.QtGui import QTextCharFormat, QColor
        from PySide6.QtCore import Qt
        fmt = QTextCharFormat()
        fmt.setForeground(QColor('#DC3545'))
        cal.setWeekdayTextFormat(Qt.Sunday, fmt)
'''

files_to_check = ['ui/address_view.py', 'ui/address_form.py']

for file in files_to_check:
    if not os.path.exists(file): continue
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
        
    lines = content.split('\n')
    new_lines = []
    
    for line in lines:
        new_lines.append(line)
        if 'cal.setPalette(palette)' in line:
            indent = line.split('cal.')[0]
            for s_line in sunday_code.split('\n'):
                if s_line.strip():
                    new_lines.append(indent + s_line.strip())
            
    with open(file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(new_lines))
print('Done adding Sunday formatting!')
