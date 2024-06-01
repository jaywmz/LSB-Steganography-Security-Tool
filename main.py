import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout
from encoder_main import encoder_window
from decoder_main import decoder_window

def main():
    global stegoFilePath, payloadFilePath, coverFilePath, lsb
    stegoFilePath = ""
    payloadFilePath = ""
    coverFilePath = ""
    lsb = 0

    app = QApplication([])
    win = QMainWindow()
    win.setWindowTitle("LSB Steganography Tool")
    win.resize(600, 400)

    tab_widget = QTabWidget()

    encoder_tab = QWidget()
    decoder_tab = QWidget()

    encoder_layout = QVBoxLayout()
    decoder_layout = QVBoxLayout()

    encoder_ui = encoder_window()
    encoder_layout.addWidget(encoder_ui)

    decoder_ui = decoder_window()
    decoder_layout.addWidget(decoder_ui)

    encoder_tab.setLayout(encoder_layout)
    decoder_tab.setLayout(decoder_layout)

    tab_widget.addTab(encoder_tab, "Encoding")
    tab_widget.addTab(decoder_tab, "Decoding")

    win.setCentralWidget(tab_widget)

    win.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()