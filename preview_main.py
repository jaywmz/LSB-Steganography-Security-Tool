from PyQt5.QtWidgets import (QFrame, QDialog, QApplication, QMainWindow, QPushButton, 
                             QSpacerItem, QSizePolicy, QVBoxLayout, QHBoxLayout, 
                             QWidget, QScrollArea, QLabel, QFileDialog, QMessageBox, 
                             QComboBox, QStackedWidget)
from PyQt5.QtCore import Qt, pyqtSignal, QUrl
from PyQt5.QtGui import QDragEnterEvent, QDropEvent, QMouseEvent, QIcon, QPixmap
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
import os
import vlc
from steganography import Steganography

def preview(param1, param2):
    preview_app = QApplication([])
    win = QMainWindow()
    win.setWindowTitle('Preview')
    win.setGeometry(100, 100, 600, 400)
    win.show()
    preview_app.exec_()
    

if __name__ == '__main__':
    preview()