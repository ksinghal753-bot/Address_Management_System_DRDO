import os
import tempfile
from PySide6.QtWidgets import (
    QDialog, QFileDialog, QMessageBox, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QFrame
)
from PySide6.QtPrintSupport import QPrintDialog, QPrinter, QPrinterInfo
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

# Virtual/software printer names – not real physical printers
_VIRTUAL_PRINTER_KEYWORDS = [
    "microsoft print to pdf", "microsoft xps", "onenote", "fax",
    "adobe pdf", "cutepdf", "dopdf", "bullzip", "foxit", "pdfcreator",
    "pdf24", "nitro", "print to pdf", "xps document writer", "snagit",
]


def _get_real_printers():
    """Returns QPrinterInfo objects that are real physical printers."""
    return [
        p for p in QPrinterInfo.availablePrinters()
        if not any(kw in p.printerName().lower() for kw in _VIRTUAL_PRINTER_KEYWORDS)
    ]


def _open_printer_settings():
    """Opens Windows Printers & Scanners settings."""
    import subprocess
    try:
        subprocess.Popen(["control", "printers"])
    except Exception:
        try:
            os.system("start ms-settings:printers")
        except Exception:
            pass


def _show_no_printer_dialog(parent):
    """Admin-facing dialog shown when no physical printer is detected."""
    dlg = QDialog(parent)
    dlg.setWindowTitle("No Printer Found")
    dlg.setFixedWidth(490)
    dlg.setStyleSheet(
        "QDialog { background-color: #FFFFFF; color: #212529; }"
        "QLabel { color: #212529; }"
        "QPushButton { border-radius: 6px; padding: 8px 20px;"
        " font-size: 13px; font-weight: bold; }"
    )

    layout = QVBoxLayout(dlg)
    layout.setSpacing(16)
    layout.setContentsMargins(28, 28, 28, 24)

    # Title row
    title_row = QHBoxLayout()
    icon_lbl = QLabel("\U0001f5a8\ufe0f")
    icon_lbl.setFont(QFont("Segoe UI Emoji", 26))
    icon_lbl.setFixedWidth(44)
    title_row.addWidget(icon_lbl)

    title_lbl = QLabel("No Physical Printer Detected")
    title_lbl.setFont(QFont("Segoe UI", 14, QFont.Bold))
    title_lbl.setStyleSheet("color: #B91C1C;")
    title_row.addWidget(title_lbl)
    title_row.addStretch()
    layout.addLayout(title_row)

    sep = QFrame()
    sep.setFrameShape(QFrame.HLine)
    sep.setStyleSheet("color: #E5E7EB;")
    layout.addWidget(sep)

    msg = QLabel(
        "No real physical printer is connected to this system.\n"
        "Only virtual printers (PDF, OneNote, Fax, XPS) were found.\n\n"
        "\U0001f46e\u200d\u2642\ufe0f  Admin Action Required:\n"
        "Please install a printer driver and connect the printer\n"
        "before using the Print Directly option.\n\n"
        "Steps to add a printer:\n"
        "  1. Open  Settings \u2192 Bluetooth & devices \u2192 Printers & scanners\n"
        "  2. Click  'Add a printer or scanner'\n"
        "  3. Select your printer and install the driver\n"
        "  4. Restart this application and try again."
    )
    msg.setFont(QFont("Segoe UI", 10))
    msg.setStyleSheet("color: #374151;")
    msg.setWordWrap(True)
    layout.addWidget(msg)

    # Buttons
    btn_row = QHBoxLayout()
    btn_row.addStretch()

    btn_settings = QPushButton("\u2699\ufe0f  Open Printer Settings")
    btn_settings.setStyleSheet(
        "QPushButton { background-color: #1D4ED8; color: white; border: none; }"
        "QPushButton:hover { background-color: #1E40AF; }"
    )
    btn_settings.setCursor(Qt.PointingHandCursor)
    btn_settings.clicked.connect(_open_printer_settings)

    btn_close = QPushButton("Close")
    btn_close.setStyleSheet(
        "QPushButton { background-color: #F3F4F6; color: #374151;"
        " border: 1px solid #D1D5DB; }"
        "QPushButton:hover { background-color: #E5E7EB; }"
    )
    btn_close.setCursor(Qt.PointingHandCursor)
    btn_close.clicked.connect(dlg.accept)

    btn_row.addWidget(btn_settings)
    btn_row.addSpacing(10)
    btn_row.addWidget(btn_close)
    layout.addLayout(btn_row)

    dlg.exec()


def execute_export_action(
    parent_widget,
    records,
    pdf_suffix,
    pdf_generator_func,
    allow_excel=True,
    excel_columns=None,
    is_envelope_or_label=False
):
    from ui.export_format_dialog import ExportFormatDialog
    from ui.shared_widgets import show_info, show_error, show_warning
    from modules.print_module import open_pdf

    dlg = ExportFormatDialog(parent_widget, allow_excel=not is_envelope_or_label)
    if dlg.exec() != QDialog.Accepted:
        return

    opt = dlg.selected_option

    if opt == "pdf":
        path = parent_widget._get_print_path(pdf_suffix)
        if not path:
            return
        ok, result = pdf_generator_func(path)
        if ok:
            show_info(parent_widget, "PDF Generated", "PDF has been generated successfully.")
            open_pdf(path)
        else:
            show_error(parent_widget, "Print Error", result)

    elif opt == "excel":
        if not allow_excel or is_envelope_or_label:
            show_warning(parent_widget, "Excel Export",
                         "Excel export is available only for list-based reports.")
            return
        if not excel_columns:
            excel_columns = [
                ("No", "id"), ("Dept", "dept_name"), ("To", "to_field"),
                ("Designation", "designation"), ("Office", "office_name"),
                ("City", "city"), ("State", "state"), ("PIN Code", "pin_code")
            ]

        path, _ = QFileDialog.getSaveFileName(
            parent_widget, "Save Excel / \u090f\u0915\u094d\u0938\u0947\u0932 \u0938\u0939\u0947\u091c\u0947\u0902",
            parent_widget._get_print_path(pdf_suffix, default_ext=".xlsx", no_dialog=True)
            if hasattr(parent_widget, '_get_print_path') else "",
            "Excel Files (*.xlsx)"
        )
        if not path:
            return

        from modules.excel_export import export_to_excel
        ok, result = export_to_excel(records, path, excel_columns)
        if ok:
            show_info(parent_widget, "Excel Generated",
                      "Excel file has been generated successfully.")
            import platform, subprocess
            if platform.system() == 'Windows':
                os.startfile(path)
            elif platform.system() == 'Darwin':
                subprocess.call(('open', path))
            else:
                subprocess.call(('xdg-open', path))
        else:
            show_error(parent_widget, "Export Error", result)

    elif opt == "direct":
        # (Moved printer check to after the preview)

        # ── Generate temporary PDF ───────────────────────────────────────
        fd, temp_path = tempfile.mkstemp(suffix=".pdf")
        os.close(fd)

        try:
            ok, result = pdf_generator_func(temp_path)
            if not ok:
                show_error(parent_widget, "Generation Error", result)
                return

            # ── Envelope Preview before printing ──
            html_preview_doc = None
            if is_envelope_or_label and len(records) == 1 and hasattr(parent_widget, "_get_preview_html"):
                from ui.address_view import ZoomablePreview
                html = parent_widget._get_preview_html(records[0], is_dialog=True)
                preview_dlg = QDialog(parent_widget)
                preview_dlg.setWindowTitle("Print Preview / प्रिंट पूर्वावलोकन")
                preview_dlg.resize(850, 480)
                lay = QVBoxLayout(preview_dlg)
                preview_text = ZoomablePreview(html)
                preview_text.setStyleSheet("QGraphicsView { border: 1px solid #CCCCCC; border-radius: 8px; }")
                lay.addWidget(preview_text, stretch=1)
                
                btn_box = QHBoxLayout()
                btn_box.addStretch()
                proceed_btn = QPushButton("Proceed to Print / प्रिंट करने के लिए आगे बढ़ें")
                proceed_btn.setStyleSheet("background-color: #7A1212; color: white; padding: 6px 16px; font-weight: bold; border-radius: 4px;")
                proceed_btn.clicked.connect(preview_dlg.accept)
                cancel_btn = QPushButton("Cancel / रद्द करें")
                cancel_btn.clicked.connect(preview_dlg.reject)
                btn_box.addWidget(proceed_btn)
                btn_box.addWidget(cancel_btn)
                lay.addLayout(btn_box)
                
                if preview_dlg.exec() != QDialog.Accepted:
                    return
                html_preview_doc = preview_text.text_doc

            # ── Check for a real physical printer first ──────────────────────
            real_printers = _get_real_printers()
            if not real_printers:
                _show_no_printer_dialog(parent_widget)
                return

            from modules.direct_print import print_pdf_directly
            printer = QPrinter(QPrinter.HighResolution)
            printer.setColorMode(QPrinter.Color)
            printer.setDuplex(QPrinter.DuplexNone)
            pdlg = QPrintDialog(printer, parent_widget)
            pdlg.setWindowTitle("Select Printer / प्रिंटर चुनें")
            pdlg.setStyleSheet(
                "QDialog { background-color: #FFFFFF; color: #000000; }"
                "QLabel { color: #000000; }"
                "QPushButton { background-color: #F0F0F0; color: #000000;"
                " border: 1px solid #CCCCCC; padding: 4px 12px; }"
                "QPushButton:hover { background-color: #E0E0E0; }"
                "QComboBox { background-color: #FFFFFF; color: #000000; }"
                "QGroupBox { color: #000000; }"
            )
            
            if pdlg.exec() == QDialog.Accepted:
                if html_preview_doc:
                    from PySide6.QtGui import QPageLayout
                    printer.setPageOrientation(QPageLayout.Orientation.Landscape)
                    html_preview_doc.print_(printer)
                    pok = True
                else:
                    pok, presult = print_pdf_directly(temp_path, printer)
                    if not pok:
                        show_error(parent_widget, "Print Error", presult)
            else:
                from PySide6.QtWidgets import QMessageBox
                reply = QMessageBox.question(
                    parent_widget,
                    "Default Printer",
                    "No printer was selected. Do you want to print to the default system printer?",
                    QMessageBox.Yes | QMessageBox.No
                )
                if reply == QMessageBox.Yes:
                    default_printer_info = QPrinterInfo.defaultPrinter()
                    if default_printer_info.isNull():
                        show_error(parent_widget, "Print Error", "No default printer found on this system.")
                    else:
                        printer.setPrinterName(default_printer_info.printerName())
                        if html_preview_doc:
                            from PySide6.QtGui import QPageLayout
                            printer.setPageOrientation(QPageLayout.Orientation.Landscape)
                            html_preview_doc.print_(printer)
                            pok = True
                        else:
                            pok, presult = print_pdf_directly(temp_path, printer)
                            if not pok:
                                show_error(parent_widget, "Print Error", presult)
        finally:
            # Delay deletion so ShellExecute can finish reading the file
            import threading

            def _delayed_remove(path):
                import time
                time.sleep(6)
                try:
                    os.remove(path)
                except Exception:
                    pass

            if os.path.exists(temp_path):
                threading.Thread(
                    target=_delayed_remove, args=(temp_path,), daemon=True
                ).start()
