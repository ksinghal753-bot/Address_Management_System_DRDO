import os
import sys

def get_preview_html():
    if hasattr(sys, '_MEIPASS'):
        base_dir = sys._MEIPASS
    else:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    logo_path = os.path.join(base_dir, "assets", "drdo_logo_clean.png").replace('\\', '/')

    sender_html = f'''
    <table style="border: 1px solid black; border-collapse: collapse; color: black; font-size: 10pt; font-weight: normal; font-family: Arial, sans-serif;">
        <tr><td colspan="2" style="padding: 4px;"><b>Sender:</b></td></tr>
        <tr>
            <td style="padding: 4px; vertical-align: top;">
                <img src="file:///{logo_path}" width="80" height="80" />
            </td>
            <td style="padding: 4px; vertical-align: top; line-height: 1.2;">
                <b>Director</b><br/>
                <b>Aerial Delivery Research</b><br/>
                Defence Research<br/>
                Post Box No. 51
            </td>
        </tr>
    </table>
    '''
    return sender_html

print(get_preview_html())
