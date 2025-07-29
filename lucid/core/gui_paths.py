"""
# Lucid UI Path Library

* Description:

    Herein is a library of paths to various ui and gui files, such as images
    and qss files.
"""


from pathlib import Path


# --------Directories----------------------------------------------------------

resources_path = Path(Path(__file__).parent, 'resources')
icons_path = Path(resources_path, 'icons')


# --------Stylesheets----------------------------------------------------------

combinear_qss = Path(resources_path, 'Combinear.qss')


# --------Icons----------------------------------------------------------------

launcher_icon = Path(icons_path, 'ICON_Lucid_Launcher_128.ico')
