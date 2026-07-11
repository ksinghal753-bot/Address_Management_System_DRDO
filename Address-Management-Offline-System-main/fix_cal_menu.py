import os
import re

extra_css = '''
    QMenu {
        background-color: #FFFFFF;
        color: #333333;
        border: 1px solid #E5E7EB;
    }
    QMenu::item {
        background-color: transparent;
        color: #333333;
        padding: 4px 16px;
    }
    QMenu::item:selected {
        background-color: #E3F2FD;
    }
    QListView {
        background-color: #FFFFFF;
        color: #333333;
    }
'''

files_to_check = ['ui/address_view.py', 'ui/address_form.py']

for file in files_to_check:
    if not os.path.exists(file): continue
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Inject before the final '\"\"\"' in the stylesheet string
    if 'QMenu {' not in content:
        content = content.replace('QCalendarWidget QHeaderView::section { \n        background-color: #FFFFFF; \n        color: #1E3A8A; \n        font-weight: bold; \n    }', 'QCalendarWidget QHeaderView::section { \n        background-color: #FFFFFF; \n        color: #1E3A8A; \n        font-weight: bold; \n    }' + extra_css)
            
        with open(file, 'w', encoding='utf-8') as f:
            f.write(content)
print('Done injecting QMenu styles to calendar!')
