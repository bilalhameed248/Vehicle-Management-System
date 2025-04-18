import os, sys
def get_asset_path(relative_path):
    """ Returns the correct path to assets whether running as script or .exe """
    if getattr(sys, 'frozen', False):  # If running as a compiled .exe
        base_path = sys._MEIPASS  # Temporary folder where PyInstaller extracts files
    else:
        base_path = os.path.dirname(os.path.abspath(sys.argv[0]))
    full_path = os.path.join(base_path, relative_path)
    return os.path.normpath(full_path)
