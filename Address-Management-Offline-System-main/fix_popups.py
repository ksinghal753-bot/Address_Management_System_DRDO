import os

files_to_check = ['ui/address_view.py', 'ui/address_form.py', 'ui/settings_dialog.py', 'ui/user_manager.py']

for file in files_to_check:
    if not os.path.exists(file): continue
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
        
    if 'QListView' not in content:
        content = content.replace('QComboBox,', 'QComboBox, QListView, QCalendarWidget,')
        
    lines = content.split('\n')
    new_lines = []
    
    for line in lines:
        new_lines.append(line)
        if '= QComboBox()' in line:
            indent = line.split('=')[0][:-len(line.split('=')[0].lstrip())]
            var_name = line.split('=')[0].strip()
            # Don't add if it's already there
            new_lines.append(indent + var_name + '.setView(QListView())')
        if '= QDateEdit()' in line:
            indent = line.split('=')[0][:-len(line.split('=')[0].lstrip())]
            var_name = line.split('=')[0].strip()
            new_lines.append(indent + var_name + '.setCalendarWidget(QCalendarWidget())')
            
    with open(file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(new_lines))
print('Done injecting setView!')
