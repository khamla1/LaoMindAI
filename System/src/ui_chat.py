
import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLineEdit, QPushButton, QLabel, QScrollArea, QFrame, QSizePolicy)
from PyQt5.QtGui import QFont, QIcon, QPalette, QColor
from PyQt5.QtCore import Qt, QTimer, QSize

try:
    from .engine import ChatBot
except ImportError:
    from engine import ChatBot


class CopyableLabel(QLabel):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.setCursor(Qt.IBeamCursor)
    
    def contextMenuEvent(self, event):
        from PyQt5.QtWidgets import QMenu, QAction
        menu = QMenu(self)
        copy_action = QAction("ຄັດລອກ (Copy)", self)
        copy_action.triggered.connect(self.copy_text)
        menu.addAction(copy_action)
        menu.exec_(event.globalPos())
        
    def copy_text(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.text())

class ChatAppQt(QMainWindow):
    def __init__(self):
        super().__init__()
        self.chatbot = ChatBot()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("LaoMind-AI (Intelligent Chatbot)")
        self.setGeometry(100, 100, 480, 800)
        self.setStyleSheet("background-color: #F5F5F5;")

        # Main Layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.main_layout = QVBoxLayout(central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # 1. Header
        header = QLabel("LaoMind-AI")
        header.setAlignment(Qt.AlignCenter)
        header.setStyleSheet("""
            background-color: #0084FF; 
            color: white; 
            padding: 15px; 
            font-size: 18px; 
            font-weight: bold;
        """)
        header.setFixedHeight(60)
        self.main_layout.addWidget(header)

        # 2. Chat Area (Scrollable)
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("border: none; background-color: #F2F2F2;")
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        # Container for messages inside scroll area
        self.chat_container = QWidget()
        self.chat_container.setStyleSheet("background-color: transparent;")
        self.chat_layout = QVBoxLayout(self.chat_container)
        self.chat_layout.setAlignment(Qt.AlignTop)
        self.chat_layout.setContentsMargins(15, 15, 15, 15)
        self.chat_layout.setSpacing(15) # Space between messages

        self.scroll_area.setWidget(self.chat_container)
        self.main_layout.addWidget(self.scroll_area)

        # 3. Input Area
        input_container = QWidget()
        input_container.setStyleSheet("background-color: white; border-top: 1px solid #DDDDDD;")
        input_container.setFixedHeight(70)
        input_layout = QHBoxLayout(input_container)
        input_layout.setContentsMargins(10, 10, 10, 10)

        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("ພິມຂໍ້ຄວາມບ່ອນນີ້...")
        self.input_field.setStyleSheet("""
            QLineEdit {
                border: none;
                padding: 10px;
                font-family: 'Leelawadee UI', 'Phetsarath OT';
                font-size: 14px;
                background-color: #F0F2F5;
                border-radius: 20px;
            }
        """)
        self.input_field.returnPressed.connect(self.send_message)
        input_layout.addWidget(self.input_field)

        send_btn = QPushButton("ສົ່ງ")
        send_btn.setCursor(Qt.PointingHandCursor)
        send_btn.clicked.connect(self.send_message)
        send_btn.setFixedSize(60, 40)
        send_btn.setStyleSheet("""
            QPushButton {
                background-color: #0084FF;
                color: white;
                border: none;
                border-radius: 20px;
                font-weight: bold;
                font-family: 'Leelawadee UI';
            }
            QPushButton:hover {
                background-color: #0073E6;
            }
        """)
        input_layout.addWidget(send_btn)

        self.main_layout.addWidget(input_container)

        # Welcome Message
        first_msg = self.chatbot.emotion_manager.apply_style("ສະບາຍດີ! ມີຫຍັງໃຫ້ຂ້ອຍຊ່ວຍມື້ນີ້?")
        self.display_message("AI", first_msg, False)

    def send_message(self):
        msg = self.input_field.text().strip()
        if not msg:
            return

        self.display_message("ທ່ານ", msg, True)
        self.input_field.clear()

        # Get reply (Logic kept same)
        # Using QTimer to minimize UI freeze, though threading would be better in future
        QTimer.singleShot(100, lambda: self._process_reply(msg))

    def _process_reply(self, user_msg):
        reply = self.chatbot.get_response(user_msg)
        self.display_message("AI", reply, False)

    def display_message(self, sender, message, is_user):
        # Create a container row for alignment
        row_widget = QWidget()
        row_layout = QHBoxLayout(row_widget)
        row_layout.setContentsMargins(0, 0, 0, 0)
        
        # Bubble Frame (Label inside)
        bubble = CopyableLabel(message)
        bubble.setWordWrap(True)
        # Max width 60-70% of window
        bubble.setMaximumWidth(int(self.scroll_area.width() * 0.7))
        bubble.setFont(QFont("Leelawadee UI", 11))
        
        if is_user:
            # User: Right Side, Light Green
            row_layout.addStretch() # Push to right
            row_layout.addWidget(bubble)
            
            bubble.setStyleSheet("""
                QLabel {
                    background-color: #DCF8C6;
                    color: black;
                    padding: 12px 16px;
                    border-radius: 15px;
                    border-bottom-right-radius: 2px;
                }
            """)
        else:
            # AI: Left Side, Light Blue
            row_layout.addWidget(bubble)
            row_layout.addStretch() # Push to left
            
            bubble.setStyleSheet("""
                QLabel {
                    background-color: #E3F2FD;
                    color: black;
                    padding: 12px 16px;
                    border-radius: 15px;
                    border-bottom-left-radius: 2px;
                }
            """)

        self.chat_layout.addWidget(row_widget)
        
        # Auto Scroll to bottom
        QTimer.singleShot(50, lambda: self._scroll_to_bottom())

    def _scroll_to_bottom(self):
        scrollbar = self.scroll_area.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    font = QFont("Leelawadee UI", 11)
    app.setFont(font)
    
    window = ChatAppQt()
    window.show()
    sys.exit(app.exec_())
