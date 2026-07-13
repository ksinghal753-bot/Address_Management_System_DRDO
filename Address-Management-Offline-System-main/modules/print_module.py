"""
Print module: ReportLab PDF generation for address envelopes.
Email, FAX No., and Contact No. are NEVER included in any printout.
"""

import os
import subprocess
import sys
import re
from datetime import datetime
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import cm, mm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph as RLParagraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak, Image
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT

from utils.constants import ENVELOPE_PREFIX


# ── Font Registration ──────────────────────────────────────────────────────────
def _register_fonts():
    """Register a font that supports Devanagari (Hindi) for text rendering."""
    windir = os.environ.get('SystemRoot', os.environ.get('WINDIR', 'C:\\Windows'))
    fonts_dir = os.path.join(windir, 'Fonts')
    
    # 1. Register Arial
    arial_path = os.path.join(fonts_dir, 'arial.ttf')
    arialbd_path = os.path.join(fonts_dir, 'arialbd.ttf')
    if os.path.exists(arial_path):
        try:
            pdfmetrics.registerFont(TTFont('Arial', arial_path))
        except Exception:
            pass
    if os.path.exists(arialbd_path):
        try:
            pdfmetrics.registerFont(TTFont('Arial-Bold', arialbd_path))
        except Exception:
            pass
            
    # 2. Register Mangal (or fallback to system Nirmala)
    mangal_path = os.path.join(fonts_dir, 'mangal.ttf')
    nirmala_path = os.path.join(fonts_dir, 'Nirmala.ttf')
    nirmalab_path = os.path.join(fonts_dir, 'NirmalaB.ttf')
    
    mangal_registered = False
    if os.path.exists(mangal_path):
        try:
            pdfmetrics.registerFont(TTFont('Mangal', mangal_path))
            pdfmetrics.registerFont(TTFont('Mangal-Bold', mangal_path))
            mangal_registered = True
        except Exception:
            pass
            
    if not mangal_registered:
        # Fallback to Nirmala and register under 'Mangal' and 'Mangal-Bold' names
        if os.path.exists(nirmala_path):
            try:
                pdfmetrics.registerFont(TTFont('Mangal', nirmala_path))
            except Exception:
                pass
        if os.path.exists(nirmalab_path):
            try:
                pdfmetrics.registerFont(TTFont('Mangal-Bold', nirmalab_path))
            except Exception:
                pass

    # Fallback paths for HindiFont
    font_paths = [
        os.path.join(os.path.dirname(__file__), '..', 'assets', 'fonts',
                     'NotoSansDevanagari-Regular.ttf'),
        r"C:\Windows\Fonts\ARIALUNI.TTF",
        r"C:\Windows\Fonts\mangal.ttf",
        r"C:\Windows\Fonts\Mangal.ttf",
        r"C:\Windows\Fonts\Nirmala.ttf",
        r"C:\Windows\Fonts\Nirmala.ttc",
        r"C:\Windows\Fonts\NotoSansDevanagari-Regular.ttf",
    ]
    for fp in font_paths:
        if os.path.exists(fp):
            try:
                pdfmetrics.registerFont(TTFont('HindiFont', fp))
                return 'HindiFont'
            except Exception:
                continue
    
    # Try using 'Mangal' if registered
    registered = pdfmetrics.getRegisteredFontNames()
    if 'Mangal' in registered:
        return 'Mangal'
        
    return 'Helvetica'  # Fallback — Hindi may not render

HINDI_FONT = _register_fonts()


def wrap_text_pdf_fonts(text: str, bold: bool = False) -> str:
    """Format string for ReportLab Paragraph wrapping Hindi in <font name="Mangal"> and English in <font name="Arial">."""
    if not text:
        return ""
    
    text = str(text)
    
    # Tokenize tags/entities to keep them intact
    tokens = re.split(r'(<[^>]+>|&[a-zA-Z0-9#]+;)', text)
    
    registered = pdfmetrics.getRegisteredFontNames()
    e_font = 'Arial-Bold' if bold else 'Arial'
    if e_font not in registered:
        e_font = 'Helvetica-Bold' if bold else 'Helvetica'
        
    h_font = 'Mangal-Bold' if bold else 'Mangal'
    if h_font not in registered:
        h_font = HINDI_FONT
        
    result = []
    for token in tokens:
        if not token:
            continue
        if (token.startswith('<') and token.endswith('>')) or (token.startswith('&') and token.endswith(';')):
            result.append(token)
        else:
            escaped = token.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            parts = re.split(r'([\u0900-\u097F]+)', escaped)
            for part in parts:
                if not part:
                    continue
                if any('\u0900' <= char <= '\u097F' for char in part):
                    result.append(f'<font name="{h_font}">{part}</font>')
                else:
                    result.append(f'<font name="{e_font}">{part}</font>')
                    
    return "".join(result)


def Paragraph(text, style, *args, **kwargs):
    """Custom Paragraph constructor wrapper to automatically format fonts for Hindi and English."""
    bold = False
    if hasattr(style, 'fontName') and style.fontName:
        bold = 'bold' in style.fontName.lower()
    
    wrapped_text = wrap_text_pdf_fonts(text, bold=bold)
    return RLParagraph(wrapped_text, style, *args, **kwargs)


# ── Colour definitions ─────────────────────────────────────────────────────────
NAVY    = colors.HexColor("#102A56")
GOLD    = colors.HexColor("#C8A400")
LIGHT   = colors.HexColor("#F5F5F0")
WHITE   = colors.white
BLACK   = colors.black


def format_ref_no(para_no: str, date_str: str, ref_suffix: str = "") -> str:
    """Format: 
    NO.:- ADRDE/AS-QMS/PARA1/ [ref_suffix]
    Date:- 01-07-2026
    """
    try:
        d = datetime.strptime(date_str, "%Y-%m-%d")
        date_formatted = d.strftime("%d-%m-%Y")
    except Exception:
        date_formatted = date_str
    para_part = para_no.replace(" ", "").upper()  # e.g. PARA5
    suffix = ref_suffix.strip() if ref_suffix else ""
    if suffix:
        ref_line = f"NO.:- {ENVELOPE_PREFIX}/{para_part}/{suffix}"
    else:
        ref_line = f"NO.:- {ENVELOPE_PREFIX}/{para_part}"
    return f"{ref_line}\nDated:- {date_formatted}"


def _get_styles():
    styles = getSampleStyleSheet()
    return {
        "ref": ParagraphStyle(
            "RefNo", fontName='Helvetica-Bold', fontSize=9,
            alignment=TA_LEFT, textColor=NAVY, leading=13
        ),
        "to_label": ParagraphStyle(
            "ToLabel", fontName='Helvetica-Bold', fontSize=11,
            alignment=TA_LEFT, textColor=BLACK
        ),
        "address_line": ParagraphStyle(
            "AddrLine", fontName='Helvetica', fontSize=11,
            alignment=TA_LEFT, textColor=BLACK, leading=16
        ),
        "address_bold": ParagraphStyle(
            "AddrBold", fontName='Helvetica-Bold', fontSize=11,
            alignment=TA_LEFT, textColor=BLACK, leading=16
        ),
        "sp": ParagraphStyle(
            "SP", fontName='Helvetica-Bold', fontSize=10,
            alignment=TA_RIGHT, textColor=NAVY
        ),
        "header": ParagraphStyle(
            "Header", fontName='Helvetica-Bold', fontSize=14,
            alignment=TA_CENTER, textColor=WHITE
        ),
        "subheader": ParagraphStyle(
            "SubHeader", fontName='Helvetica', fontSize=10,
            alignment=TA_CENTER, textColor=colors.HexColor("#C8A400")
        ),
        "table_header": ParagraphStyle(
            "TblHdr", fontName='Helvetica-Bold', fontSize=10,
            alignment=TA_CENTER, textColor=WHITE
        ),
        "table_cell": ParagraphStyle(
            "TblCell", fontName='Helvetica', fontSize=9,
            alignment=TA_LEFT, textColor=BLACK, leading=13
        ),
        "footer": ParagraphStyle(
            "Footer", fontName='Helvetica', fontSize=8,
            alignment=TA_CENTER, textColor=colors.gray
        ),
    }


def _build_envelope_elements(record: dict, styles: dict) -> list:
    """Build flowables for a single envelope printout in plain format (Landscape)."""
    elems = []
    ref_no  = format_ref_no(record.get("para_no", ""), record.get("date_entry", ""), record.get("ref_suffix", ""))
    sp_text = record.get("delivery_type", "Ordinary / साधारण")
    sp_eng  = sp_text.split("/")[0].strip()
    sp_hin  = sp_text.split("/")[1].strip() if len(sp_text.split("/")) > 1 else ""
    sp_fmt  = f"{sp_eng}/{sp_hin}" if sp_hin else f"{sp_eng}/"

    ref_parts = ref_no.split("\n")
    no_line = ref_parts[0]
    date_line = ref_parts[1] if len(ref_parts) > 1 else ""

    # Override colors and font size, use HINDI_FONT for proper Devanagari rendering
    ref_style = ParagraphStyle('EnvRef', parent=styles['ref'], textColor=BLACK, fontSize=12, fontName=HINDI_FONT)
    sp_style = ParagraphStyle('EnvSP', parent=styles['sp'], textColor=BLACK, fontSize=12, fontName=HINDI_FONT)
    to_style = ParagraphStyle('EnvTo', parent=styles['to_label'], textColor=BLACK, fontSize=12, fontName=HINDI_FONT)
    bold_style = ParagraphStyle('EnvBold', parent=styles['address_bold'], textColor=BLACK, fontSize=12, fontName=HINDI_FONT)
    line_style = ParagraphStyle('EnvLine', parent=styles['address_line'], textColor=BLACK, fontSize=12, fontName=HINDI_FONT)

    # Create a 2-column header Table: NO:-/Date:- and By S/P
    header_table = Table(
        [
            [Paragraph(no_line, ref_style), Paragraph(f"By S/P: {sp_fmt}", sp_style)],
            [Paragraph(date_line, ref_style), ""]
        ],
        colWidths=[15*cm, 10.7*cm]
    )
    header_table.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("ALIGN", (1, 0), (1, 0), "RIGHT"),
        ("SPAN", (1, 0), (1, 1)),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 1), (0, 1), 6),  # Add a little space between No and Date
    ]))
    
    elems.append(header_table)
    elems.append(Spacer(1, 1.0*cm))  # Reduced gap before address block

    # Envelope box - Plain format with indentation
    # Col 1: Empty space (left offset)
    # Col 2: "To,"
    # Col 3: Address lines
    envelope_data = [
        ["", Paragraph("To,", to_style), ""]
    ]

    def add_line(text, style):
        if text and text.strip():
            envelope_data.append(["", "", Paragraph(text.strip(), style)])

    add_line(record.get("designation", ""), bold_style)
    add_line(record.get("office_name", ""), line_style)
    add_line(record.get("addr_line1", ""), line_style)
    add_line(record.get("addr_line2", ""), line_style)

    city_state = f"{record.get('city', '')}, {record.get('state', '')}".strip(", ")
    add_line(city_state, line_style)

    if record.get("pin_code"):
        add_line(f"PIN Code: {record.get('pin_code', '')}", line_style)

    env_table = Table(
        envelope_data,
        colWidths=[13.0*cm, 1.5*cm, 11.2*cm]
    )
    env_table.setStyle(TableStyle([
        ("VALIGN",        (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING",   (0, 0), (-1, -1), 0),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 0),
        ("TOPPADDING",    (0, 0), (-1, -1), 2.5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5),
    ]))

    elems.append(env_table)
    elems.append(Spacer(1, 0.5*cm))
    
    sender_style = styles['ref'].clone('Sender')
    sender_style.fontSize = 9
    sender_style.leading = 11
    
    sender_para = Paragraph(f"""<b>निदेशक / Director</b><br/>
<b>हवाई वितरण अनुसंधान एंव विकास संस्थापन</b><br/>
<b>Aerial Delivery Research &amp; Development Establishment</b><br/>
रक्षा अनुसंधान एंव विकास संगठन<br/>
Defence Research &amp; Development Organisation<br/>
पत्र पेटी संख्या 51, स्टेशन रोड, आगरा कैंट<br/>
Post Box No. 51, Station Road, Agra Cantt-282001""", sender_style)

    import sys
    if hasattr(sys, '_MEIPASS'):
        base_dir = sys._MEIPASS
    else:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    logo_path = os.path.join(base_dir, "assets", "adrde_logo.png")
    
    use_image_only = False
    if os.path.exists(logo_path):
        try:
            from reportlab.lib.utils import ImageReader
            img_reader = ImageReader(logo_path)
            iw, ih = img_reader.getSize()
            aspect = ih / float(iw)
            logo_img = Image(logo_path, width=11.5*cm, height=11.5*cm * aspect)
            use_image_only = True
        except Exception:
            logo_img = ""
            use_image_only = False
    else:
        use_image_only = False

    if use_image_only:
        # User requested to replace the entire box with the image itself
        sender_table = Table([[logo_img]], colWidths=[11.5*cm])
        sender_table.setStyle(TableStyle([
            ("VALIGN", (0, 0), (-1, -1), "CENTER"),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("LEFTPADDING", (0, 0), (-1, -1), 0),
            ("RIGHTPADDING", (0, 0), (-1, -1), 0),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
            ("TOPPADDING", (0, 0), (-1, -1), 0),
        ]))
    else:
        sender_inner_table = Table(
            [
                [Paragraph("<b>प्रेषक:</b>", sender_style), ""],
                [logo_img, sender_para]
            ],
            colWidths=[2.7*cm, 8.5*cm]
        )
        sender_inner_table.setStyle(TableStyle([
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("SPAN", (0, 0), (1, 0)),
            ("LEFTPADDING", (0, 0), (-1, -1), 2),
            ("RIGHTPADDING", (0, 0), (-1, -1), 2),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
            ("TOPPADDING", (0, 0), (-1, -1), 2),
        ]))
        
        sender_table = Table([[sender_inner_table]], colWidths=[11.5*cm])
        sender_table.setStyle(TableStyle([
            ("BOX", (0, 0), (-1, -1), 1, colors.black),
            ("LEFTPADDING", (0, 0), (-1, -1), 4),
            ("RIGHTPADDING", (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ("TOPPADDING", (0, 0), (-1, -1), 4),
        ]))

    bottom_table = Table(
        [
            [sender_table, ""]
        ],
        colWidths=[15*cm, 10.7*cm]
    )
    bottom_table.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "BOTTOM"),
    ]))
    elems.append(bottom_table)
    
    return elems

def _build_page_header(canvas, doc, title: str):
    """Draw the navy header band on every page."""
    canvas.saveState()
    w, h = doc.pagesize
    # Header band
    canvas.setFillColor(NAVY)
    canvas.rect(0, h - 3*cm, w, 3*cm, fill=1, stroke=0)
    # Gold underline
    canvas.setStrokeColor(GOLD)
    canvas.setLineWidth(3)
    canvas.line(0, h - 3*cm, w, h - 3*cm)
    # Title text
    canvas.setFillColor(WHITE)
    canvas.setFont("Helvetica-Bold", 13)
    canvas.drawCentredString(w/2, h - 1.6*cm, "ADRDE, DRDO — Address Management System")
    canvas.setFont("Helvetica", 9)
    canvas.setFillColor(colors.HexColor("#C8A400"))
    canvas.drawCentredString(w/2, h - 2.2*cm, title)
    # Footer
    canvas.setFillColor(colors.gray)
    canvas.setFont("Helvetica", 7)
    canvas.drawCentredString(w/2, 0.5*cm,
        f"Printed: {datetime.now().strftime('%d-%m-%Y %H:%M')} | "
        "Confidential — For Official Use Only")
    canvas.drawRightString(w - cm, 0.5*cm, f"Page {doc.page}")
    canvas.restoreState()


def generate_single_envelope_pdf(record: dict, output_path: str) -> tuple[bool, str]:
    """Generate PDF for a single address envelope."""
    try:
        doc = SimpleDocTemplate(
            output_path,
            pagesize=landscape(A4),
            topMargin=2*cm,
            bottomMargin=1.5*cm,
            leftMargin=2*cm,
            rightMargin=2*cm
        )
        styles = _get_styles()

        elements = _build_envelope_elements(record, styles)
        doc.build(elements)
        return True, output_path
    except Exception as e:
        return False, str(e)


def generate_multiple_envelopes_pdf(records: list[dict], output_path: str) -> tuple[bool, str]:
    """Generate PDF for multiple address envelopes, one per page."""
    try:
        doc = SimpleDocTemplate(
            output_path,
            pagesize=landscape(A4),
            topMargin=2*cm,
            bottomMargin=1.5*cm,
            leftMargin=2*cm,
            rightMargin=2*cm
        )
        styles = _get_styles()

        elements = []
        for i, record in enumerate(records):
            if i > 0:
                elements.append(PageBreak())
            elements.extend(_build_envelope_elements(record, styles))

        doc.build(elements)
        return True, output_path
    except Exception as e:
        return False, str(e)


def _build_label_elements(record: dict, styles: dict) -> list:
    """Build flowables for printing only reference number and date in plain format."""
    elems = []
    ref_no  = format_ref_no(record.get("para_no", ""), record.get("date_entry", ""), record.get("ref_suffix", ""))
    ref_parts = ref_no.split("\n")
    no_line = ref_parts[0]
    date_line = ref_parts[1].replace("Date:- ", "Date:-") if len(ref_parts) > 1 else ""

    # Custom style using HINDI_FONT for proper Unicode rendering
    plain_style = ParagraphStyle('LblPlain', parent=styles['address_line'], textColor=BLACK, fontSize=12, fontName=HINDI_FONT, leading=20)

    # NO line
    elems.append(Paragraph(no_line, plain_style))
    elems.append(Spacer(1, 0.5*cm))
    # Date line
    if date_line:
        elems.append(Paragraph(date_line, plain_style))
        elems.append(Spacer(1, 0.5*cm))
    
    return elems


def generate_single_label_pdf(record: dict, output_path: str) -> tuple[bool, str]:
    """Generate PDF containing ONLY reference label and date in plain format."""
    try:
        doc = SimpleDocTemplate(
            output_path,
            pagesize=A4,
            topMargin=1.5*cm,
            bottomMargin=1.5*cm,
            leftMargin=2*cm,
            rightMargin=2*cm
        )
        styles = _get_styles()

        elements = _build_label_elements(record, styles)
        # Build without header/footer
        doc.build(elements)
        return True, output_path
    except Exception as e:
        return False, str(e)


def generate_multiple_labels_pdf(records: list[dict], output_path: str) -> tuple[bool, str]:
    """Generate PDF containing ONLY reference labels, one per page in plain format."""
    try:
        doc = SimpleDocTemplate(
            output_path,
            pagesize=A4,
            topMargin=1.5*cm,
            bottomMargin=1.5*cm,
            leftMargin=2*cm,
            rightMargin=2*cm
        )
        styles = _get_styles()

        elements = []
        for i, record in enumerate(records):
            if i > 0:
                elements.append(Spacer(1, 0.5*cm))
                elements.append(HRFlowable(width="100%", thickness=1, color=colors.gray, spaceBefore=0.2*cm, spaceAfter=0.2*cm, dash=(5, 5)))
                elements.append(Spacer(1, 0.5*cm))
            elements.extend(_build_label_elements(record, styles))

        # Build without header/footer
        doc.build(elements)
        return True, output_path
    except Exception as e:
        return False, str(e)








def generate_department_list_pdf(records: list, dept_name: str,
                                  output_path: str) -> tuple[bool, str]:
    """Generate department-wise address list PDF in a plain format."""
    try:
        doc = SimpleDocTemplate(
            output_path,
            pagesize=landscape(A4),
            topMargin=1.5*cm,
            bottomMargin=1.5*cm,
            leftMargin=1.5*cm,
            rightMargin=1.5*cm
        )
        styles = _get_styles()

        # Custom plain styles using HINDI_FONT for proper Unicode rendering
        hdr_style = ParagraphStyle('DeptHdr', parent=styles['table_header'], textColor=BLACK, fontName=HINDI_FONT)
        cell_style = ParagraphStyle('DeptCell', parent=styles['table_cell'], textColor=BLACK, fontName=HINDI_FONT)

        elements = []
        
        # Add simple text header instead of blue banner
        title_style = ParagraphStyle('Title', parent=styles['header'], textColor=BLACK, fontName=HINDI_FONT, alignment=TA_CENTER)
        elements.append(Paragraph(f"Department Address List: {dept_name}", title_style))
        elements.append(Spacer(1, 10*mm))

        # Table columns — EMAIL, FAX, CONTACT excluded
        col_headers = [
            Paragraph("S.No", hdr_style),
            Paragraph("To", hdr_style),
            Paragraph("Designation", hdr_style),
            Paragraph("Office Name", hdr_style),
            Paragraph("Address", hdr_style),
            Paragraph("City/State", hdr_style),
            Paragraph("PIN", hdr_style),
            Paragraph("PARA", hdr_style),
            Paragraph("Date", hdr_style),
            Paragraph("By S/P", hdr_style),
        ]

        table_data = [col_headers]
        for i, rec in enumerate(records, 1):
            addr = rec.get("addr_line1", "")
            if rec.get("addr_line2"):
                addr += "\n" + rec["addr_line2"]
            try:
                d = datetime.strptime(rec.get("date_entry", ""), "%Y-%m-%d")
                date_str = d.strftime("%d-%m-%Y")
            except Exception:
                date_str = rec.get("date_entry", "")

            table_data.append([
                Paragraph(str(i), cell_style),
                Paragraph(rec.get("to_field", ""), cell_style),
                Paragraph(rec.get("designation", ""), cell_style),
                Paragraph(rec.get("office_name", ""), cell_style),
                Paragraph(addr, cell_style),
                Paragraph(f"{rec.get('city','')}, {rec.get('state','')}".strip(", "), cell_style),
                Paragraph(rec.get("pin_code", ""), cell_style),
                Paragraph(rec.get("para_no", ""), cell_style),
                Paragraph(date_str, cell_style),
                Paragraph(rec.get("delivery_type", ""), cell_style),
            ])

        col_widths = [1.2*cm, 2.5*cm, 3*cm, 3.5*cm, 5*cm, 3.5*cm, 1.5*cm, 1.5*cm, 2*cm, 2.3*cm]
        total_col_w = sum(col_widths)
        avail_w = landscape(A4)[0] - 3*cm
        if avail_w > total_col_w:
            col_widths = [w + (avail_w - total_col_w) * (w / total_col_w) for w in col_widths]

        tbl = Table(table_data, colWidths=col_widths, repeatRows=1)
        tbl.setStyle(TableStyle([
            ("GRID",          (0, 0), (-1, -1),  0.5, BLACK),
            ("VALIGN",        (0, 0), (-1, -1),  "TOP"),
            ("TOPPADDING",    (0, 0), (-1, -1),  4),
            ("BOTTOMPADDING", (0, 0), (-1, -1),  4),
            ("LEFTPADDING",   (0, 0), (-1, -1),  4),
            ("RIGHTPADDING",  (0, 0), (-1, -1),  4),
        ]))
        elements.append(tbl)
        doc.build(elements)
        return True, output_path
    except Exception as e:
        return False, str(e)


def generate_full_directory_pdf(records: list, output_path: str) -> tuple[bool, str]:
    """Generate complete address directory PDF (one envelope per page)."""
    try:
        doc = SimpleDocTemplate(
            output_path,
            pagesize=A4,
            topMargin=3.5*cm,
            bottomMargin=1.5*cm,
            leftMargin=2*cm,
            rightMargin=2*cm
        )
        styles = _get_styles()

        def header_footer(canvas, doc):
            _build_page_header(canvas, doc,
                "Complete Address Directory / पूर्ण पता निर्देशिका")

        elements = []
        for i, rec in enumerate(records):
            if i > 0:
                elements.append(PageBreak())
            elements += _build_envelope_elements(rec, styles)

        doc.build(elements, onFirstPage=header_footer, onLaterPages=header_footer)
        return True, output_path
    except Exception as e:
        return False, str(e)


def open_pdf(path: str):
    """Open the generated PDF with the system default viewer."""
    try:
        if sys.platform == "win32":
            os.startfile(path)
        elif sys.platform == "darwin":
            subprocess.call(["open", path])
        else:
            subprocess.call(["xdg-open", path])
    except Exception:
        pass


def get_default_output_dir() -> str:
    """Return default directory for saving PDFs (Documents folder)."""
    if sys.platform == "win32":
        docs = os.path.join(os.path.expanduser("~"), "Documents", "ADRDE_Prints")
    else:
        docs = os.path.join(os.path.expanduser("~"), "ADRDE_Prints")
    os.makedirs(docs, exist_ok=True)
    return docs


def generate_address_list_pdf(records: list, output_path: str, selected_columns: list = None) -> tuple[bool, str]:
    """Generate full address list PDF (table format) including selected columns in a plain format."""
    try:
        from reportlab.lib.pagesizes import landscape, A2, A3, A4
        styles = _get_styles()

        # Custom plain styles using HINDI_FONT for proper Unicode rendering
        hdr_style = ParagraphStyle('ListHdr', parent=styles['table_header'], textColor=BLACK, fontName=HINDI_FONT)
        cell_style = ParagraphStyle('ListCell', parent=styles['table_cell'], textColor=BLACK, fontName=HINDI_FONT)

        elements = []
        elements.append(Spacer(1, 5*mm))

        all_cols_def = [
            ("dept_name", "Dept", 2.5*cm),
            ("to_field", "To", 2.5*cm),
            ("designation", "Designation", 3.5*cm),
            ("office_name", "Office Name", 4*cm),
            ("address", "Address", 6*cm),
            ("city_state", "City/State", 3.5*cm),
            ("pin_code", "PIN", 1.8*cm),
            ("email", "Email", 4.5*cm),
            ("contact_no", "Contact", 3*cm),
            ("fax", "Fax", 3*cm),
            ("para_no", "PARA", 1.5*cm),
            ("date_entry", "Date", 2.2*cm),
            ("delivery_type", "By S/P", 2.5*cm)
        ]

        if not selected_columns:
            selected_columns = [c[0] for c in all_cols_def]

        active_cols = [c for c in all_cols_def if c[0] in selected_columns]
        
        # Calculate total width to pick a page size
        total_w = 0.8*cm + sum([c[2] for c in active_cols])
        # A4 Landscape width is ~29.7cm
        # A3 Landscape width is ~42cm
        # A2 Landscape width is ~59.4cm
        if total_w < 27*cm:
            psize = landscape(A4)
        elif total_w < 40*cm:
            psize = landscape(A3)
        else:
            psize = landscape(A2)

        doc = SimpleDocTemplate(
            output_path,
            pagesize=psize,
            topMargin=1.5*cm,
            bottomMargin=1.5*cm,
            leftMargin=1.5*cm,
            rightMargin=1.5*cm
        )

        col_headers = [Paragraph("S.No", hdr_style)]
        for c in active_cols:
            col_headers.append(Paragraph(c[1], hdr_style))

        table_data = [col_headers]
        for i, rec in enumerate(records, 1):
            row = [Paragraph(str(i), cell_style)]
            for col_id, _, _ in active_cols:
                if col_id == "address":
                    addr = rec.get("addr_line1", "")
                    if rec.get("addr_line2"):
                        addr += "\n" + rec["addr_line2"]
                    row.append(Paragraph(addr, cell_style))
                elif col_id == "city_state":
                    row.append(Paragraph(f"{rec.get('city','')}, {rec.get('state','')}".strip(", "), cell_style))
                elif col_id == "date_entry":
                    try:
                        d = datetime.strptime(rec.get("date_entry", ""), "%Y-%m-%d")
                        date_str = d.strftime("%d-%m-%Y")
                    except Exception:
                        date_str = rec.get("date_entry", "")
                    row.append(Paragraph(date_str, cell_style))
                else:
                    # Directly render text (including Hindi) using the Unicode font
                    row.append(Paragraph(rec.get(col_id, ""), cell_style))
            table_data.append(row)

        col_widths = [1.2*cm] + [c[2] for c in active_cols]
        total_col_w = sum(col_widths)
        avail_w = psize[0] - 3*cm
        if avail_w > total_col_w:
            col_widths = [w + (avail_w - total_col_w) * (w / total_col_w) for w in col_widths]

        tbl = Table(table_data, colWidths=col_widths, repeatRows=1)
        tbl.setStyle(TableStyle([
            ("GRID",          (0, 0), (-1, -1),  0.5, BLACK),
            ("VALIGN",        (0, 0), (-1, -1),  "TOP"),
            ("TOPPADDING",    (0, 0), (-1, -1),  4),
            ("BOTTOMPADDING", (0, 0), (-1, -1),  4),
            ("LEFTPADDING",   (0, 0), (-1, -1),  4),
            ("RIGHTPADDING",  (0, 0), (-1, -1),  4),
        ]))
        elements.append(tbl)
        
        # Build without the colored header/footer
        doc.build(elements)
        return True, output_path
    except Exception as e:
        return False, str(e)

def generate_reference_labels_pdf(records: list, output_path: str, print_mode: str = "both") -> tuple[bool, str]:
    """Generate reference labels matching the user's sketch."""
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import cm
        from reportlab.lib import colors

        doc = SimpleDocTemplate(
            output_path,
            pagesize=A4,
            rightMargin=1.5*cm,
            leftMargin=1.5*cm,
            topMargin=1.5*cm,
            bottomMargin=1.5*cm
        )
        
        styles = getSampleStyleSheet()
        left_style = ParagraphStyle(
            'LeftStyle',
            parent=styles['Normal'],
            fontName=HINDI_FONT,
            fontSize=12,
            leading=16,
        )
        right_style = ParagraphStyle(
            'RightStyle',
            parent=styles['Normal'],
            fontName=HINDI_FONT,
            fontSize=12,
            leading=16,
        )

        elements = []

        for i, rec in enumerate(records):
            if i > 0:
                elements.append(Spacer(1, 0.5*cm))
                elements.append(HRFlowable(width="100%", thickness=1, color=colors.gray, spaceBefore=0.2*cm, spaceAfter=0.2*cm, dash=(5, 5)))
                elements.append(Spacer(1, 0.5*cm))

            # Fetch the actual NO and Date
            ref_str = format_ref_no(rec.get("para_no", ""), rec.get("date_entry", ""), rec.get("ref_suffix", ""))
            ref_parts = ref_str.split("\n")
            no_line = ref_parts[0] if len(ref_parts) > 0 else "NO: -"
            date_line = ref_parts[1].replace("Date:- ", "Date:-") if len(ref_parts) > 1 else "Date: -"
            left_content = f"{no_line}<br/><br/>{date_line}"
            
            right_lines = ["TO,"]
            indent = "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
            if rec.get("to_field"):
                right_lines.append(indent + rec["to_field"])
            if rec.get("designation"):
                right_lines.append(indent + rec["designation"])
            if rec.get("office_name"):
                right_lines.append(indent + rec["office_name"])
            if rec.get("addr_line1"):
                right_lines.append(indent + rec["addr_line1"])
            if rec.get("addr_line2"):
                right_lines.append(indent + rec["addr_line2"])
                
            city_state_pin = ", ".join(filter(None, [rec.get("city", ""), rec.get("state", "")]))
            if rec.get("pin_code"):
                if city_state_pin:
                    city_state_pin += " - " + rec["pin_code"]
                else:
                    city_state_pin = "PIN: " + rec["pin_code"]
            if city_state_pin:
                right_lines.append(indent + city_state_pin)
                
            right_content = "<br/>".join(right_lines)
            
            if print_mode == "both":
                left_cell = Paragraph(left_content, left_style)
                right_cell = Paragraph(right_content, right_style)
                data = [[left_cell, right_cell]]
                tbl = Table(data, colWidths=[8.5*cm, 8.5*cm])
                tbl.setStyle(TableStyle([
                    ('VALIGN', (0,0), (-1,-1), 'TOP'),
                    ('LINEBEFORE', (1,0), (1,-1), 1, colors.black),
                    ('LEFTPADDING', (1,0), (1,-1), 30),
                    ('RIGHTPADDING', (0,0), (0,-1), 15),
                    ('TOPPADDING', (0,0), (-1,-1), 20),
                    ('BOTTOMPADDING', (0,0), (-1,-1), 20),
                ]))
            elif print_mode == "left":
                left_cell = Paragraph(left_content, left_style)
                data = [[left_cell]]
                tbl = Table(data, colWidths=[17*cm])
                tbl.setStyle(TableStyle([
                    ('VALIGN', (0,0), (-1,-1), 'TOP'),
                    ('LEFTPADDING', (0,0), (0,-1), 15),
                    ('RIGHTPADDING', (0,0), (0,-1), 15),
                    ('TOPPADDING', (0,0), (-1,-1), 20),
                    ('BOTTOMPADDING', (0,0), (-1,-1), 20),
                ]))
            elif print_mode == "right":
                right_cell = Paragraph(right_content, right_style)
                data = [[right_cell]]
                tbl = Table(data, colWidths=[17*cm])
                tbl.setStyle(TableStyle([
                    ('VALIGN', (0,0), (-1,-1), 'TOP'),
                    ('LEFTPADDING', (0,0), (0,-1), 15),
                    ('RIGHTPADDING', (0,0), (0,-1), 15),
                    ('TOPPADDING', (0,0), (-1,-1), 20),
                    ('BOTTOMPADDING', (0,0), (-1,-1), 20),
                ]))
            
            elements.append(tbl)
            
        doc.build(elements)
        return True, output_path
    except Exception as e:
        return False, str(e)
