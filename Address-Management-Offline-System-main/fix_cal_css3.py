import os

calendar_css = '''cal.setStyleSheet(\"\"\"
    QCalendarWidget { 
        background-color: #F8F9FA; 
        color: #212529;
        border: 1px solid #DEE2E6;
    }
    QCalendarWidget QWidget {
        alternate-background-color: #F8F9FA;
    }
    QCalendarWidget QAbstractItemView:enabled {
        color: #212529;
        background-color: #FFFFFF;
        selection-background-color: #0078D7;
        selection-color: #FFFFFF;
    }
    QCalendarWidget QWidget#qt_calendar_navigationbar { 
        background-color: #F8F9FA; 
        border-bottom: 1px solid #DEE2E6; 
    }
    QCalendarWidget QToolButton { 
        color: #212529; 
        background-color: transparent; 
        font-weight: bold; 
    }
    QCalendarWidget QToolButton:hover { background-color: #E7F1FF; }
    QCalendarWidget QSpinBox { background-color: #FFFFFF; color: #212529; }
    QCalendarWidget QTableView { 
        background-color: #FFFFFF; 
        color: #212529; 
        selection-background-color: #0078D7; 
        selection-color: #FFFFFF;
    }
    QCalendarWidget QTableView:hover {
        background-color: #E7F1FF;
    }
    QCalendarWidget QHeaderView { background-color: #F8F9FA; }
    QCalendarWidget QHeaderView::section { 
        background-color: #F8F9FA; 
        color: #212529; 
        font-weight: bold; 
    }
\"\"\")'''

files_to_check = ['ui/address_view.py', 'ui/address_form.py']

for file in files_to_check:
    if not os.path.exists(file): continue
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
        
    import re
    content = re.sub(r'cal\.setStyleSheet\(""\".*?\"""\)', calendar_css, content, flags=re.DOTALL)
            
    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)
print('Done updating to exact requested CSS!')
