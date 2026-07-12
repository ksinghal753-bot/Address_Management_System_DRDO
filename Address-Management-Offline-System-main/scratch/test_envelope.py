import sys
import os
sys.path.append(os.path.abspath('.'))
from modules.print_module import _get_styles, format_ref_no
from reportlab.lib.pagesizes import landscape, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak
from reportlab.lib import colors
from reportlab.lib.units import cm

def build_test_elements(record, styles):
    elems = []
    HINDI_FONT = 'NotoSansDevanagari'
    BLACK = colors.black
    ref_no  = format_ref_no(record.get("para_no", ""), record.get("date_entry", ""), record.get("ref_suffix", ""))
    sp_text = record.get("delivery_type", "Ordinary / ???????")
    sp_eng  = sp_text.split("/")[0].strip()
    sp_hin  = sp_text.split("/")[1].strip() if len(sp_text.split("/")) > 1 else ""
    sp_fmt  = f"{sp_eng}/{sp_hin}" if sp_hin else f"{sp_eng}/"

    ref_parts = ref_no.split("\n")
    no_line = ref_parts[0]
    date_line = ref_parts[1].replace("Date:- ", "Date:-") if len(ref_parts) > 1 else ""

    ref_style = styles['ref']
    sp_style = styles['sp']
    
    sender_style = styles['ref'].clone('Sender')
    sender_style.fontSize = 9
    sender_style.leading = 11
    
    sender_para = Paragraph(f"""<b>?????? / Director</b><br/>
<b>???? ????? ???????? ??? ????? ????????</b><br/>
<b>Aerial Delivery Research &amp; Development Establishment</b><br/>
????? ???????? ??? ????? ?????<br/>
Defence Research &amp; Development Organisation<br/>
???? ???? ?????? 51, ?????? ???, ???? ????<br/>
Post Box No. 51, Station Road, Agra Cantt-282001""", sender_style)

    logo_path = os.path.join(os.path.abspath('.'), "assets", "drdo_logo_clean.png")
    if os.path.exists(logo_path):
        logo_img = Image(logo_path, width=2.5*cm, height=2.5*cm)
    else:
        logo_img = ""

    sender_inner_table = Table(
        [
            [Paragraph("<b>??????:</b>", sender_style), ""],
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
    
    # Outer box for sender
    sender_table = Table([[sender_inner_table]], colWidths=[11.5*cm])
    sender_table.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), 1, colors.black),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
    ]))

    header_table = Table(
        [
            [sender_table, Paragraph(f"{no_line}<br/>{date_line}", ref_style), Paragraph(f"<b>By S/P:</b> {sp_fmt}", sp_style)]
        ],
        colWidths=[12.5*cm, 7*cm, 6.2*cm]
    )
    header_table.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("ALIGN", (2, 0), (2, 0), "RIGHT"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
    ]))
    
    elems.append(header_table)
    return elems

def test():
    doc = SimpleDocTemplate('scratch/test_env.pdf', pagesize=landscape(A4), topMargin=2*cm, bottomMargin=1.5*cm, leftMargin=2*cm, rightMargin=2*cm)
    rec = {
        "para_no": "ADRDE/AS-QMS/PARA1",
        "date_entry": "2026-07-11",
        "ref_suffix": "",
        "delivery_type": "Registered/?????????"
    }
    styles = _get_styles()
    elems = build_test_elements(rec, styles)
    doc.build(elems)

test()
print('PDF generated')
