import os
import re

calendar_css = '''cal.setStyleSheet(\"\"\"
    QCalendarWidget { 
        background-color: #FFFFFF; 
        color: #333333;
        border: 1px solid #E5E7EB;
        border-radius: 10px;
    }
    QCalendarWidget QWidget {
        alternate-background-color: #FFFFFF;
    }
    QCalendarWidget QAbstractItemView:enabled {
        color: #333333;
        background-color: #FFFFFF;
        selection-background-color: #2563EB;
        selection-color: #FFFFFF;
    }
    QCalendarWidget QAbstractItemView:disabled {
        color: #BDBDBD;
    }
    QCalendarWidget QWidget#qt_calendar_navigationbar { 
        background-color: #FFFFFF; 
        border-bottom: 1px solid #E5E7EB; 
    }
    QCalendarWidget QToolButton { 
        color: #333333; 
        background-color: transparent; 
        font-weight: bold; 
    }
    QCalendarWidget QToolButton:hover { background-color: #E3F2FD; }
    QCalendarWidget QSpinBox { background-color: #FFFFFF; color: #333333; }
    QCalendarWidget QTableView { 
        background-color: #FFFFFF; 
        color: #333333; 
        selection-background-color: #2563EB; 
        selection-color: #FFFFFF;
    }
    QCalendarWidget QTableView:hover {
        background-color: #E3F2FD;
    }
    QCalendarWidget QHeaderView { background-color: #FFFFFF; }
    QCalendarWidget QHeaderView::section { 
        background-color: #FFFFFF; 
        color: #1E3A8A; 
        font-weight: bold; 
    }
\"\"\")'''

files_to_check = ['ui/address_view.py', 'ui/address_form.py']

for file in files_to_check:
    if not os.path.exists(file): continue
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
        
    content = re.sub(r'cal\.setStyleSheet\(""\".*?\"""\)', calendar_css, content, flags=re.DOTALL)
    
    # Update Sunday format color
    content = re.sub(r"QColor\('#DC3545'\)", "QColor('#E53935')", content)
            
    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)
print('Done updating to modern exact requested CSS!')
