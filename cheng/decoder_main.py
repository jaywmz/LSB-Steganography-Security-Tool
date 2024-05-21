from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QScrollArea, QLabel, QFileDialog, QMessageBox, QMenu, QMenuBar, QAction, QComboBox, QStackedWidget
from PyQt5.QtCore import Qt, pyqtSignal, QUrl
from PyQt5.QtGui import QDragEnterEvent, QDropEvent, QMouseEvent, QIcon, QPixmap
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PIL import Image, ImageTk
from steganography import Steganography

class FileDropBox(QLabel):
    def __init__(self, valid_extensions, preview_stack, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.valid_extensions = valid_extensions
        self.preview_stack = preview_stack
        
        self.player = QMediaPlayer()
        self.player.error.connect(self.handle_error)
        self.video_widget = QVideoWidget()
        self.player.setVideoOutput(self.video_widget)
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
            self.player.setMedia(QMediaContent())
            pixmap = QPixmap(file_path)
            pixmap = pixmap.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)  # Adjust the size as needed
            self.preview_stack.setCurrentIndex(0)  # Switch to QLabel
            self.preview_stack.currentWidget().setPixmap(pixmap)
        elif file_path.lower().endswith(('.mp4', '.avi', '.mov', '.mkv', '.wav', '.mp3', '.ogg', '.flac', '.m4a', '.aac')):
            self.player.stop()  # Stop the player
            self.player.setMedia(QMediaContent())  # Clear the current media
            self.player.setMedia(QMediaContent(QUrl.fromLocalFile(file_path)))
            self.player.play()
            self.preview_stack.setCurrentIndex(1)  # Switch to QVideoWidget
        elif file_path.lower().endswith('.txt'):
            with open(file_path, 'r') as file:
                content = file.read(1000)  # Read the first 1000 characters
            if len(content) == 1000:
                content += '...'  # Add '...' to indicate that the content is truncated
            self.preview_stack.currentWidget().setText(content)

    def handle_error(self):
        error = self.player.error()
        if error != QMediaPlayer.NoError:
            error_message = self.player.errorString()
            print(f"Error: {error_message}")
            msgBox = QMessageBox(self)
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setWindowTitle("Error")
            msgBox.setText(error_message)
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
    
    # # Create a menu bar
    # menuBar = QMenuBar()
    # menuBar.setStyleSheet("background-color: #797979;")

    # # Encode Page
    # fileAction = QAction("Encode", win)
    # fileAction.triggered.connect(lambda: print("Encode action triggered"))
    # menuBar.addAction(fileAction)
    
    # # Decode Page
    # decodeAction = QAction("Decode", win)
    # decodeAction.triggered.connect(lambda: print("Decode action triggered"))
    # menuBar.addAction(decodeAction)
    
    # # Set the menu bar of the window
    # win.setMenuBar(menuBar)

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
    stegoDropBox = FileDropBox(['.png', '.jpg', '.jpeg', '.bmp', '.gif', '.mp4', '.avi', '.mov', '.mkv', '.wav', '.mp3', '.ogg', '.flac', '.m4a', '.aac'], stegoPreviewStack)
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
                        
        decoder = Steganography.decode(stegoFilePath, lsb)
        
        msgBox = QMessageBox(win)
        msgBox.setText(decoder.get("message"))
        msgBox.setStyleSheet("border: 0px; padding: 10px; height: 100px; width: 300px;")
        
        if decoder.get("status") is False:
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setWindowTitle("Error")
        else:
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setWindowTitle("Success")
        
        msgBox.exec_()
        
        ## What to do next?

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