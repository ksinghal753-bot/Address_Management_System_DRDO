import sys

with open('ui/address_view.py', 'r', encoding='utf-8') as f:
    content = f.read()

new_build_ui = '''        # ── Toolbar ───────────────────────────────────────────────────────────
        toolbar = QWidget()
        toolbar.setStyleSheet(f"background: {COLORS['primary_dark']}; padding: 4px 12px;")
        tl = QHBoxLayout(toolbar)
        tl.setContentsMargins(10, 6, 10, 6)
        tl.setSpacing(10)

        title = QLabel("📋  Address Records / पता अभिलेख")
        title.setStyleSheet("color: white; font-size: 14px; font-weight: bold;")
        tl.addWidget(title)
        tl.addStretch()

        # Stats label
        self.stats_lbl = QLabel("")
        self.stats_lbl.setStyleSheet(f"color: {COLORS['accent_light']}; font-size: 12px;")
        tl.addWidget(self.stats_lbl)

        back_btn = QPushButton("← " + LABELS["return"])
        back_btn.clicked.connect(self.go_back.emit)
        tl.addWidget(back_btn)

        root.addWidget(toolbar)

        # ── Top Splitter (Search / Preview) ───────────────────────────────────
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
        sg.setContentsMargins(10, 8, 10, 6)

        # Top Action Row inside Search Panel
        top_actions = QHBoxLayout()
        top_actions.setSpacing(8)

        if self.role == "admin":
            self.add_btn = QPushButton("➕ " + LABELS["add"])
            self.add_btn.setObjectName("successButton")
            self.add_btn.clicked.connect(self.add_new.emit)
            top_actions.addWidget(self.add_btn)

            self.edit_btn = QPushButton("✏️ " + LABELS["edit"])
            self.edit_btn.setObjectName("secondaryButton")
            self.edit_btn.setEnabled(False)
            self.edit_btn.clicked.connect(self._edit_selected)
            top_actions.addWidget(self.edit_btn)

            self.del_btn = QPushButton("🗑️ " + LABELS["delete"])
            self.del_btn.setObjectName("dangerDeleteButton")
            self.del_btn.setEnabled(False)
            self.del_btn.clicked.connect(self._delete_selected)
            top_actions.addWidget(self.del_btn)

        self.view_btn = QPushButton("👁️ View / देखें")
        self.view_btn.setObjectName("secondaryButton")
        self.view_btn.setEnabled(False)
        self.view_btn.clicked.connect(self._view_selected)
        top_actions.addWidget(self.view_btn)

        self.clear_sel_btn = QPushButton("🧹 Clear / साफ")
        self.clear_sel_btn.setObjectName("secondaryButton")
        self.clear_sel_btn.clicked.connect(self._clear_selection)
        top_actions.addWidget(self.clear_sel_btn)
        
        self.print_btn = QPushButton("🖨️ Print / प्रिंट")
        self.print_btn.setObjectName("primaryPrintButton")
        self.print_btn.clicked.connect(self._show_print_dialog)
        top_actions.addWidget(self.print_btn)

        top_actions.addStretch()

        sg.addLayout(top_actions)
        sg.addWidget(HLine())

        row1 = QHBoxLayout()
        # Department filter
        dept_lbl = QLabel("Dept:")
        dept_lbl.setObjectName("fieldLabel")
        self.dept_filter = QComboBox()
        self.dept_filter.setMinimumWidth(160)
        self._load_dept_filter()

        # PARA filter
        para_lbl = QLabel("PARA:")
        para_lbl.setObjectName("fieldLabel")
        self.para_filter = QComboBox()
        self.para_filter.addItem("All / सभी", None)
        for p in PARA_OPTIONS:
            self.para_filter.addItem(p)

        row1.addWidget(dept_lbl)
        row1.addWidget(self.dept_filter)
        row1.addSpacing(10)
        row1.addWidget(para_lbl)
        row1.addWidget(self.para_filter)
        row1.addStretch()

        row2 = QHBoxLayout()
        # Keyword search
        kw_lbl = QLabel("Keyword:")
        kw_lbl.setObjectName("fieldLabel")
        self.keyword_input = QLineEdit()
        self.keyword_input.setPlaceholderText("Office, City, Name... / कार्यालय, शहर, नाम...")
        self.keyword_input.setMinimumWidth(200)
        self.keyword_input.returnPressed.connect(self._do_search)

        # City filter
        city_lbl = QLabel("City / PIN:")
        city_lbl.setObjectName("fieldLabel")
        self.city_filter = QLineEdit()
        self.city_filter.setPlaceholderText("City or PIN")
        self.city_filter.setMaximumWidth(120)

        # Date filter
        date_lbl = QLabel("Date:")
        date_lbl.setObjectName("fieldLabel")
        self.use_date = QCheckBox()
        self.date_filter = QDateEdit()
        self.date_filter.setCalendarPopup(True)
        self.date_filter.setDate(QDate.currentDate())
        self.date_filter.setDisplayFormat("dd-MM-yyyy")
        self.date_filter.setEnabled(False)
        self.use_date.toggled.connect(self.date_filter.setEnabled)

        row2.addWidget(kw_lbl)
        row2.addWidget(self.keyword_input)
        row2.addSpacing(8)
        row2.addWidget(city_lbl)
        row2.addWidget(self.city_filter)
        row2.addSpacing(8)
        row2.addWidget(date_lbl)
        row2.addWidget(self.use_date)
        row2.addWidget(self.date_filter)
        row2.addStretch()

        btn_row = QHBoxLayout()
        search_btn = QPushButton("🔍 " + LABELS["search"])
        search_btn.clicked.connect(self._do_search)
        clear_btn = QPushButton("✖ Clear / साफ")
        clear_btn.clicked.connect(self._clear_search)
        btn_row.addWidget(search_btn)
        btn_row.addWidget(clear_btn)
        btn_row.addStretch()

        sg.addLayout(row1)
        sg.addLayout(row2)
        sg.addLayout(btn_row)
        sg.addStretch(1)  # Push contents to top

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

start_idx = content.find('        # ── Toolbar ───────────────────────────────────────────────────────────')
end_idx = content.find('    def _load_dept_filter(self):')
if start_idx == -1 or end_idx == -1:
    print('Failed to find build_ui bounds')
    sys.exit(1)

content = content[:start_idx] + new_build_ui + '    def _load_dept_filter(self):\n' + content[end_idx + len('    def _load_dept_filter(self):\n'):]

# Add _clear_selection method right before _load_dept_filter
clear_sel_code = '''    def _clear_selection(self):
        self.table.clearSelection()

'''
content = content.replace('    def _load_dept_filter(self):', clear_sel_code + '    def _load_dept_filter(self):')

old_actions = '''    def _update_actions_state(self, enabled: bool):
        self.view_btn.setEnabled(enabled)
        self.print_btn.setEnabled(True)
        self.preview_open_btn.setEnabled(enabled)
        self.preview_print_btn.setEnabled(enabled)
        if self.role == "admin":
            self.edit_btn.setEnabled(enabled)
            self.del_btn.setEnabled(enabled)'''
            
new_actions = '''    def _update_actions_state(self, enabled: bool):
        self.view_btn.setEnabled(enabled)
        self.print_btn.setEnabled(True)
        self.preview_open_btn.setEnabled(enabled)
        if self.role == "admin":
            self.edit_btn.setEnabled(enabled)
            self.del_btn.setEnabled(enabled)'''
            
content = content.replace(old_actions, new_actions)

old_preview_update = '''        # Override SP and date from preview panel
        rec["delivery_type"] = self.preview_sp.currentText()
        rec["date_entry"]    = self.preview_date.date().toString("yyyy-MM-dd")'''
new_preview_update = '''        # Removed preview_sp and preview_date logic'''
content = content.replace(old_preview_update, new_preview_update)

old_get_record = '''    def _get_record_for_print(self, record: dict) -> dict:
        """Get record with preview panel overrides applied."""
        rec = record.copy()
        rec["delivery_type"] = self.preview_sp.currentText()
        rec["date_entry"]    = self.preview_date.date().toString("yyyy-MM-dd")
        return rec'''
new_get_record = '''    def _get_record_for_print(self, record: dict) -> dict:
        """Get record with preview panel overrides applied."""
        return record.copy()'''
content = content.replace(old_get_record, new_get_record)

with open('ui/address_view.py', 'w', encoding='utf-8') as f:
    f.write(content)
print('Script completed successfully.')
