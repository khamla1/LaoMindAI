
import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFont
from src.ui_chat import ChatAppQt

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Global Font Setting
    font = QFont("Leelawadee UI", 11)
    app.setFont(font)
    
    window = ChatAppQt()
    window.show()
    sys.exit(app.exec_())
