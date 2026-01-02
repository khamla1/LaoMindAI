
import sys
import os
import json
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QTabWidget, QLabel, QComboBox, QSlider, QCheckBox, QPushButton, 
                             QScrollArea, QFrame, QListWidget, QMessageBox, QDialog, QLineEdit, 
                             QTextEdit, QGroupBox, QFormLayout, QPlainTextEdit)
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt, QSize

try:
    from .engine import ChatBot
except ImportError:
    from engine import ChatBot

class AdminAppQt(QMainWindow):
    def __init__(self):
        super().__init__()
        self.chatbot = ChatBot()
        self.emotion_manager = self.chatbot.emotion_manager
        
        self.setWindowTitle("LaoMind-AI Admin Panel (PyQt5)")
        self.setGeometry(100, 100, 900, 700)
        
        # Global Font Setting - key to fixing the display issue
        self.font_ui = QFont("Leelawadee UI", 11)
        self.font_h1 = QFont("Leelawadee UI", 14, QFont.Bold)
        self.setFont(self.font_ui)
        
        self._setup_ui()

    def _setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Tabs
        self.tabs = QTabWidget()
        self.tabs.setFont(self.font_ui)
        main_layout.addWidget(self.tabs)
        
        self.tab_character = QWidget()
        self.tab_knowledge = QWidget()
        self.tab_aimodels = QWidget()
        
        self.tabs.addTab(self.tab_character, "ການຕັ້ງຄ່າຕົວລະຄອນ (Character)")
        self.tabs.addTab(self.tab_knowledge, "ຄວາມຮູ້ (Knowledge)")
        self.tabs.addTab(self.tab_aimodels, "ສະໝອງ AI (AI Brain)")
        
        self._build_character_tab()
        self._build_knowledge_tab()
        self._build_aimodels_tab()

    def _build_character_tab(self):
        layout = QVBoxLayout(self.tab_character)
        
        title = QLabel("ຕັ້ງຄ່າຕົວລະຄອນ (Character Settings)")
        title.setFont(self.font_h1)
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        
        current = self.emotion_manager.load_emotions()
        
        # 1. Personality & Emotion
        group_pers = QGroupBox("1. ບຸກຄະລິກ & ອາລົມ (Personality & Emotion)")
        form_pers = QFormLayout()
        
        self.combo_personality = QComboBox()
        self.combo_personality.addItems(["ຜູ້ຊ່ວຍ", "ເພື່ອນ", "ຄູສອນ", "ບອດໜ້າຮັກ"])
        self.combo_personality.setCurrentText(current.get("personality", "ຜູ້ຊ່ວຍ"))
        form_pers.addRow("ແບບບຸກຄະລິກ:", self.combo_personality)
        
        self.combo_tone = QComboBox()
        self.combo_tone.addItems(["ທາງການ", "ໜ້າຮັກ", "ເປັນກັນເອງ"])
        self.combo_tone.setCurrentText(current.get("tone", "ທາງການ"))
        form_pers.addRow("ຮູບແບບການເວົ້າ:", self.combo_tone)
        
        self.combo_mood = QComboBox()
        self.combo_mood.addItems(["ທົ່ວໄປ", "ມີຄວາມສຸກ", "ຕື່ນເຕັ້ນ", "ສະຫງົບ", "ເສົ້າ"])
        self.combo_mood.setCurrentText(current.get("mood", "ທົ່ວໄປ"))
        form_pers.addRow("ອາລົມພື້ນຖານ:", self.combo_mood)
        
        # Sliders need a label to show value
        self.slider_empathy = QSlider(Qt.Horizontal)
        self.slider_empathy.setRange(1, 10)
        self.slider_empathy.setValue(int(current.get("empathy", 5)))
        form_pers.addRow("Empathy (1-10):", self.slider_empathy)
        
        group_pers.setLayout(form_pers)
        content_layout.addWidget(group_pers)
        
        # 2. Behavior
        group_beh = QGroupBox("2. ພຶດຕິກຳ (Behavior)")
        form_beh = QFormLayout()
        
        self.slider_accuracy = QSlider(Qt.Horizontal)
        self.slider_accuracy.setRange(1, 10)
        self.slider_accuracy.setValue(int(current.get("accuracy", 8)))
        form_beh.addRow("ຄວາມຖືກຕ້ອງ (Accuracy):", self.slider_accuracy)
        
        self.slider_creative = QSlider(Qt.Horizontal)
        self.slider_creative.setRange(1, 10)
        self.slider_creative.setValue(int(current.get("creativity", 5)))
        form_beh.addRow("ຄວາມຄິດສ້າງສັນ:", self.slider_creative)
        
        self.combo_depth = QComboBox()
        self.combo_depth.addItems(["ສັ້ນ", "ປົກກະຕິ", "ລະອຽດ"])
        self.combo_depth.setCurrentText(current.get("depth", "ປົກກະຕິ"))
        form_beh.addRow("ຄວາມລະອຽດ:", self.combo_depth)
        
        group_beh.setLayout(form_beh)
        content_layout.addWidget(group_beh)
        
        # Save Button
        btn_save = QPushButton("💾 ບັນທຶກການຕັ້ງຄ່າທັງໝົດ")
        btn_save.setFont(self.font_h1)
        btn_save.setStyleSheet("background-color: #4CAF50; color: white; padding: 10px; border-radius: 5px;")
        btn_save.clicked.connect(self._save_character_settings)
        content_layout.addWidget(btn_save)
        
        content_layout.addStretch()
        scroll.setWidget(content_widget)
        layout.addWidget(scroll)

    def _save_character_settings(self):
        settings = {
            "mood": self.combo_mood.currentText(),
            "tone": self.combo_tone.currentText(),
            "personality": self.combo_personality.currentText(),
            "empathy": self.slider_empathy.value(),
            "accuracy": self.slider_accuracy.value(),
            "creativity": self.slider_creative.value(),
            "depth": self.combo_depth.currentText(),
        }
        self.emotion_manager.save_emotions(settings)
        QMessageBox.information(self, "Saved", "ບັນທຶກການຕັ້ງຄ່າສຳເລັດ!")

    def _build_knowledge_tab(self):
        layout = QVBoxLayout(self.tab_knowledge)
        
        # Controls
        controls_layout = QHBoxLayout()
        
        btn_add = QPushButton("ເພີ່ມຂໍ້ມູນໃໝ່")
        btn_add.setStyleSheet("background-color: #2196F3; color: white;")
        btn_add.clicked.connect(lambda: self._knowledge_dialog())
        
        btn_ai = QPushButton("✨ ສ້າງຂໍ້ມູນອັດຕະໂນມັດ (AI Import)")
        btn_ai.setStyleSheet("background-color: #9C27B0; color: white;")
        btn_ai.clicked.connect(self._ai_import_dialog)
        
        btn_refresh = QPushButton("ໂຫຼດຂໍ້ມູນຄືນ")
        btn_refresh.clicked.connect(self._idx_knowledge_list)
        
        btn_del = QPushButton("ລົບລາຍການທີ່ເລືອກ")
        btn_del.setStyleSheet("background-color: #f44336; color: white;")
        btn_del.clicked.connect(self._delete_knowledge_item)
        
        controls_layout.addWidget(btn_add)
        controls_layout.addWidget(btn_ai)
        controls_layout.addWidget(btn_refresh)
        controls_layout.addStretch()
        controls_layout.addWidget(btn_del)
        
        layout.addLayout(controls_layout)
        
        # List
        self.list_knowledge = QListWidget()
        self.list_knowledge.setFont(self.font_ui)
        self.list_knowledge.doubleClicked.connect(self._edit_knowledge_item)
        layout.addWidget(self.list_knowledge)
        
        self._idx_knowledge_list()

    def _idx_knowledge_list(self):
        self.list_knowledge.clear()
        self.chatbot.refresh_knowledge()
        for item in self.chatbot.get_all_questions():
            self.list_knowledge.addItem(f"ຖາມ: {item['q']} | ຕອບ: {item['a']}")

    def _knowledge_dialog(self, old_q=None, old_a=None):
        dialog = QDialog(self)
        dialog.setWindowTitle("ແກ້ໄຂຂໍ້ມູນ" if old_q else "ເພີ່ມຂໍ້ມູນໃໝ່")
        dialog.setFont(self.font_ui)
        dialog.setMinimumWidth(500)
        
        layout = QVBoxLayout(dialog)
        
        input_q = QLineEdit()
        input_q.setStyleSheet("font-family: 'Leelawadee UI', 'Phetsarath OT'; font-size: 14px;")
        if old_q: input_q.setText(old_q)
        layout.addWidget(input_q)
        
        layout.addWidget(QLabel("ຄຳຕອບ:"))
        input_a = QLineEdit()
        input_a.setStyleSheet("font-family: 'Leelawadee UI', 'Phetsarath OT'; font-size: 14px;")
        if old_a: input_a.setText(old_a)
        layout.addWidget(input_a)
        
        btn_save = QPushButton("ບັນທຶກ")
        btn_save.setStyleSheet("background-color: #4CAF50; color: white;")
        
        def save():
            new_q, new_a = input_q.text(), input_a.text()
            if not new_q or not new_a: return
            
            if old_q:
                self.chatbot.edit_knowledge(old_q, new_q, new_a)
            else:
                self.chatbot.add_knowledge(new_q, new_a)
            self._idx_knowledge_list()
            dialog.accept()
            
        btn_save.clicked.connect(save)
        layout.addWidget(btn_save)
        dialog.exec_()

    def _edit_knowledge_item(self):
        item = self.list_knowledge.currentItem()
        if not item: return
        text = item.text()
        try:
            q_part = text.split(" | ຕອບ: ")[0].replace("ຖາມ: ", "")
            a_part = text.split(" | ຕອບ: ")[1]
            self._knowledge_dialog(q_part, a_part)
        except:
            pass

    def _delete_knowledge_item(self):
        item = self.list_knowledge.currentItem()
        if not item: return
        text = item.text()
        q_part = text.split(" | ຕອບ: ")[0].replace("ຖາມ: ", "")
        
        reply = QMessageBox.question(self, 'Confirm', f"ຕ້ອງການລົບ '{q_part}' ຫຼືບໍ່?", 
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.chatbot.delete_knowledge(q_part)
            self._idx_knowledge_list()

    def _ai_import_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("ສ້າງຂໍ້ມູນອັດຕະໂນມັດ (AI Data Generator)")
        dialog.setFont(self.font_ui)
        dialog.resize(600, 500)
        
        layout = QVBoxLayout(dialog)
        
        layout.addWidget(QLabel("ວາງບົດຄວາມ/ຂໍ້ມູນຂອງທ່ານທີ່ນີ້ (Paste Text):"))
        
        # QTextEdit supports unicode pasting much better
        txt_input = QPlainTextEdit()
        txt_input.setFont(self.font_ui)
        txt_input.setStyleSheet("QPlainTextEdit { font-family: 'Leelawadee UI', 'Phetsarath OT'; font-size: 14px; }")
        layout.addWidget(txt_input)
        
        btn_generate = QPushButton("✨ ໃຫ້ AI ສ້າງໃຫ້ (Generate)")
        btn_generate.setFont(self.font_h1)
        btn_generate.setStyleSheet("background-color: #9C27B0; color: white;")
        
        def process():
            raw_text = txt_input.toPlainText().strip()
            if len(raw_text) < 10:
                QMessageBox.warning(dialog, "Warning", "ຂໍ້ຄວາມສັ້ນເກີນໄປ!")
                return
            
            btn_generate.setText("ກຳລັງໃຫ້ AI ຄິດ... (Processing...)")
            btn_generate.setEnabled(False)
            QApplication.processEvents()
            
            try:
                prompt = (
                    f"Instructions: Analyze the text below and generate 5 to 10 question-answer pairs in Lao language. "
                    f"Return ONLY a raw JSON list of objects with keys 'q' and 'a'. "
                    f"Do NOT use Markdown formatting. Do NOT explain. Just the JSON.\n\n"
                    f"Text: {raw_text}\n"
                    f"JSON Output:"
                )
                
                if self.chatbot.active_provider == "gemini":
                    resp = self.chatbot.gemini.generate_response(prompt)
                else:
                    resp = self.chatbot.ollama.generate_response(prompt)
                
                clean_json = resp.replace("```json", "").replace("```", "").strip()
                data = json.loads(clean_json)
                
                count = 0
                if isinstance(data, list):
                    for item in data:
                        if "q" in item and "a" in item:
                            self.chatbot.add_knowledge(item["q"], item["a"])
                            count += 1
                    
                    QMessageBox.information(dialog, "Success", f"AI ສ້າງຂໍ້ມູນສຳເລັດ {count} ຂໍ້!")
                    self._idx_knowledge_list()
                    dialog.accept()
                else:
                    QMessageBox.critical(dialog, "Error", "AI ຕອບກັບມາຜິດຮູບແບບ (Not a list).")
                    
            except Exception as e:
                QMessageBox.critical(dialog, "Error", f"Failed: {e}")
            finally:
                btn_generate.setText("✨ ໃຫ້ AI ສ້າງໃຫ້ (Generate)")
                btn_generate.setEnabled(True)
        
        btn_generate.clicked.connect(process)
        layout.addWidget(btn_generate)
        
        dialog.exec_()

    def _build_aimodels_tab(self):
        layout = QVBoxLayout(self.tab_aimodels)
        
        title = QLabel("ສະໝອງ AI (AI Brain Control)")
        title.setFont(self.font_h1)
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        group = QGroupBox("ສະຖານະການທຳງານ (Status)")
        form = QFormLayout()
        
        # Model Selection
        self.combo_model = QComboBox()
        available_models = self.chatbot.ollama.get_models()
        if not available_models:
             available_models = ["gemma:2b", "gemma2:2b", "llama3", "mistral"]
        self.combo_model.addItems(available_models)
        self.combo_model.setCurrentText(self.chatbot.external_model_name)
        
        refresh_btn = QPushButton("🔄")
        refresh_btn.setFixedWidth(40)
        refresh_btn.clicked.connect(lambda: self._refresh_models())
        
        model_row = QHBoxLayout()
        model_row.addWidget(self.combo_model)
        model_row.addWidget(refresh_btn)
        
        form.addRow("ໂມເດວປັດຈຸບັນ (Current Model):", model_row)
        
        # Toggle
        self.check_ai = QCheckBox("ເປີດໃຊ້ງານ AI (Enable AI)")
        self.check_ai.setChecked(self.chatbot.use_external_model)
        self.check_ai.setStyleSheet("font-size: 14px; font-weight: bold; color: #2196F3;")
        form.addRow("ການທຳງານ:", self.check_ai)
        
        group.setLayout(form)
        layout.addWidget(group)
        
        btn_save = QPushButton("💾 ບັນທຶກສະຖານະ (Update Status)")
        btn_save.setFont(self.font_h1)
        btn_save.setStyleSheet("background-color: #4CAF50; color: white;")
        btn_save.clicked.connect(self._update_ai_settings)
        layout.addWidget(btn_save)
        
        layout.addStretch()

    def _refresh_models(self):
        mods = self.chatbot.ollama.get_models()
        if mods:
            self.combo_model.clear()
            self.combo_model.addItems(mods)
            QMessageBox.information(self, "Refreshed", f"Found {len(mods)} models!")
        else:
            QMessageBox.warning(self, "Error", "Could not fetch models.")

    def _update_ai_settings(self):
        val = self.combo_model.currentText()
        self.chatbot.active_provider = "ollama"
        self.chatbot.use_external_model = self.check_ai.isChecked()
        self.chatbot.external_model_name = val
        self.chatbot.ollama.model = val
        
        QMessageBox.information(self, "Success", f"Updated AI Status!\nModel: {val}\nAI Enabled: {self.chatbot.use_external_model}")

