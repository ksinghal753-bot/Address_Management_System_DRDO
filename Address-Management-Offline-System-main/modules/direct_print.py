import os
import time

def get_default_printer() -> str:
    """Returns the name of the current default Windows printer."""
    try:
        import ctypes
        import ctypes.wintypes
        buffer_size = ctypes.wintypes.DWORD(256)
        buffer = ctypes.create_unicode_buffer(256)
        ctypes.WinDLL('winspool.drv').GetDefaultPrinterW(buffer, ctypes.byref(buffer_size))
        return buffer.value
    except Exception:
        return ""

def set_default_printer(printer_name: str) -> bool:
    """Temporarily sets the default Windows printer."""
    try:
        import ctypes
        if not printer_name:
            return False
        return bool(ctypes.WinDLL('winspool.drv').SetDefaultPrinterW(printer_name))
    except Exception:
        return False

def print_pdf_directly(pdf_path: str, printer) -> tuple[bool, str]:
    """
    Renders a PDF file using QPdfDocument and paints it directly to the given QPrinter.
    This bypasses any external PDF viewer and uses PySide's native printing system.
    """
    try:
        from PySide6.QtPdf import QPdfDocument
        from PySide6.QtGui import QPainter
        from PySide6.QtCore import QSize
        
        doc = QPdfDocument()
        doc.load(pdf_path)
        if doc.status() != QPdfDocument.Status.Ready:
            return False, f"Failed to load PDF, status: {doc.status()}"
            
        painter = QPainter()
        if not painter.begin(printer):
            return False, "Failed to start printing: QPainter begin failed."
            
        try:
            page_layout = printer.pageLayout()
            paint_rect_pixels = page_layout.paintRectPixels(printer.resolution())
            
            for i in range(doc.pageCount()):
                if i > 0:
                    printer.newPage()
                    
                pdf_size_points = doc.pageSize(i)
                
                target_w = paint_rect_pixels.width()
                target_h = paint_rect_pixels.height()
                
                pdf_w = pdf_size_points.width()
                pdf_h = pdf_size_points.height()
                
                scale_w = target_w / pdf_w
                scale_h = target_h / pdf_h
                scale = min(scale_w, scale_h)
                
                render_w = int(pdf_w * scale)
                render_h = int(pdf_h * scale)
                
                img = doc.render(i, QSize(render_w, render_h))
                
                x = (target_w - render_w) // 2
                y = (target_h - render_h) // 2
                
                painter.drawImage(x, y, img)
        finally:
            painter.end()
            
        return True, "Printed successfully."
    except Exception as e:
        return False, str(e)
