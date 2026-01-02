
import sys
from PyQt5.QtWidgets import QApplication
from src.ui_admin import AdminAppQt

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Global Font Fix for Windows
    from PyQt5.QtGui import QFont
    font = QFont("Leelawadee UI", 11)
    app.setFont(font)
    
    window = AdminAppQt()
    window.show()
    sys.exit(app.exec_())
