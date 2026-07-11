import os

calendar_css = '''cal.setStyleSheet(\"\"\"
    QCalendarWidget { 
        background-color: #FFFFFF; 
        color: #000000;
    }
    QCalendarWidget QWidget {
        alternate-background-color: #FFFFFF;
    }
    QCalendarWidget QAbstractItemView:enabled {
        color: #000000;
        background-color: #FFFFFF;
        selection-background-color: #0078D7;
        selection-color: #FFFFFF;
    }
    QCalendarWidget QWidget#qt_calendar_navigationbar { 
        background-color: #FFFFFF; 
        border-bottom: 1px solid #D0D0D0; 
    }
    QCalendarWidget QToolButton { 
        color: #000000; 
        background-color: transparent; 
        font-weight: bold; 
    }
    QCalendarWidget QToolButton:hover { background-color: #F2F2F2; }
    QCalendarWidget QSpinBox { background-color: #FFFFFF; color: #000000; }
    QCalendarWidget QTableView { 
        background-color: #FFFFFF; 
        color: #000000; 
        selection-background-color: #0078D7; 
        selection-color: #FFFFFF;
    }
    QCalendarWidget QHeaderView { background-color: #FFFFFF; }
    QCalendarWidget QHeaderView::section { background-color: #FFFFFF; color: #000000; font-weight: bold; }
\"\"\")'''

files_to_check = ['ui/address_view.py', 'ui/address_form.py']

for file in files_to_check:
    if not os.path.exists(file): continue
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # We will just replace the old inline CSS with this new one
    import re
    # The old CSS started with cal.setStyleSheet(""" and ended with """)
    # Let's use regex to replace it
    content = re.sub(r'cal\.setStyleSheet\(""\".*?\"""\)', calendar_css, content, flags=re.DOTALL)
            
    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)
print('Done adding stronger inline stylesheet to calendars!')
