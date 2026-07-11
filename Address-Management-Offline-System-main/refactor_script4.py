import sys

with open('ui/address_view.py', 'r', encoding='utf-8') as f:
    content = f.read()

target_content = """        # ── Top Splitter (Search / Preview) ───────────────────────────────────
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

        header_row = QHBoxLayout()
        prev_title = SectionTitle("Envelope Preview / लिफाफा पूर्वावलोकन")
        
        self.preview_open_btn = QPushButton("👁️ Open / खोलें")
        self.preview_open_btn.setObjectName("secondaryButton")
        self.preview_open_btn.setEnabled(False)
        self.preview_open_btn.clicked.connect(self._open_envelope_preview_dialog)
        
        header_row.addWidget(prev_title)
        header_row.addStretch()
        header_row.addWidget(self.preview_open_btn)
        
        right_vbox.addLayout(header_row)
        right_vbox.addWidget(HLine())

        self.envelope_preview = QTextEdit()
        self.envelope_preview.setReadOnly(True)
        self.envelope_preview.setObjectName("envelopePreview")
        self.envelope_preview.setFont(QFont("Courier New", 11))
        right_vbox.addWidget(self.envelope_preview, stretch=1)

        top_layout.addWidget(right_widget, stretch=1)
        root.addLayout(top_layout)"""

replacement_content = """        # ── Top Splitter (Search / Preview) ───────────────────────────────────
        top_layout = QHBoxLayout()
        # Set only 12px vertical gap under the toolbar
        top_layout.setContentsMargins(12, 12, 12, 0)
        top_layout.setSpacing(12)

        # Left: Search panel (Using QWidget instead of QGroupBox to remove large white space)
        search_widget = QWidget()
        search_widget.setObjectName("addressViewSearch")
        search_widget.setStyleSheet(f"#addressViewSearch {{ background-color: {COLORS['surface']}; border: 1.5px solid {COLORS['border']}; border-radius: 12px; }}")
        search_vbox = QVBoxLayout(search_widget)
        search_vbox.setContentsMargins(12, 12, 12, 12)
        search_vbox.setSpacing(8)

        # Left header
        search_header = QHBoxLayout()
        search_title = SectionTitle("Search / खोजें")
        search_header.addWidget(search_title)
        search_header.addStretch()
        search_vbox.addLayout(search_header)
        search_vbox.addWidget(HLine())

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

        search_vbox.addLayout(top_actions)
        search_vbox.addWidget(HLine())

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

        search_vbox.addLayout(row1)
        search_vbox.addStretch(1)

        top_layout.addWidget(search_widget, stretch=1)

        # Right: envelope preview
        right_widget = QWidget()
        right_widget.setObjectName("addressViewRight")
        right_widget.setStyleSheet(f"#addressViewRight {{ background-color: {COLORS['surface']}; border: 1.5px solid {COLORS['border']}; border-radius: 12px; }}")
        right_vbox = QVBoxLayout(right_widget)
        right_vbox.setContentsMargins(12, 12, 12, 12)
        right_vbox.setSpacing(8)

        header_row = QHBoxLayout()
        prev_title = SectionTitle("Envelope Preview / लिफाफा पूर्वावलोकन")
        
        self.preview_open_btn = QPushButton("👁️ Open / खोलें")
        self.preview_open_btn.setObjectName("secondaryButton")
        self.preview_open_btn.setEnabled(False)
        self.preview_open_btn.clicked.connect(self._open_envelope_preview_dialog)
        
        header_row.addWidget(prev_title)
        header_row.addStretch()
        header_row.addWidget(self.preview_open_btn)
        
        right_vbox.addLayout(header_row)
        right_vbox.addWidget(HLine())

        self.envelope_preview = QTextEdit()
        self.envelope_preview.setReadOnly(True)
        self.envelope_preview.setObjectName("envelopePreview")
        self.envelope_preview.setFont(QFont("Courier New", 11))
        # Remove default border since parent now has it
        self.envelope_preview.setStyleSheet("border: none; background: transparent;")
        right_vbox.addWidget(self.envelope_preview, stretch=1)

        top_layout.addWidget(right_widget, stretch=1)
        root.addLayout(top_layout)"""

if target_content in content:
    content = content.replace(target_content, replacement_content)
    with open('ui/address_view.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Success")
else:
    print("Target content not found!")
