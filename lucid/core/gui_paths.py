"""
# Lucid UI Path Library

* Description:

    Herein is a library of paths to various ui and gui files, such as images
    and qss files.
"""


from pathlib import Path


# --------Directories----------------------------------------------------------

RESOURCES_PATH = Path(Path(__file__).parent, 'resources')
ICONS_PATH = Path(RESOURCES_PATH, 'icons')


# --------Stylesheets----------------------------------------------------------

COMBINEAR_QSS = Path(RESOURCES_PATH, 'Combinear.qss')


# --------Pipeline Icons-------------------------------------------------------

LAUNCHER_ICON = Path(ICONS_PATH, 'ICON_Lucid_Launcher_128.ico')

# ----------Generic Color Button Icons-----------------------------------------

BUTTON_40X40_BLUE = Path(ICONS_PATH, 'ICON_Default_Blue_40x40.png')
BUTTON_80X40_BLUE = Path(ICONS_PATH, 'ICON_Default_Blue_80x40.png.png')
BUTTON_40X40_CYAN = Path(ICONS_PATH, 'ICON_Default_Cyan_40x40.png')
BUTTON_40X40_GREEN = Path(ICONS_PATH, 'ICON_Default_Green_40x40.png')
BUTTON_40X40_ORANGE = Path(ICONS_PATH, 'ICON_Default_Orange_40x40.png')
BUTTON_40X40_PURPLE = Path(ICONS_PATH, 'ICON_Default_Purple_40x40.png')
BUTTON_40X40_RED = Path(ICONS_PATH, 'ICON_Default_Red_40x40.png')
BUTTON_40X40_YELLOW = Path(ICONS_PATH, 'ICON_Default_Yellow_40x40.png')
BUTTON_200X40_FLAT_BLACK = Path(ICONS_PATH, 'ICON_FlatBlack_200x40.png')
BUTTON_40X40_BLACK = Path(ICONS_PATH, 'ICON_Default_Black_40x40.png')

# ----------Misc Icons---------------------------------------------------------

CHECK_ICON = Path(ICONS_PATH, 'check.png')
EYE_ICON = Path(ICONS_PATH, 'eye.png')
