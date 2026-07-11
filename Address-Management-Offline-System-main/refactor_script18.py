import os

# 1. Update modern_theme.py
file_path_theme = r"c:\Users\KANIKA SINGHAL\OneDrive\Desktop\New folder\CANTEEN_MANAGEMENT_SYSTEM\ADRDE_DRDO\ADRDE_ADDRESS\ui\modern_theme.py"

with open(file_path_theme, "r", encoding="utf-8") as f:
    content_theme = f.read()

qmenu_style = """
        /* ── Dropdown Menus ── */
        QMenu {
            background-color: #FFFFFF;
            color: #111827;
            border: 1px solid #E2E8F0;
            border-radius: 6px;
            padding: 4px 0px;
        }
        QMenu::item {
            padding: 6px 24px;
            background: transparent;
        }
        QMenu::item:selected {
            background-color: #F0F9FF;
            color: #0369A1;
        }
"""

# Insert before QMenuBar
if "/* ── Menu/Status Bar ── */" in content_theme:
    content_theme = content_theme.replace("/* ── Menu/Status Bar ── */", qmenu_style + "\n        /* ── Menu/Status Bar ── */")
else:
    # Append it to the end if not found
    content_theme += qmenu_style

with open(file_path_theme, "w", encoding="utf-8") as f:
    f.write(content_theme)


# 2. Update constants.py
file_path_const = r"c:\Users\KANIKA SINGHAL\OneDrive\Desktop\New folder\CANTEEN_MANAGEMENT_SYSTEM\ADRDE_DRDO\ADRDE_ADDRESS\utils\constants.py"

with open(file_path_const, "r", encoding="utf-8") as f:
    content_const = f.read()

qmenu_style_const = """
    /* ── Dropdown Menus ── */
    QMenu {
        background-color: #FFFFFF;
        color: #111827;
        border: 1px solid #E2D8CD;
        border-radius: 6px;
        padding: 4px 0px;
    }
    QMenu::item {
        padding: 6px 24px;
        background: transparent;
    }
    QMenu::item:selected {
        background-color: #E3F2FD;
        color: #1E3A8A;
    }
"""

if "/* ── QCalendarWidget" in content_const:
    content_const = content_const.replace("/* ── QCalendarWidget", qmenu_style_const + "\n    /* ── QCalendarWidget")
else:
    content_const += qmenu_style_const

with open(file_path_const, "w", encoding="utf-8") as f:
    f.write(content_const)

print("QMenu styles added successfully.")
