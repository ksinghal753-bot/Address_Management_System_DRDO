import os

file_path = 'main.py'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

if 'app.setStyle(\"Fusion\")' not in content:
    content = content.replace('app.setStyleSheet(get_app_stylesheet(app_settings.get_theme()))', 'app.setStyle(\"Fusion\")\n    app.setStyleSheet(get_app_stylesheet(app_settings.get_theme()))')
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
        print('Fusion style applied to app in main.py')
else:
    print('Fusion style already applied')
