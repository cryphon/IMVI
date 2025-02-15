import os
from PyQt5.QtGui import QFontDatabase

def load_fonts(font_dir):
    """Load all font files from the specified directory"""
    for font_file in os.listdir(font_dir):
        if font_file.endswith('.ttf'):  # TrueType fonts
            font_path = os.path.join(font_dir, font_file)
            QFontDatabase.addApplicationFont(font_path)
