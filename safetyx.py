import os
import shutil
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QPushButton,
    QFileDialog, QListWidget, QMessageBox, QCheckBox, QLineEdit,
    QDialog, QHBoxLayout, QTextEdit
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPalette, QColor, QFont
from config import check_password, change_password, init_password

FOLDERS = {
    "Rasmlar": "folders/images",
    "Videolar": "folders/videos",
    "Fayllar": "folders/files"
}

class PasswordDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Parolni kiriting")
        self.setFixedSize(300, 150)
        self.setStyleSheet("background-color: #2e2e2e; color: white;")
        layout = QVBoxLayout()
        label = QLabel("Parol:")
        label.setStyleSheet("color: white;")
        self.input = QLineEdit()
        self.input.setEchoMode(QLineEdit.EchoMode.Password)
        self.input.setStyleSheet("padding: 8px; background-color: #444; color: white; border-radius: 5px;")
        btn = QPushButton("Kirish")
        btn.setStyleSheet("padding: 8px; background-color: #5c5cff; color: white; border-radius: 5px;")
        btn.clicked.connect(self.check)
        layout.addWidget(label)
        layout.addWidget(self.input)
        layout.addWidget(btn)
        self.setLayout(layout)
        self.accepted = False

    def check(self):
        if check_password(self.input.text()):
            self.accepted = True
            self.accept()
        else:
            QMessageBox.warning(self, "Xato", "Noto'g'ri parol")

class ChangePasswordDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Parolni o‘zgartirish")
        self.setFixedSize(300, 250)
        self.setStyleSheet("background-color: #2e2e2e; color: white;")
        layout = QVBoxLayout()
        self.old_pass = QLineEdit()
        self.old_pass.setEchoMode(QLineEdit.EchoMode.Password)
        self.new_pass = QLineEdit()
        self.new_pass.setEchoMode(QLineEdit.EchoMode.Password)
        self.confirm_pass = QLineEdit()
        self.confirm_pass.setEchoMode(QLineEdit.EchoMode.Password)

        for label_text, widget in [("Joriy parol:", self.old_pass), ("Yangi parol:", self.new_pass), ("Takrorlang:", self.confirm_pass)]:
            label = QLabel(label_text)
            label.setStyleSheet("color: white;")
            widget.setStyleSheet("padding: 8px; background-color: #444; color: white; border-radius: 5px;")
            layout.addWidget(label)
            layout.addWidget(widget)

        btn = QPushButton("Saqlash")
        btn.setStyleSheet("padding: 8px; background-color: #5c5cff; color: white; border-radius: 5px;")
        btn.clicked.connect(self.change_password)
        layout.addWidget(btn)
        self.setLayout(layout)

    def change_password(self):
        if not check_password(self.old_pass.text()):
            QMessageBox.warning(self, "Xato", "Joriy parol noto‘g‘ri")
        elif self.new_pass.text() != self.confirm_pass.text():
            QMessageBox.warning(self, "Xato", "Yangi parollar mos emas")
        elif len(self.new_pass.text()) < 4:
            QMessageBox.warning(self, "Xato", "Parol juda qisqa")
        else:
            change_password(self.new_pass.text())
            QMessageBox.information(self, "OK", "Parol o‘zgartirildi")
            self.accept()

class FolderWindow(QWidget):
    def __init__(self, folder_name, folder_path):
        super().__init__()
        self.folder_name = folder_name
        self.folder_path = folder_path
        self.setWindowTitle(f"{folder_name}")
        self.setMinimumSize(600, 500)
        self.setStyleSheet("background-color: #1e1e1e; color: white;")

        layout = QVBoxLayout()

        back_btn = QPushButton("⬅️ Orqaga")
        back_btn.clicked.connect(self.close)
        back_btn.setStyleSheet("background-color: #444; color: white; padding: 8px; border-radius: 5px;")
        layout.addWidget(back_btn)

        self.file_list = QListWidget()
        self.file_list.setStyleSheet("background-color: #2e2e2e; color: white;")
        layout.addWidget(self.file_list)

        self.show_hidden = QCheckBox("Yashirin fayllarni ko‘rsatish")
        self.show_hidden.setStyleSheet("color: white;")
        self.show_hidden.stateChanged.connect(self.load_files)
        layout.addWidget(self.show_hidden)

        btn_layout = QHBoxLayout()
        for label, method in [("➕ Qo‘shish", self.add_file), ("❌ O‘chirish", self.delete_file), ("📝 Tahrirlash", self.edit_selected)]:
            btn = QPushButton(label)
            btn.setStyleSheet("background-color: #5c5cff; color: white; padding: 8px; border-radius: 5px;")
            btn.clicked.connect(method)
            btn_layout.addWidget(btn)
        layout.addLayout(btn_layout)

        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Qidiruv...")
        self.search_input.setStyleSheet("padding: 6px; background-color: #333; color: white; border-radius: 5px;")
        btn_search = QPushButton("🔍")
        btn_search.setStyleSheet("background-color: #5c5cff; color: white; padding: 6px; border-radius: 5px;")
        btn_search.clicked.connect(self.search_files)
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(btn_search)
        layout.addLayout(search_layout)

        self.setLayout(layout)
        self.load_files()

    def load_files(self):
        self.file_list.clear()
        if not os.path.exists(self.folder_path):
            os.makedirs(self.folder_path)
        for file in os.listdir(self.folder_path):
            path = os.path.join(self.folder_path, file)
            if not self.show_hidden.isChecked() and self.is_hidden(path):
                continue
            self.file_list.addItem(file)

    def add_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Fayl tanlang")
        if file_path:
            filename = os.path.basename(file_path)
            dest = os.path.join(self.folder_path, filename)
            try:
                shutil.copy(file_path, dest)
                self.hide_file(dest)
                self.load_files()
            except Exception as e:
                QMessageBox.critical(self, "Xato", f"Faylni qo‘shib bo‘lmadi:\n{str(e)}")

    def delete_file(self):
        selected = self.file_list.currentItem()
        if selected:
            path = os.path.join(self.folder_path, selected.text())
            os.remove(path)
            self.load_files()

    def edit_selected(self):
        selected = self.file_list.currentItem()
        if selected and selected.text().endswith(".txt"):
            path = os.path.join(self.folder_path, selected.text())
            dlg = EditTextDialog(path)
            dlg.exec()
            self.load_files()
        else:
            QMessageBox.warning(self, "Xato", ".txt faylni tanlang")

    def search_files(self):
        self.file_list.clear()
        query = self.search_input.text().lower()
        for file in os.listdir(self.folder_path):
            if query in file.lower():
                self.file_list.addItem(file)

    def is_hidden(self, filepath):
        return bool(os.stat(filepath).st_file_attributes & 2)

    def hide_file(self, filepath):
        os.system(f'attrib +h "{filepath}"')

class EditTextDialog(QDialog):
    def __init__(self, filepath):
        super().__init__()
        self.setWindowTitle("Faylni tahrirlash")
        self.setMinimumSize(500, 300)
        self.setStyleSheet("background-color: #1e1e1e; color: white;")
        layout = QVBoxLayout()
        self.editor = QTextEdit()
        self.editor.setStyleSheet("background-color: #2e2e2e; color: white;")
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                self.editor.setText(f.read())
        except:
            self.editor.setText("")
        layout.addWidget(QLabel(f"Fayl: {os.path.basename(filepath)}"))
        layout.addWidget(self.editor)
        btn = QPushButton("Saqlash")
        btn.clicked.connect(self.save)
        btn.setStyleSheet("padding: 8px; background-color: #5c5cff; color: white; border-radius: 5px;")
        layout.addWidget(btn)
        self.setLayout(layout)
        self.filepath = filepath

    def save(self):
        with open(self.filepath, "w", encoding="utf-8") as f:
            f.write(self.editor.toPlainText())
        QMessageBox.information(self, "OK", "Saqlandi")
        self.accept()

class FileManagerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Yashirin Fayl Menejeri")
        self.setMinimumSize(450, 350)
        self.setStyleSheet("background-color: #121212; color: white;")
        self.windows = []

        layout = QVBoxLayout()
        title = QLabel("📁 Papkani tanlang:")
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(title)

        for name, path in FOLDERS.items():
            btn = QPushButton(name)
            btn.setStyleSheet("padding: 10px; background-color: #3a3aff; color: white; border-radius: 8px;")
            btn.clicked.connect(lambda checked, n=name, p=path: self.open_folder(n, p))
            layout.addWidget(btn)

        self.btn_change_pass = QPushButton("🔒 Parolni o‘zgartirish")
        self.btn_change_pass.setStyleSheet("background-color: #ff8800; color: white; padding: 8px; border-radius: 6px;")
        self.btn_change_pass.clicked.connect(self.change_password_dialog)
        layout.addWidget(self.btn_change_pass)

        self.btn_exit = QPushButton("🚪 Chiqish")
        self.btn_exit.setStyleSheet("background-color: #cc0000; color: white; padding: 8px; border-radius: 6px;")
        self.btn_exit.clicked.connect(self.close_app)
        layout.addWidget(self.btn_exit)

        self.setLayout(layout)

    def open_folder(self, name, path):
        dlg = FolderWindow(name, path)
        self.windows.append(dlg)
        dlg.show()

    def change_password_dialog(self):
        dlg = ChangePasswordDialog()
        dlg.exec()

    def close_app(self):
        QApplication.quit()

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    init_password()
    login = PasswordDialog()
    if login.exec() == QDialog.DialogCode.Accepted and login.accepted:
        window = FileManagerApp()
        window.show()
        sys.exit(app.exec())
