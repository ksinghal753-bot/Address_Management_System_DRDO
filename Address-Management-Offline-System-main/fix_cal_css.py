import os

calendar_css = '''cal.setStyleSheet(\"\"\"
    QCalendarWidget { background-color: #FFFFFF; border: 1px solid #D0D0D0; }
    QCalendarWidget QWidget#qt_calendar_navigationbar { background-color: #FFFFFF; border-bottom: 1px solid #D0D0D0; }
    QCalendarWidget QToolButton { color: #000000; background-color: transparent; font-weight: bold; }
    QCalendarWidget QToolButton:hover { background-color: #F2F2F2; }
    QCalendarWidget QSpinBox { background-color: #FFFFFF; color: #000000; }
    QCalendarWidget QTableView { background-color: #FFFFFF; color: #000000; alternate-background-color: #FFFFFF; }
    QCalendarWidget QHeaderView { background-color: #FFFFFF; }
    QCalendarWidget QHeaderView::section { background-color: #FFFFFF; color: #000000; font-weight: bold; }
\"\"\")'''

files_to_check = ['ui/address_view.py', 'ui/address_form.py']

for file in files_to_check:
    if not os.path.exists(file): continue
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
        
    lines = content.split('\n')
    new_lines = []
    
    for line in lines:
        new_lines.append(line)
        if 'cal = QCalendarWidget()' in line:
            indent = line.split('cal =')[0]
            for css_line in calendar_css.split('\n'):
                if css_line.strip():
                    new_lines.append(indent + css_line)
            
    with open(file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(new_lines))
print('Done adding inline stylesheet to calendars!')
