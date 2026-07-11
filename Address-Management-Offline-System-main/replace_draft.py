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
        sg.setSpacing(4)
        sg.setContentsMargins(10, 4, 10, 6)

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

        # SP selector in preview panel
        sp_row = QHBoxLayout()
        sp_lbl = QLabel("By S/P / डाक प्रकार:")
        sp_lbl.setObjectName("fieldLabel")
        self.preview_sp = QComboBox()
        self.preview_sp.addItems(DELIVERY_TYPES)
        self.preview_sp.currentIndexChanged.connect(self._update_preview)
        sp_row.addWidget(sp_lbl)
        sp_row.addWidget(self.preview_sp)
        sp_row.addStretch()
        right_vbox.addLayout(sp_row)

        # Date picker for print
        date_row = QHBoxLayout()
        date_print_lbl = QLabel("Print Date / प्रिंट दिनांक:")
        date_print_lbl.setObjectName("fieldLabel")
        self.preview_date = QDateEdit()
        self.preview_date.setCalendarPopup(True)
        self.preview_date.setDate(QDate.currentDate())
        self.preview_date.setDisplayFormat("dd-MM-yyyy")
        self.preview_date.dateChanged.connect(self._update_preview)

        self.preview_open_btn = QPushButton("👁️ Open / खोलें")
        self.preview_open_btn.setObjectName("secondaryButton")
        self.preview_open_btn.setEnabled(False)
        self.preview_open_btn.clicked.connect(self._open_envelope_preview_dialog)

        self.preview_print_btn = QPushButton("🖨️ Print Envelope / प्रिंट करें")
        self.preview_print_btn.setObjectName("primaryPrintButton")
        self.preview_print_btn.setEnabled(False)
        self.preview_print_btn.clicked.connect(self._print_single)

        date_row.addWidget(date_print_lbl)
        date_row.addWidget(self.preview_date)
        date_row.addSpacing(8)
        date_row.addWidget(self.preview_open_btn)
        date_row.addSpacing(8)
        date_row.addWidget(self.preview_print_btn)
        date_row.addStretch()
        right_vbox.addLayout(date_row)

        top_layout.addWidget(right_widget, stretch=1)
        root.addLayout(top_layout)

        # ── Bottom Section (Table + Actions) ──────────────────────────────────
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

        # Record action buttons (below table)
        action_row = QHBoxLayout()
        action_row.setSpacing(8)

        self.view_btn = QPushButton("👁️ View / देखें")
        self.view_btn.setObjectName("secondaryButton")
        self.view_btn.setEnabled(False)
        self.view_btn.clicked.connect(self._view_selected)

        self.print_btn = QPushButton("🖨️ Print Options / प्रिंट विकल्प")
        self.print_btn.setObjectName("primaryPrintButton")
        self.print_btn.clicked.connect(self._show_print_dialog)

        action_row.addWidget(self.view_btn)

        if self.role == "admin":
            self.edit_btn = QPushButton("✏️ " + LABELS["edit"])
            self.edit_btn.setObjectName("secondaryButton")
            self.edit_btn.setEnabled(False)
            self.edit_btn.clicked.connect(self._edit_selected)

            self.del_btn = QPushButton("🗑️ " + LABELS["delete"])
            self.del_btn.setObjectName("dangerDeleteButton")
            self.del_btn.setEnabled(False)
            self.del_btn.clicked.connect(self._delete_selected)

            action_row.addWidget(self.edit_btn)
            action_row.addWidget(self.del_btn)

        action_row.addWidget(self.print_btn)

        bottom_vbox.addLayout(action_row)
        root.addWidget(bottom_widget, stretch=1)
