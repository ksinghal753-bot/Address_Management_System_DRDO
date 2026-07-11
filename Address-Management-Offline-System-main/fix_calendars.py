import os

files_to_check = ['ui/address_view.py', 'ui/address_form.py']

for file in files_to_check:
    if not os.path.exists(file): continue
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
        
    if 'QStyleFactory' not in content:
        content = content.replace('QCalendarWidget,', 'QCalendarWidget, QStyleFactory,')
        
    lines = content.split('\n')
    new_lines = []
    
    for line in lines:
        if '.setCalendarWidget(QCalendarWidget())' in line:
            indent = line.split('.')[0][:-len(line.split('.')[0].lstrip())]
            var_name = line.split('.')[0].strip()
            new_lines.append(indent + "cal = QCalendarWidget()")
            new_lines.append(indent + "cal.setStyle(QStyleFactory.create('Fusion'))")
            new_lines.append(indent + var_name + ".setCalendarWidget(cal)")
        else:
            new_lines.append(line)
            
    with open(file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(new_lines))
print('Done fixing calendars!')
