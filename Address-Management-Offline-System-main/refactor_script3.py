import sys

with open('ui/address_view.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Add itemChanged signal
old_signals = '''        self.table.itemSelectionChanged.connect(self._on_row_selected)
        self.table.doubleClicked.connect(self._on_row_double_clicked)'''
new_signals = '''        self.table.itemSelectionChanged.connect(self._on_row_selected)
        self.table.doubleClicked.connect(self._on_row_double_clicked)
        self.table.itemChanged.connect(self._set_action_btns)'''
content = content.replace(old_signals, new_signals)

# Replace _set_action_btns logic
old_set_actions = '''    def _set_action_btns(self, enabled: bool):
        self.view_btn.setEnabled(enabled)
        self.print_btn.setEnabled(True)
        self.preview_open_btn.setEnabled(enabled)
        self.preview_print_btn.setEnabled(enabled)
        if self.role == "admin":
            self.edit_btn.setEnabled(enabled)
            self.del_btn.setEnabled(enabled)'''

# Note: preview_print_btn was removed, so old_set_actions string from previous steps still has it because my refactor script replaced _update_actions_state, not _set_action_btns! Wait, earlier I discovered this, let's look at the exact content of _set_action_btns.

# To be safe, use regex or find to replace _set_action_btns fully
import re
pattern = re.compile(r'    def _set_action_btns\(self.*?def _update_preview', re.DOTALL)

new_set_actions = '''    def _set_action_btns(self, *args, **kwargs):
        checked = self._get_checked_records()
        sel_count = len(checked)
        
        if sel_count == 0 and self._selected_record:
            sel_count = 1

        if sel_count == 0:
            self.view_btn.setEnabled(False)
            self.preview_open_btn.setEnabled(False)
            if self.role == "admin":
                self.edit_btn.setEnabled(False)
                self.del_btn.setEnabled(False)
            return

        self.view_btn.setEnabled(True)
        self.preview_open_btn.setEnabled(sel_count == 1)
        if self.role == "admin":
            self.edit_btn.setEnabled(sel_count == 1)
            self.del_btn.setEnabled(sel_count >= 1)

    def _update_preview'''

content = pattern.sub(new_set_actions, content)

with open('ui/address_view.py', 'w', encoding='utf-8') as f:
    f.write(content)
print('Action buttons script completed successfully.')
