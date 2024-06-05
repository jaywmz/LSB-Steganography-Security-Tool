# Import necessary modules
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout
from encoder_main import encoder_window
from decoder_main import decoder_window

# Define the main function
def main():
    # Declare global variables
    global stegoFilePath, payloadFilePath, coverFilePath, lsb
    # Initialize global variables
    stegoFilePath = ""
    payloadFilePath = ""
    coverFilePath = ""
    lsb = 0

    # Create a QApplication instance
    app = QApplication([])
    # Create a QMainWindow instance
    win = QMainWindow()
    # Set window title and size
    win.setWindowTitle("LSB Steganography Tool")
    win.resize(600,800)

    # Create a QTabWidget instance
    tab_widget = QTabWidget()

    # Create QWidget instances for the encoder and decoder tabs
    encoder_tab = QWidget()
    decoder_tab = QWidget()

    # Create QVBoxLayout instances for the encoder and decoder layouts
    encoder_layout = QVBoxLayout()
    decoder_layout = QVBoxLayout()

    # Create instances of the encoder and decoder windows
    encoder_ui = encoder_window()
    decoder_ui = decoder_window()

    # Add the encoder and decoder windows to their respective layouts
    encoder_layout.addWidget(encoder_ui)
    decoder_layout.addWidget(decoder_ui)

    # Set the layouts for the encoder and decoder tabs
    encoder_tab.setLayout(encoder_layout)
    decoder_tab.setLayout(decoder_layout)

    # Add the encoder and decoder tabs to the tab widget
    tab_widget.addTab(encoder_tab, "Encoding")
    tab_widget.addTab(decoder_tab, "Decoding")

    # Set the tab widget as the central widget of the main window
    win.setCentralWidget(tab_widget)

    # Show the main window
    win.show()
    # Execute the application and exit when it's done
    sys.exit(app.exec_())

# If this script is run as the main program, call the main function
if __name__ == '__main__':
    main()