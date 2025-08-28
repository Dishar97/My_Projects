
import sys
import subprocess
import requests
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLineEdit, QLabel, QScrollArea, QComboBox, QInputDialog, QMessageBox, QTextBrowser
)
from PyQt6.QtCore import Qt

# ========== SETTINGS ==========
OLLAMA_MODELS = ["gemma:7b", "llama3", "mistral"]
DEFAULT_MODEL = "gemma:7b"
OLLAMA_URL = "http://localhost:11434/api/generate"


# ========== OLLAMA STARTUP ==========
def start_ollama_if_needed(model):
    try:
        requests.get("http://localhost:11434", timeout=3)
    except:
        subprocess.Popen(["ollama", "run", model], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


# ========== SEND TO GEMMA/OLLAMA ==========
def query_ollama(prompt, model):
    headers = {"Content-Type": "application/json"}
    data = {"model": model, "prompt": prompt, "stream": False}
    try:
        response = requests.post(OLLAMA_URL, json=data, headers=headers, timeout=60)
        return response.json().get("response", "").strip() if response.ok else f"Xatolik: {response.status_code}"
    except Exception as e:
        return f"❌ Ulanishda xatolik: {str(e)}"


# ========== MAIN CHAT UI ==========
class ChatApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gemma Chat - ChatGPT Style")
        self.setMinimumSize(800, 600)
        self.theme = "dark"
        self.model = DEFAULT_MODEL

        self.layout = QVBoxLayout(self)
        self.setStyleSheet(self.get_stylesheet())

        # Model selector
        self.model_selector = QComboBox()
        self.model_selector.addItems(OLLAMA_MODELS)
        self.model_selector.setCurrentText(self.model)
        self.model_selector.currentTextChanged.connect(self.change_model)

        # Theme switch
        self.theme_button = QPushButton("🌙 Tungi rejim")
        self.theme_button.clicked.connect(self.toggle_theme)

        # Yuqori panel
        top_layout = QHBoxLayout()
        top_layout.addWidget(QLabel("Model tanlang:"))
        top_layout.addWidget(self.model_selector)
        top_layout.addStretch()
        top_layout.addWidget(self.theme_button)
        self.layout.addLayout(top_layout)

        # Chat area
        self.chat_area = QTextBrowser()
        self.chat_area.setOpenExternalLinks(True)
        self.layout.addWidget(self.chat_area)

        # Input field
        input_layout = QHBoxLayout()
        self.input = QLineEdit()
        self.input.setPlaceholderText("Xabar yozing...")
        self.input.returnPressed.connect(self.send_message)
        self.send_button = QPushButton("Yuborish")
        self.send_button.clicked.connect(self.send_message)
        input_layout.addWidget(self.input)
        input_layout.addWidget(self.send_button)

        self.layout.addLayout(input_layout)

    def get_stylesheet(self):
        if self.theme == "dark":
            return '''
            QWidget { background-color: #1e1e1e; color: #ffffff; font-size: 15px; font-family: Segoe UI; }
            QLineEdit, QTextBrowser { background-color: #2d2d2d; border: 1px solid #444; border-radius: 6px; padding: 8px; }
            QPushButton { background-color: #10a37f; border: none; padding: 8px 16px; border-radius: 6px; }
            QPushButton:hover { background-color: #0e8c6a; }
            QComboBox { background-color: #2d2d2d; border: 1px solid #444; padding: 6px; border-radius: 6px; }
            '''
        else:
            return '''
            QWidget { background-color: #f4f4f4; color: #000000; font-size: 15px; font-family: Segoe UI; }
            QLineEdit, QTextBrowser { background-color: #ffffff; border: 1px solid #ccc; border-radius: 6px; padding: 8px; }
            QPushButton { background-color: #10a37f; color: white; border: none; padding: 8px 16px; border-radius: 6px; }
            QPushButton:hover { background-color: #0e8c6a; }
            QComboBox { background-color: #ffffff; border: 1px solid #ccc; padding: 6px; border-radius: 6px; }
            '''

    def toggle_theme(self):
        self.theme = "light" if self.theme == "dark" else "dark"
        self.setStyleSheet(self.get_stylesheet())
        self.theme_button.setText("☀️ Kunduzgi rejim" if self.theme == "dark" else "🌙 Tungi rejim")

    def send_message(self):
        prompt = self.input.text().strip()
        if not prompt:
            return
        self.append_message("Siz", prompt)
        self.input.clear()
        reply = query_ollama(prompt, self.model)
        self.append_message("Gemma", reply)

    def append_message(self, sender, message):
        block_style = "padding: 10px; margin: 10px 0; border-radius: 10px;"
        if sender == "Siz":
            html = f"<div style='{block_style} background-color:#0e8c6a; color:white;'><b>{sender}:</b><br>{message}</div>"
        else:
            html = f"<div style='{block_style} background-color:#444; color:white;'><b>{sender}:</b><br>{message}</div>"
        self.chat_area.append(html)

    def change_model(self, selected_model):
        self.model = selected_model
        self.append_message("🧠", f"Model o‘zgartirildi: {selected_model}")


# ========== PASSWORD CHECK ==========


    start_ollama_if_needed(DEFAULT_MODEL)

    window = ChatApp()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
