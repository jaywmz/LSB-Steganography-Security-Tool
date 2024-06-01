from PyQt5.QtWidgets import (QFrame, QDialog, QApplication, QMainWindow, QPushButton, 
                             QSpacerItem, QSizePolicy, QVBoxLayout, QHBoxLayout, 
                             QWidget, QScrollArea, QLabel, QFileDialog, QMessageBox, 
                             QComboBox, QStackedWidget)
from PyQt5.QtCore import Qt, pyqtSignal, QUrl, QSize
from PyQt5.QtGui import QDragEnterEvent, QDropEvent, QMouseEvent, QIcon, QPixmap, QMovie
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
import os
import vlc
import sys
import time
from steganography import Steganography

class FileDropBox(QLabel):
    def __init__(self, valid_extensions, preview_stack, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.valid_extensions = valid_extensions
        self.preview_stack = preview_stack
        self.valid_file_path = None
        
        # VLC player initialization
        self.instance = vlc.Instance()
        self.player = self.instance.media_player_new()
        self.video_widget = QFrame()
        self.preview_stack.addWidget(self.video_widget)
        
        # Play button initialization
        self.play_button = QPushButton("Play/Pause", self)
        self.play_button.clicked.connect(self.play_video)
        self.play_button.move(10, 10)  # Set the position of the play button
        self.play_button.hide()  # Hide the play button initially
        
        # Restart button initialization
        self.restart_button = QPushButton("Restart", self)
        self.restart_button.clicked.connect(self.restart_video)
        self.restart_button.move(100, 10)  # Set the position of the restart button
        self.restart_button.hide()  # Hide the restart button initially

        # Test Preview Button
        self.test_button = QPushButton("Test", self)
        self.test_button.clicked.connect(self.test_me)
        self.test_button.move(20, 30)
        self.test_button.hide()
        
        self.setText("Drag and drop a file here \nor \nclick to select")
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet("border: 2px dashed #aaa; margin-left: 10px;")
        self.setAcceptDrops(True)
        self.setMinimumSize(200, 100)
        self.setAcceptDrops(True)

    # This is a test for PreviewWindow
    def test_me(self):
        print("Test")
        # Create a preview window
        self.preview_window = PreviewWindow(self.valid_file_path, self.valid_file_path, self)
        self.preview_window.show()

    def play_video(self):
        if self.player.get_state() == vlc.State.Paused:
            self.player.play()
        else:
            self.player.pause()
            
    def restart_video(self):
        self.player.stop()
        self.player.set_media(self.media)
        self.player.set_hwnd(int(self.video_widget.winId()))
        self.player.set_position(0.0)
        self.player.play()
                        
    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
            
    def is_video_file(self, filename):
        return filename.lower().endswith(('.mp4', '.avi', '.mov', '.mkv'))

    def dropEvent(self, event: QDropEvent):
        if event.mimeData().hasUrls():
            url = event.mimeData().urls()[0]
            file_path = url.toLocalFile()
            if file_path is None:
                self.preview_stack.setCurrentWidget(QLabel("Cover File Preview"))
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
            self.play_button.hide()
            self.restart_button.hide()
            pixmap = QPixmap(file_path)
            pixmap = pixmap.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.preview_stack.setCurrentIndex(0)
            self.preview_stack.currentWidget().setPixmap(pixmap)
            self.valid_file_path = file_path
        elif file_path.lower().endswith(('.mp4', '.avi', '.mov', '.mkv', '.wav', '.mp3', '.ogg', '.flac', '.m4a', '.aac')):
            self.player.stop()
            media = self.instance.media_new(file_path)
            self.media = media
            self.player.set_media(media)
            self.player.set_hwnd(int(self.video_widget.winId()))
            self.player.play()
            self.preview_stack.setCurrentIndex(1)
            self.valid_file_path = file_path
            self.play_button.show()
            self.restart_button.show()
        elif file_path.lower().endswith('.txt'):
            with open(file_path, 'r') as file:
                content = file.read(1000)
            if len(content) == 1000:
                content += '...'
            self.preview_stack.currentWidget().setText(content)
        else:
            self.preview_stack.setCurrentWidget(QLabel("Cover File Preview"))
            msgBox = QMessageBox(self)
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setWindowTitle("Invalid File Type")
            msgBox.setText("Please drag and drop a file of type: " + ", ".join(self.valid_extensions))
            msgBox.setStyleSheet("border: 0px;")
            msgBox.exec_()

    def handle_error(self):
        error = self.player.get_state()
        if error != vlc.State.Error:
            error_message = self.player.get_state()
            print(f"Error: {error_message}")
            msgBox = QMessageBox(self)
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setWindowTitle("Error")
            msgBox.setText(f"Error: {error_message}")
            msgBox.setStyleSheet("border: 0px;")
            msgBox.exec_()

class PreviewWindow(QDialog):
    def __init__(self, input_file_path, output_file_path, parent=None):
        super().__init__(parent)
        print(f"Input File Path: {input_file_path}")
        print(f"Output File Path: {output_file_path}")
        self.setWindowTitle('Before and After Preview')
        self.resize(400, 400)
        
        self.setStyleSheet("")
        
        self.layout = QHBoxLayout()
        self.before_layout = QVBoxLayout()
        self.after_layout = QVBoxLayout()
        
        self.before_label = QLabel("Before Encoding:")
        self.before_layout.addWidget(self.before_label)
        self.before_image_label = QLabel()  # Create a new label for the image/GIF
        self.before_layout.addWidget(self.before_image_label)  # Add the new label to the layout
        self.before_preview_stack = QStackedWidget()
        self.before_instance = vlc.Instance()
        self.before_player = self.before_instance.media_player_new()
        self.before_video_widget = QFrame()
        self.before_video_widget.setFixedSize(400, 300)
        self.before_preview_stack.setStyleSheet("background-color: blue;")
        self.before_preview_stack.addWidget(self.before_video_widget)
        self.before_layout.addWidget(self.before_preview_stack)
        self.before_play_button = QPushButton("Play/Pause", self)
        self.before_play_button.clicked.connect(self.before_play_video)
        self.before_layout.addWidget(self.before_play_button)
        self.before_play_button.hide()
        self.before_restart_button = QPushButton("Restart", self)
        self.before_restart_button.clicked.connect(self.before_restart_video)
        self.before_layout.addWidget(self.before_restart_button)
        self.before_restart_button.hide()
        
        self.after_label = QLabel("After Encoding:")
        self.after_layout.addWidget(self.after_label)
        self.after_image_label = QLabel()  # Create a new label for the image/GIF
        self.after_layout.addWidget(self.after_image_label)
        self.after_preview_stack = QStackedWidget()
        self.after_instance = vlc.Instance()
        self.after_player = self.after_instance.media_player_new()
        self.after_video_widget = QFrame()
        self.after_video_widget.setFixedSize(400, 300)  # Set the size of the video widget
        self.after_preview_stack.setStyleSheet("background-color: blue;")
        self.after_preview_stack.addWidget(self.after_video_widget)
        self.after_layout.addWidget(self.after_preview_stack)
        self.after_play_button = QPushButton("Play/Pause", self)
        self.after_play_button.clicked.connect(self.after_play_video)
        self.after_layout.addWidget(self.after_play_button)
        self.after_play_button.hide()
        self.after_restart_button = QPushButton("Restart", self)
        self.after_restart_button.clicked.connect(self.after_restart_video)
        self.after_layout.addWidget(self.after_restart_button)
        self.after_restart_button.hide()
        
        self.layout.addLayout(self.before_layout)
        self.layout.addLayout(self.after_layout)
        self.setLayout(self.layout)

        if input_file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):
            # Display image
            self.before_preview_stack.hide()
            pixmap = QPixmap(input_file_path)
            pixmap = pixmap.scaled(400, 300, Qt.KeepAspectRatio)  # Scale the pixmap
            self.before_image_label.setPixmap(pixmap)
        elif input_file_path.lower().endswith('.gif'):
            # Display animated GIF
            self.before_preview_stack.hide()
            movie = QMovie(input_file_path)
            movie.setScaledSize(QSize(400, 300))  # Scale the movie
            self.before_image_label.setMovie(movie)
            movie.start()
        elif input_file_path.lower().endswith(('.mp4', '.avi', '.mov', '.mkv', '.wav', '.mp3', '.ogg', '.flac', '.m4a', '.aac')):
            # Play video
            self.before_player.set_media(self.before_instance.media_new(input_file_path))
            self.before_player.set_hwnd(self.before_video_widget.winId())  # Add this line
            self.before_player.play()
            self.before_play_button.show()
            self.before_restart_button.show()
            self.before_image_label.hide()
        else:
            self.before_label.setText("Input file is not an image or a video.")

        # Check if the output file is an image or a video
        if output_file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):
            # Display image
            self.after_preview_stack.hide()
            pixmap = QPixmap(output_file_path)
            pixmap = pixmap.scaled(400, 300, Qt.KeepAspectRatio)  # Scale the pixmap
            self.after_image_label.setPixmap(pixmap)
        elif output_file_path.lower().endswith('.gif'):
            # Display animated GIF
            self.after_preview_stack.hide()
            movie = QMovie(output_file_path)
            movie.setScaledSize(QSize(400, 300))  # Scale the movie
            self.after_image_label.setMovie(movie)
            movie.start()
        elif output_file_path.lower().endswith(('.mp4', '.avi', '.mov', '.mkv', '.wav', '.mp3', '.ogg', '.flac', '.m4a', '.aac')):
            # Play video
            self.after_player.set_media(self.after_instance.media_new(output_file_path))
            self.after_player.set_hwnd(self.after_video_widget.winId())  # Add this line
            self.after_player.play()
            self.after_play_button.show()
            self.after_restart_button.show()
            self.after_image_label.hide()
        else:
            self.after_label.setText("Output file is not an image or a video.")
        
    def closeEvent(self, event):
        
        self.before_player.stop()
        self.after_player.stop()
        time.sleep(0.5)
        
        self.before_player.set_media(None)
        self.after_player.set_media(None)
        event.accept()  
    
    def before_play_video(self):
        if self.before_player.get_state() == vlc.State.Paused:
            self.before_player.play()
        else:
            self.before_player.pause()
    
    def after_play_video(self):
        if self.after_player.get_state() == vlc.State.Paused:
            self.after_player.play()
        else:
            self.after_player.pause()
            
    def before_restart_video(self):
        self.before_player.stop()
        self.before_player.set_media(self.before_player.get_media())
        self.before_player.set_hwnd(int(self.before_video_widget.winId()))
        self.before_player.set_position(0.0)
        self.before_player.play()

    def after_restart_video(self):
        self.after_player.stop()
        self.after_player.set_media(self.after_player.get_media())
        self.after_player.set_hwnd(int(self.after_video_widget.winId()))
        self.after_player.set_position(0.0)
        self.after_player.play()
    
def encoder_window():
    
    global stegoFilePath, payloadFilePath, coverFilePath, lsb
    stegoFilePath = ""
    payloadFilePath = ""
    coverFilePath = ""
    lsb = 0
    
    # app = QApplication([])
    # win = QMainWindow()
    # win.setWindowTitle("LSB Steganography Encoder")
    # win.resize(600, 750)

    # Main Window Widget
    widget = QWidget()
    layout = QVBoxLayout(widget)

    # Title
    titleLabel = QLabel("LSB Steganography Encoder")
    titleLabel.setStyleSheet("font-size: 20px;margin: 10px;text-decoration: underline;")
    layout.addWidget(titleLabel)
    
    # Cover File Drop Box
    coverLabel = QLabel("Cover File:")
    coverLabel.setStyleSheet("margin-left: 10px;font-style: italic;")
    layout.addWidget(coverLabel)
    
    coverDropBoxLayout = QHBoxLayout()
    coverPreviewStack = QStackedWidget()
    coverPreviewStack.addWidget(QLabel("Cover File Preview"))  # Add QLabel for images
    coverDropBox = FileDropBox(['.png', '.jpg', '.jpeg', '.bmp', '.gif', '.mp4', '.avi', '.mov', '.mkv', '.wav', '.mp3', '.ogg', '.flac', '.m4a', '.aac'], coverPreviewStack)
    coverDropBoxLayout.addWidget(coverDropBox)
    coverPreviewStack.setStyleSheet("margin-left: 80px;height: 100px;width: 100px;")
    coverDropBoxLayout.addWidget(coverPreviewStack)
    layout.addLayout(coverDropBoxLayout)
    
    # Plus Icon
    plusIcon = QLabel()
    plusmap = QPixmap("./img/plus.png")
    plusmap = plusmap.scaled(20, 20, Qt.KeepAspectRatio, Qt.SmoothTransformation)
    plusIcon.setPixmap(plusmap)
    plusIcon.setStyleSheet("margin: 20px;padding-left: 220px;")
    layout.addWidget(plusIcon)
    
    # Payload File Drop Box
    payloadLabel = QLabel("Payload File:")
    payloadLabel.setStyleSheet("margin-left: 10px;font-style: italic;")
    layout.addWidget(payloadLabel)
    
    payloadDropBoxLayout = QHBoxLayout()
    payloadPreviewStack = QStackedWidget()
    payloadPreviewStack.addWidget(QLabel("Payload File Preview"))  # Add QLabel for text files
    payloadDropBox = FileDropBox(['.txt'], payloadPreviewStack)
    payloadDropBoxLayout.addWidget(payloadDropBox)
    payloadPreviewStack.setStyleSheet("margin-left: 80px;height: 100px;width: 100px;")
    payloadDropBoxLayout.addWidget(payloadPreviewStack)
    layout.addLayout(payloadDropBoxLayout)
        
    # Plus Icon
    anotherPlusIcon = QLabel()
    anotherPlusmap = QPixmap("./img/plus.png")
    anotherPlusmap = anotherPlusmap.scaled(20, 20, Qt.KeepAspectRatio, Qt.SmoothTransformation)
    anotherPlusIcon.setPixmap(anotherPlusmap)
    anotherPlusIcon.setStyleSheet("margin: 20px;padding-left: 220px;")
    layout.addWidget(anotherPlusIcon)
    
    # No. of LSB Cover Object Bits ComboBox
    lsbLabel = QLabel("No. of LSB Cover Object Bits: ")
    lsbLabel.setStyleSheet("margin-left: 10px;font-style: italic;")
    layout.addWidget(lsbLabel)
    lsbComboBox = QComboBox()
    lsbComboBox.addItems([str(i) for i in range(1, 9)])  # Add items "1" to "8"
    lsbComboBox.setStyleSheet("margin-left: 10px;font-size: 15px;padding: 5px;")
    layout.addWidget(lsbComboBox)

    # Plus Icon
    andAnotherPlusIcon = QLabel()
    andAnotherPlusmap = QPixmap("./img/plus.png")
    andAnotherPlusmap = andAnotherPlusmap.scaled(20, 20, Qt.KeepAspectRatio, Qt.SmoothTransformation)
    andAnotherPlusIcon.setPixmap(andAnotherPlusmap)
    andAnotherPlusIcon.setStyleSheet("margin: 20px;padding-left: 220px;")
    layout.addWidget(andAnotherPlusIcon)

    # Select Directory Function
    def selectDir():
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        output_dir = QFileDialog.getExistingDirectory(None, "Select Directory", "", options=options)
        
        # Change the button text
        dirButton.setText(output_dir)

    # Select Directory Button
    dirLabel = QLabel("Select Output Directory:")
    dirLabel.setStyleSheet("margin-left: 10px;font-style: italic;")
    layout.addWidget(dirLabel)
    dirButton = QPushButton("Select Directory")
    dirButton.setStyleSheet("margin-left: 10px;font-size: 15px;height: 20px;padding: 5px;")
    dirButton.clicked.connect(selectDir)
    layout.addWidget(dirButton)

    # Encode Function
    def encode():
        if coverDropBox.text() == "Drag and drop a file here \nor \nclick to select":
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setWindowTitle("Cover File Not Selected")
            msgBox.setText("Please select a cover file.")
            msgBox.setStyleSheet("border: 0px;")
            msgBox.exec_()
            return
        if payloadDropBox.text() == "Drag and drop a file here \nor \nclick to select":
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setWindowTitle("Payload File Not Selected")
            msgBox.setText("Please select a payload file.")
            msgBox.setStyleSheet("border: 0px;")
            msgBox.exec_()
            return
        if dirButton.text() == "Select Directory" or dirButton.text() == "":
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setWindowTitle("Output Directory Not Selected")
            msgBox.setText("Please select an output directory.")
            msgBox.setStyleSheet("border: 0px;")
            msgBox.exec_()
            return  
        
        coverFilePath = coverDropBox.text()
        payloadFilePath = payloadDropBox.text()
        lsb = int(lsbComboBox.currentText())
        output_dir = dirButton.text()
        
        print(f"Cover File Path: {coverFilePath}")
        print(f"Payload File Path: {payloadFilePath}")
        print(f"LSB: {lsb}")
        print(f"Output Directory: {output_dir}")
        
        with open(payloadFilePath, 'r') as file:
            payload = file.read()
            
        encoder = Steganography()
        if coverFilePath.lower().endswith(('.mp4', '.avi', '.mov', '.mkv')):
            result = encoder.encode_steganography_video(coverFilePath, payload, lsb, output_dir)
        else:
            result = encoder.encode(coverFilePath, payload, lsb, output_dir)
        
        msgBox = QMessageBox()
        msgBox.setText(result.get("message"))
        msgBox.setStyleSheet("border: 0px;")
        
        if result.get("status") is False:
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setWindowTitle("Error")
            preview_bool = False
        else:
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setWindowTitle("Success")
            preview_bool = True

        msgBox.exec_()
        
        if preview_bool is False:
            return
        else:
            preview_window = PreviewWindow(coverFilePath, result.get("output_file_path"))
            preview_window.exec_()
        
        ## What to do next?
    
    # Button above Down Arrow Icon
    button = QPushButton("Encode")
    button.setStyleSheet("margin-left: 10px;height: 40px;margin-top: 30px;font-weight: bold;font-size: 15px;background-color: #8f88f7;")
    layout.addWidget(button)
    button.clicked.connect(encode)
    
    scroll = QScrollArea()
    scroll.setWidget(widget)
    
    return scroll
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    encoder_window()
    sys.exit(app.exec_())
