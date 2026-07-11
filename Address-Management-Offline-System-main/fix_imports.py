import os

files_to_check = ['ui/settings_dialog.py', 'ui/user_manager.py']

for file in files_to_check:
    if not os.path.exists(file): continue
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
        
    if 'QStyleFactory' not in content:
        content = content.replace('QComboBox', 'QComboBox, QStyleFactory')
            
    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)
print('Done fixing imports!')
