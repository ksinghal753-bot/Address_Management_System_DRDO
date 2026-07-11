import re

with open('ui/address_view.py', 'r', encoding='utf-8') as f:
    c = f.read()

# 1. _print_single
old1 = '''    def _print_single(self):
        if not self._selected_record:
            return
        # Confirmation box when clicking one address to ask print
        if not show_question(
            self,
            "Print Address / प्रिंट पुष्टीकरण",
            f"Do you want to print envelope for this address?\\n"
            f"क्या आप इस पते के लिए लिफाफा प्रिंट करना चाहते हैं?\\n\\n"
            f"Office: {self._selected_record.get('office_name','')}"
        ):
            return
        path = self._get_print_path("Envelope")
        if not path:
            return
        rec = self._get_record_for_print(self._selected_record)
        ok, result = generate_single_envelope_pdf(rec, path)
        if ok:
            show_info(self, "PDF Generated / PDF बना", LABELS["print_success"])
            open_pdf(path)
        else:
            show_error(self, "Print Error / प्रिंट त्रुटि", result)'''

new1 = '''    def _print_single(self):
        if not self._selected_record:
            return
        if not show_question(
            self,
            "Print Address / प्रिंट पुष्टीकरण",
            f"Do you want to print envelope for this address?\\n"
            f"क्या आप इस पते के लिए लिफाफा प्रिंट करना चाहते हैं?\\n\\n"
            f"Office: {self._selected_record.get('office_name','')}"
        ):
            return
        
        rec = self._get_record_for_print(self._selected_record)
        from modules.export_action import execute_export_action
        from modules.print_module import generate_single_envelope_pdf
        execute_export_action(
            parent_widget=self,
            records=[rec],
            pdf_suffix="Envelope",
            pdf_generator_func=lambda path: generate_single_envelope_pdf(rec, path),
            is_envelope_or_label=True
        )'''
c = c.replace(old1, new1)

# 2. _print_checked
old2 = '''    def _print_checked(self):
        checked = self._get_checked_records()
        if not checked:
            return
        path = self._get_print_path("Multiple_Envelopes")
        if not path:
            return
        recs = [self._get_record_for_print(r) for r in checked]
        ok, result = generate_multiple_envelopes_pdf(recs, path)
        if ok:
            show_info(self, "PDF Generated / PDF बना", LABELS["print_success"])
            open_pdf(path)
        else:
            show_error(self, "Print Error / प्रिंट त्रुटि", result)'''
new2 = '''    def _print_checked(self):
        checked = self._get_checked_records()
        if not checked:
            return
        recs = [self._get_record_for_print(r) for r in checked]
        from modules.export_action import execute_export_action
        from modules.print_module import generate_multiple_envelopes_pdf
        execute_export_action(
            parent_widget=self,
            records=recs,
            pdf_suffix="Multiple_Envelopes",
            pdf_generator_func=lambda path: generate_multiple_envelopes_pdf(recs, path),
            is_envelope_or_label=True
        )'''
c = c.replace(old2, new2)

# 3. _print_label
old3 = '''    def _print_label(self):
        checked = self._get_checked_records()
        if checked:
            path = self._get_print_path("Multiple_Labels")
            if not path:
                return
            recs = [self._get_record_for_print(r) for r in checked]
            ok, result = generate_multiple_labels_pdf(recs, path)
            if ok:
                show_info(self, "PDF Generated / PDF बना", LABELS["print_success"])
                open_pdf(path)
            else:
                show_error(self, "Print Error / प्रिंट त्रुटि", result)
            return

        if not self._selected_record:
            return
        path = self._get_print_path("Label")
        if not path:
            return
        rec = self._get_record_for_print(self._selected_record)
        ok, result = generate_single_label_pdf(rec, path)
        if ok:
            show_info(self, "PDF Generated / PDF बना", LABELS["print_success"])
            open_pdf(path)
        else:
            show_error(self, "Print Error / प्रिंट त्रुटि", result)'''
new3 = '''    def _print_label(self):
        checked = self._get_checked_records()
        if checked:
            recs = [self._get_record_for_print(r) for r in checked]
            from modules.export_action import execute_export_action
            from modules.print_module import generate_multiple_labels_pdf
            execute_export_action(
                parent_widget=self,
                records=recs,
                pdf_suffix="Multiple_Labels",
                pdf_generator_func=lambda path: generate_multiple_labels_pdf(recs, path),
                is_envelope_or_label=True
            )
            return

        if not self._selected_record:
            return
        rec = self._get_record_for_print(self._selected_record)
        from modules.export_action import execute_export_action
        from modules.print_module import generate_single_label_pdf
        execute_export_action(
            parent_widget=self,
            records=[rec],
            pdf_suffix="Label",
            pdf_generator_func=lambda path: generate_single_label_pdf(rec, path),
            is_envelope_or_label=True
        )'''
c = c.replace(old3, new3)

# 4. _print_selected_list
old4 = '''    def _print_selected_list(self):
        checked = self._get_checked_records()
        if not checked:
            show_warning(self, "No Selection", "Please select at least one address to print.")
            return
            
        if getattr(self, "current_selection_mode", "list") == "label":
            # Show preview dialog first
            dialog = ReferenceLabelPreviewDialog(self, checked)
            if dialog.exec() == QDialog.Accepted:
                path = self._get_print_path("ReferenceLabels")
                if not path:
                    return
                from modules.print_module import generate_reference_labels_pdf
                ok, result = generate_reference_labels_pdf(checked, path, dialog.selected_print_mode)
                if ok:
                    show_info(self, "PDF Generated / PDF बना", LABELS["print_success"])
                    open_pdf(path)
                    self._cancel_selection_mode()
                else:
                    show_error(self, "Print Error / प्रिंट त्रुटि", result)
            return

        selected_cols = [key for key, _ in self.field_definitions if self.field_checkboxes[key].isChecked()]
        if not selected_cols:
            show_warning(self, "No Columns Selected", "Please select at least one column to print.")
            return
            
        path = self._get_print_path("AddressList")
        if not path:
            return
            
        from modules.print_module import generate_address_list_pdf
        ok, result = generate_address_list_pdf(checked, path, selected_cols)
        if ok:
            show_info(self, "PDF Generated / PDF बना", LABELS["print_success"])
            open_pdf(path)
            self._cancel_selection_mode()
        else:
            show_error(self, "Print Error / प्रिंट त्रुटि", result)'''
new4 = '''    def _print_selected_list(self):
        checked = self._get_checked_records()
        if not checked:
            show_warning(self, "No Selection", "Please select at least one address to print.")
            return
            
        if getattr(self, "current_selection_mode", "list") == "label":
            # Show preview dialog first
            dialog = ReferenceLabelPreviewDialog(self, checked)
            if dialog.exec() == QDialog.Accepted:
                from modules.export_action import execute_export_action
                from modules.print_module import generate_reference_labels_pdf
                execute_export_action(
                    parent_widget=self,
                    records=checked,
                    pdf_suffix="ReferenceLabels",
                    pdf_generator_func=lambda path: generate_reference_labels_pdf(checked, path, dialog.selected_print_mode),
                    is_envelope_or_label=True
                )
                self._cancel_selection_mode()
            return

        selected_cols = [key for key, _ in self.field_definitions if self.field_checkboxes[key].isChecked()]
        if not selected_cols:
            show_warning(self, "No Columns Selected", "Please select at least one column to print.")
            return
            
        from modules.export_action import execute_export_action
        from modules.print_module import generate_address_list_pdf
        excel_cols = [(header, key) for header, key in self.field_definitions if key in selected_cols]
        execute_export_action(
            parent_widget=self,
            records=checked,
            pdf_suffix="AddressList",
            pdf_generator_func=lambda path: generate_address_list_pdf(checked, path, selected_cols),
            excel_columns=excel_cols
        )
        self._cancel_selection_mode()'''
c = c.replace(old4, new4)

# 5. _print_list
old5 = '''    def _print_list(self):
        checked = self._get_checked_records()
        records = checked if checked else (
            [self._selected_record] if self._selected_record else self._records
        )
        if not records:
            show_info(self, "No Records", LABELS["no_records"])
            return
            
        dlg = ColumnSelectionDialog(self)
        if dlg.exec() != QDialog.Accepted:
            return
            
        selected_cols = dlg.get_selected_columns()
        if not selected_cols:
            show_warning(self, "No Columns Selected / कोई कॉलम नहीं चुना गया", "Please select at least one column to print.")
            return
            
        path = self._get_print_path("AddressList")
        if not path:
            return
            
        from modules.print_module import generate_address_list_pdf
        ok, result = generate_address_list_pdf(records, path, selected_cols)
        if ok:
            show_info(self, "PDF Generated / PDF बना", LABELS["print_success"])
            open_pdf(path)
        else:
            show_error(self, "Print Error / प्रिंट त्रुटि", result)'''
new5 = '''    def _print_list(self):
        checked = self._get_checked_records()
        records = checked if checked else (
            [self._selected_record] if self._selected_record else self._records
        )
        if not records:
            show_info(self, "No Records", LABELS["no_records"])
            return
            
        dlg = ColumnSelectionDialog(self)
        if dlg.exec() != QDialog.Accepted:
            return
            
        selected_cols = dlg.get_selected_columns()
        if not selected_cols:
            show_warning(self, "No Columns Selected / कोई कॉलम नहीं चुना गया", "Please select at least one column to print.")
            return
            
        from modules.export_action import execute_export_action
        from modules.print_module import generate_address_list_pdf
        excel_cols = [(header, key) for header, key in self.field_definitions if key in selected_cols]
        execute_export_action(
            parent_widget=self,
            records=records,
            pdf_suffix="AddressList",
            pdf_generator_func=lambda path: generate_address_list_pdf(records, path, selected_cols),
            excel_columns=excel_cols
        )'''
c = c.replace(old5, new5)

# 6. _print_dept
old6 = '''    def _print_dept(self):
        dept_id = self.dept_filter.currentData()
        dept_name = self.dept_filter.currentText()
        if not dept_id:
            show_warning(self, "Select Department / विभाग चुनें",
                         "Please select a specific department first.\\nकृपया पहले एक विभाग चुनें।")
            return
        records = get_all_addresses(dept_id=dept_id)
        if not records:
            show_info(self, "No Records", LABELS["no_records"])
            return
        path = self._get_print_path(f"Dept_{dept_name.split('(')[0].strip()}")
        if not path:
            return
        ok, result = generate_department_list_pdf(records, dept_name, path)
        if ok:
            show_info(self, "PDF Generated / PDF बना", LABELS["print_success"])
            open_pdf(path)
        else:
            show_error(self, "Print Error / प्रिंट त्रुटि", result)'''
new6 = '''    def _print_dept(self):
        dept_id = self.dept_filter.currentData()
        dept_name = self.dept_filter.currentText()
        if not dept_id:
            show_warning(self, "Select Department / विभाग चुनें",
                         "Please select a specific department first.\\nकृपया पहले एक विभाग चुनें।")
            return
        records = get_all_addresses(dept_id=dept_id)
        if not records:
            show_info(self, "No Records", LABELS["no_records"])
            return
            
        from modules.export_action import execute_export_action
        from modules.print_module import generate_department_list_pdf
        excel_cols = [(header, key) for header, key in self.field_definitions if key not in ("select", "actions", "id")]
        execute_export_action(
            parent_widget=self,
            records=records,
            pdf_suffix=f"Dept_{dept_name.split('(')[0].strip()}",
            pdf_generator_func=lambda path: generate_department_list_pdf(records, dept_name, path),
            excel_columns=excel_cols
        )'''
c = c.replace(old6, new6)

# 7. _print_all
old7 = '''    def _print_all(self):
        records = get_all_addresses()
        if not records:
            show_info(self, "No Records", LABELS["no_records"])
            return
        path = self._get_print_path("FullDirectory")
        if not path:
            return
        ok, result = generate_full_directory_pdf(records, path)
        if ok:
            show_info(self, "PDF Generated / PDF बना", LABELS["print_success"])
            open_pdf(path)
        else:
            show_error(self, "Print Error / प्रिंट त्रुटि", result)'''
new7 = '''    def _print_all(self):
        records = get_all_addresses()
        if not records:
            show_info(self, "No Records", LABELS["no_records"])
            return
            
        from modules.export_action import execute_export_action
        from modules.print_module import generate_full_directory_pdf
        excel_cols = [(header, key) for header, key in self.field_definitions if key not in ("select", "actions", "id")]
        execute_export_action(
            parent_widget=self,
            records=records,
            pdf_suffix="FullDirectory",
            pdf_generator_func=lambda path: generate_full_directory_pdf(records, path),
            excel_columns=excel_cols
        )'''
c = c.replace(old7, new7)

with open('ui/address_view.py', 'w', encoding='utf-8') as f:
    f.write(c)

print("Updated address_view.py with execute_export_action hooks")
