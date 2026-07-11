import sys

with open('ui/address_view.py', 'r', encoding='utf-8') as f:
    content = f.read()

new_build_ui = '''        # ── Top Splitter (Search / Preview) ───────────────────────────────────
        top_layout = QHBoxLayout()
        top_layout.setContentsMargins(12, 6, 12, 0)
        top_layout.setSpacing(12)

        # Left: Search panel
        search_widget = QWidget()
        search_widget.setObjectName("addressViewSearch")
        search_widget.setStyleSheet(f"#addressViewSearch {{ background-color: {COLORS['surface']}; }}")
        search_vbox = QVBoxLayout(search_widget)
        search_vbox.setContentsMargins(0, 0, 0, 0)

        search_group = QGroupBox("Search / खोजें")
        search_group.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sg = QVBoxLayout(search_group)
        sg.setSpacing(8)
        sg.setContentsMargins(8, 8, 8, 6)

        # Action Grid for compactness
        top_actions = QGridLayout()
        top_actions.setSpacing(6)

        row_idx = 0
        col_idx = 0

        if self.role == "admin":
            self.add_btn = QPushButton("➕ Add Address")
            self.add_btn.setObjectName("successButton")
            self.add_btn.clicked.connect(self.add_new.emit)
            top_actions.addWidget(self.add_btn, row_idx, col_idx)
            col_idx += 1

            self.edit_btn = QPushButton("✏️ Edit Address")
            self.edit_btn.setObjectName("secondaryButton")
            self.edit_btn.setEnabled(False)
            self.edit_btn.clicked.connect(self._edit_selected)
            top_actions.addWidget(self.edit_btn, row_idx, col_idx)
            col_idx += 1

            self.del_btn = QPushButton("🗑️ Delete")
            self.del_btn.setObjectName("dangerDeleteButton")
            self.del_btn.setEnabled(False)
            self.del_btn.clicked.connect(self._delete_selected)
            top_actions.addWidget(self.del_btn, row_idx, col_idx)
            
            row_idx += 1
            col_idx = 0

        self.view_btn = QPushButton("👁️ View")
        self.view_btn.setObjectName("secondaryButton")
        self.view_btn.setEnabled(False)
        self.view_btn.clicked.connect(self._view_selected)
        top_actions.addWidget(self.view_btn, row_idx, col_idx)
        col_idx += 1

        self.clear_sel_btn = QPushButton("🧹 Clear")
        self.clear_sel_btn.setObjectName("secondaryButton")
        self.clear_sel_btn.clicked.connect(self._clear_selection)
        top_actions.addWidget(self.clear_sel_btn, row_idx, col_idx)
        col_idx += 1

        self.print_btn = QPushButton("🖨️ Print")
        self.print_btn.setObjectName("primaryPrintButton")
        self.print_btn.clicked.connect(self._show_print_dialog)
        top_actions.addWidget(self.print_btn, row_idx, col_idx)

        sg.addLayout(top_actions)
        sg.addWidget(HLine())

        row1 = QHBoxLayout()
        row1.setSpacing(6)
        
        dept_lbl = QLabel("Dept:")
        dept_lbl.setObjectName("fieldLabel")
        self.dept_filter = QComboBox()
        self.dept_filter.setMinimumWidth(120)
        self.dept_filter.currentIndexChanged.connect(self._do_search)
        self._load_dept_filter()

        para_lbl = QLabel("PARA:")
        para_lbl.setObjectName("fieldLabel")
        self.para_filter = QComboBox()
        self.para_filter.setMinimumWidth(80)
        self.para_filter.addItem("All", None)
        for p in PARA_OPTIONS:
            self.para_filter.addItem(p)
        self.para_filter.currentIndexChanged.connect(self._do_search)

        row1.addWidget(dept_lbl)
        row1.addWidget(self.dept_filter, stretch=1)
        row1.addWidget(para_lbl)
        row1.addWidget(self.para_filter, stretch=1)

        sg.addLayout(row1)
        sg.addStretch(1)

        search_vbox.addWidget(search_group)
        top_layout.addWidget(search_widget, stretch=1)

        # Right: envelope preview
        right_widget = QWidget()
        right_widget.setObjectName("addressViewRight")
        right_widget.setStyleSheet(f"#addressViewRight {{ background-color: {COLORS['surface']}; }}")
        right_vbox = QVBoxLayout(right_widget)
        right_vbox.setContentsMargins(12, 12, 12, 12)
        right_vbox.setSpacing(8)

        prev_title = SectionTitle("Envelope Preview / लिफाफा पूर्वावलोकन")
        right_vbox.addWidget(prev_title)
        right_vbox.addWidget(HLine())

        self.envelope_preview = QTextEdit()
        self.envelope_preview.setReadOnly(True)
        self.envelope_preview.setObjectName("envelopePreview")
        self.envelope_preview.setFont(QFont("Courier New", 11))
        right_vbox.addWidget(self.envelope_preview, stretch=1)

        # Open button at bottom right
        open_row = QHBoxLayout()
        open_row.addStretch()
        self.preview_open_btn = QPushButton("👁️ Open / खोलें")
        self.preview_open_btn.setObjectName("secondaryButton")
        self.preview_open_btn.setEnabled(False)
        self.preview_open_btn.clicked.connect(self._open_envelope_preview_dialog)
        open_row.addWidget(self.preview_open_btn)
        
        right_vbox.addLayout(open_row)

        top_layout.addWidget(right_widget, stretch=1)
        root.addLayout(top_layout)

        # ── Bottom Section (Table) ──────────────────────────────────
        bottom_widget = QWidget()
        bottom_widget.setStyleSheet(f"background-color: {COLORS['surface']};")
        bottom_vbox = QVBoxLayout(bottom_widget)
        bottom_vbox.setContentsMargins(12, 6, 12, 8)
        bottom_vbox.setSpacing(6)

        # Address table
        self.table = QTableWidget()
        self.table.setColumnCount(len(TABLE_COLUMNS))
        self.table.setHorizontalHeaderLabels([c[0] for c in TABLE_COLUMNS])
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.verticalHeader().setVisible(False)
        self.table.setSortingEnabled(True)
        self.table.itemSelectionChanged.connect(self._on_row_selected)
        self.table.doubleClicked.connect(self._on_row_double_clicked)

        # Hide ID column
        self.table.setColumnHidden(0, True)

        bottom_vbox.addWidget(self.table, stretch=1)
        root.addWidget(bottom_widget, stretch=1)
'''

start_idx = content.find('        # ── Top Splitter (Search / Preview) ───────────────────────────────────')
end_idx = content.find('    def _clear_selection(self):')
if start_idx == -1 or end_idx == -1:
    print('Failed to find build_ui bounds')
    sys.exit(1)

content = content[:start_idx] + new_build_ui + '\n' + content[end_idx:]

new_do_search = '''    def _do_search(self):
        dept_id = self.dept_filter.currentData()
        para    = self.para_filter.currentText()
        para    = para if para != "All" else ""
        
        results = search_addresses(
            dept_id=dept_id,
            para_no=para,
            keyword="",
            city="",
            pin_code="",
            date_entry=""
        )
        self._load_records(results)'''

old_do_search = '''    def _do_search(self):
        dept_id = self.dept_filter.currentData()
        para    = self.para_filter.currentText()
        para    = para if para != "All / सभी" else ""
        keyword = self.keyword_input.text().strip()
        city_pin = self.city_filter.text().strip()
        date_str = ""
        if self.use_date.isChecked():
            date_str = self.date_filter.date().toString("yyyy-MM-dd")

        city = city_pin if not city_pin.isdigit() else ""
        pin  = city_pin if city_pin.isdigit() else ""

        results = search_addresses(
            dept_id=dept_id,
            para_no=para,
            keyword=keyword,
            city=city,
            pin_code=pin,
            date_entry=date_str
        )
        self._load_records(results)'''

content = content.replace(old_do_search, new_do_search)

old_clear_search = '''    def _clear_search(self):
        self.dept_filter.setCurrentIndex(0)
        self.para_filter.setCurrentIndex(0)
        self.keyword_input.clear()
        self.city_filter.clear()
        self.use_date.setChecked(False)
        self._load_records()'''
new_clear_search = '''    def _clear_search(self):
        self.dept_filter.blockSignals(True)
        self.para_filter.blockSignals(True)
        self.dept_filter.setCurrentIndex(0)
        self.para_filter.setCurrentIndex(0)
        self.dept_filter.blockSignals(False)
        self.para_filter.blockSignals(False)
        self._load_records()'''

content = content.replace(old_clear_search, new_clear_search)

# Make sure "All Departments / सभी विभाग" is in load_dept_filter if we removed it? No we didn't remove it from load_dept_filter. But we need to make sure the "All" logic in _do_search is correct for it.
# wait, dept is handled by currentData() which returns None for All Departments, so that's fine.

with open('ui/address_view.py', 'w', encoding='utf-8') as f:
    f.write(content)
print('Script 2 completed successfully.')
