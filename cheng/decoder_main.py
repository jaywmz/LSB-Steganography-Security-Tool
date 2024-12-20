from PyQt5.QtWidgets import QFrame, QApplication, QMainWindow, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QScrollArea, QLabel, QFileDialog, QMessageBox, QComboBox, QStackedWidget
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QDragEnterEvent, QDropEvent, QMouseEvent, QPixmap
import vlc
from PIL import Image
from steganography import Steganography

class FileDropBox(QLabel):
    def __init__(self, valid_extensions, preview_stack, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.valid_extensions = valid_extensions
        self.preview_stack = preview_stack
        
        # VLC player initialization
        self.instance = vlc.Instance()
        self.player = self.instance.media_player_new()
        self.video_widget = QFrame()
        self.preview_stack.addWidget(self.video_widget)

        self.setText("Drag and drop a file here \nor \nclick to select")
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet("border: 2px dashed #aaa; margin-left: 10px;")
        self.setAcceptDrops(True)
        self.setMinimumSize(200, 100)

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):
        if event.mimeData().hasUrls():
            url = event.mimeData().urls()[0]
            file_path = url.toLocalFile()
            if file_path is None:
                self.preview_label.clear()
                return
            if file_path.lower().endswith(tuple(self.valid_extensions)):
                self.setText(file_path)
                self.preview_file(file_path)
            else:
                self.setText("Drag and drop a file here \nor \nclick to select")
                self.preview_file(None)
                msgBox = QMessageBox(self)
                msgBox.setIcon(QMessageBox.Warning)
                msgBox.setWindowTitle("Invalid File Type")
                msgBox.setText("Please drag and drop a file of type: " + ", ".join(self.valid_extensions))
                msgBox.setStyleSheet("border: 0px;")
                msgBox.exec_()

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            fileFilter = ";;".join([f"{ext.upper()} Files (*{ext})" for ext in self.valid_extensions])
            fileName, _ = QFileDialog.getOpenFileName(self, "Select a file", "", fileFilter)
            if fileName:
                self.setText(fileName)
                self.preview_file(fileName)
    
    def preview_file(self, file_path):
        if file_path is None:
            return
        if file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            self.player.stop()
            pixmap = QPixmap(file_path)
            pixmap = pixmap.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.preview_stack.setCurrentIndex(0)
            self.preview_stack.currentWidget().setPixmap(pixmap)
        elif file_path.lower().endswith(('.mp4', '.avi', '.mov', '.mkv', '.wav', '.mp3', '.ogg', '.flac', '.m4a', '.aac')):
            self.player.stop()
            media = self.instance.media_new(file_path)
            self.player.set_media(media)
            self.player.set_hwnd(int(self.video_widget.winId()))
            self.player.play()
            self.preview_stack.setCurrentIndex(1)
        elif file_path.lower().endswith('.txt'):
            with open(file_path, 'r') as file:
                content = file.read(1000)
            if len(content) == 1000:
                content += '...'
            self.preview_stack.setCurrentIndex(0)
            self.preview_stack.currentWidget().setText(content)

    def handle_error(self):
        error = self.player.get_state()
        if error == vlc.State.Error:
            error_message = self.player.get_state()
            print(f"Error: {error_message}")
            msgBox = QMessageBox(self)
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setWindowTitle("Error")
            msgBox.setText(f"Error: {error_message}")
            msgBox.setStyleSheet("border: 0px;")
            msgBox.exec_()

def window():
    
    global stegoFilePath, payloadFilePath, coverFilePath, lsb
    stegoFilePath = ""
    payloadFilePath = ""
    coverFilePath = ""
    lsb = 0
    
    app = QApplication([])
    win = QMainWindow()
    win.setWindowTitle("LSB Steganography Decoder")
    win.resize(600, 400)
    
    # Main Window Widget
    widget = QWidget()
    layout = QVBoxLayout(widget)

    # Title
    titleLabel = QLabel("LSB Steganography Decoder")
    titleLabel.setStyleSheet("font-size: 20px;margin: 10px;text-decoration: underline;")
    layout.addWidget(titleLabel)
    
    # Cover File Drop Box
    stegoLabel = QLabel("Stego File:")
    stegoLabel.setStyleSheet("margin-left: 10px;font-style: italic;")
    layout.addWidget(stegoLabel)
    
    stegoDropBoxLayout = QHBoxLayout()
    stegoPreviewStack = QStackedWidget()
    stegoPreviewStack.addWidget(QLabel("Stego File Preview"))  # Add QLabel for images
    stegoDropBox = FileDropBox(['.*', '.png', '.jpg', '.jpeg', '.bmp', '.gif', '.mp4', '.avi', '.mov', '.mkv', '.wav', '.mp3', '.ogg', '.flac', '.m4a', '.aac'], stegoPreviewStack)
    stegoDropBoxLayout.addWidget(stegoDropBox)
    stegoPreviewStack.setStyleSheet("margin-left: 80px;height: 100px;width: 100px;")
    stegoDropBoxLayout.addWidget(stegoPreviewStack)
    layout.addLayout(stegoDropBoxLayout)
    
    # No. of LSB Cover Object Bits ComboBox
    lsbLabel = QLabel("No. of LSB Cover Object Bits: ")
    lsbLabel.setStyleSheet("margin-left: 10px;font-style: italic;")
    layout.addWidget(lsbLabel)
    lsbComboBox = QComboBox()
    lsbComboBox.addItems([str(i) for i in range(1, 9)])  # Add items "1" to "8"
    lsbComboBox.setStyleSheet("margin-left: 10px;font-size: 15px;padding: 5px;")
    layout.addWidget(lsbComboBox)

    # Decode Function
    def decode():
        
        if stegoDropBox.text() == "Drag and drop a file here \nor \nclick to select":
            msgBox = QMessageBox(win)
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setWindowTitle("Stego File Not Selected")
            msgBox.setText("Please select a stego file.")
            msgBox.setStyleSheet("border: 0px;")
            msgBox.exec_()
            return
        
        stegoFilePath = stegoDropBox.text()
        lsb = int(lsbComboBox.currentText())

        try:
            decoder = Steganography()
            if stegoFilePath.lower().endswith(('.mp4', '.avi', '.mov', '.mkv')):
                result = decoder.decode_steganography_video(stegoFilePath, lsb)
            else:
                result = decoder.decode(stegoFilePath, lsb)

            msgBox = QMessageBox(win)
            msgBox.setText(result.get("message"))
            msgBox.setStyleSheet("border: 0px; padding: 10px; height: 100px; width: 300px;")
            
            if result.get("status") is False:
                msgBox.setIcon(QMessageBox.Warning)
                msgBox.setWindowTitle("Error")
            else:
                msgBox.setIcon(QMessageBox.Information)
                msgBox.setWindowTitle("Success")
            
            msgBox.exec_()
        except Exception as e:
            msgBox = QMessageBox(win)
            msgBox.setIcon(QMessageBox.Critical)
            msgBox.setWindowTitle("Decoding Error")
            msgBox.setText(f"An error occurred while decoding: {str(e)}")
            msgBox.setStyleSheet("border: 0px;")
            msgBox.exec_()

    # Button above Down Arrow Icon
    button = QPushButton("Decode")
    button.setStyleSheet("margin-left: 10px;height: 40px;margin-top: 30px;font-weight: bold;font-size: 15px;background-color: #bc88f7;")
    layout.addWidget(button)
    button.clicked.connect(decode)

    # Down Arrow Icon
    downArrowIcon = QLabel()
    downArrowmap = QPixmap("./img/down-arrow.png")
    downArrowmap = downArrowmap.scaled(20, 20, Qt.KeepAspectRatio, Qt.SmoothTransformation)
    downArrowIcon.setPixmap(downArrowmap)
    downArrowIcon.setStyleSheet("margin: 20px;padding-left: 220px;")
    layout.addWidget(downArrowIcon)
    downArrowIcon.hide() # hide the arrow first

    scroll = QScrollArea()
    scroll.setWidget(widget)
    win.setCentralWidget(scroll)

    win.show()
    app.exec_()

if __name__ == '__main__':
    window()
