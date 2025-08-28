import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QFileDialog, QMessageBox
import yt_dlp

class YouTubeDownloader(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("YouTube Video Downloader")
        self.setGeometry(200, 200, 500, 150)

        layout = QVBoxLayout()

        self.label = QLabel("YouTube linkni kiriting:")
        layout.addWidget(self.label)

        self.url_input = QLineEdit()
        layout.addWidget(self.url_input)

        self.download_button = QPushButton("Yuklab olish")
        self.download_button.clicked.connect(self.download_video)
        layout.addWidget(self.download_button)

        self.setLayout(layout)

    def download_video(self):
        url = self.url_input.text().strip()
        if not url:
            QMessageBox.warning(self, "Xatolik", "Iltimos, YouTube linkni kiriting!")
            return

        # Foydalanuvchidan saqlash papkasini tanlash
        save_path = QFileDialog.getExistingDirectory(self, "Saqlash joyini tanlang")
        if not save_path:
            return

        # faqat eng yaxshi MP4 (video+audio) formatini olish
        ydl_opts = {
            'outtmpl': os.path.join(save_path, '%(title)s.%(ext)s'),
            'format': 'best[ext=mp4][vcodec!=none][acodec!=none]',  # faqat bitta MP4 stream
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            QMessageBox.information(self, "Tugatildi", "Video muvaffaqiyatli yuklab olindi!")
        except Exception as e:
            QMessageBox.critical(self, "Xatolik", f"Yuklab olishda xatolik: {str(e)}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = YouTubeDownloader()
    window.show()
    sys.exit(app.exec_())
