from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
import ctypes
import sys
import pandas as pd
from playsound import playsound #pip install playsound==1.2.2 if has errors
from gtts import gTTS
import os

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__()
        self.main_widget = Widget(self)
        self.setCentralWidget(self.main_widget)
        self.initialise_ui()

    def initialise_ui(self):
        self.statusbar = self.statusBar()
        self.statusbar.showMessage('Ready')
        self.setWindowTitle("AVA Spelling Bee")
        self.setWindowIcon(QIcon(QApplication.style().standardIcon(
          QStyle.SP_FileDialogListView)))
        self.show()

class Widget(QWidget):
    def __init__(self, parent):
        super(Widget, self).__init__(parent)
        self.parent = parent
        self.initialise_ui()
        self.reset()
        self.count = 0
        self.words = pd.read_csv("words8.csv")

    def reset(self):
        return

    def initialise_ui(self):
        hbox = QHBoxLayout()
        btn1 = QPushButton(QIcon(QApplication.style().standardIcon(
            QStyle.SP_DialogOpenButton)), 'Input Folder', self)
        btn2 = QPushButton(QIcon(QApplication.style().standardIcon(
            QStyle.SP_DialogOpenButton)), 'Output Folder', self)
        btn3 = QPushButton(QIcon(QApplication.style().standardIcon(
            QStyle.SP_DialogApplyButton)), 'Next', self)
        btn4 = QPushButton(QIcon(QApplication.style().standardIcon(
            QStyle.SP_DialogCancelButton)), 'Exit', self)
        btn1.clicked.connect(self.select_input_folder)
        btn2.clicked.connect(self.select_output_folder)
        btn3.clicked.connect(self.next)
        btn4.clicked.connect(QApplication.instance().quit)
        hbox.addWidget(btn1)
        hbox.addWidget(btn2)
        hbox.addWidget(btn3)
        hbox.addWidget(btn4)
        self.setLayout(hbox)

    def select_input_folder(self):
        return

    def select_output_folder(self):
        return

    def next(self):
        if (self.count < len(self.words.columns)):
            word = self.words.columns[self.count]
            obj = gTTS(text=word, lang='en', slow=False)
            filename = f'{word}.mp3' 
            obj.save(filename)
            playsound(filename)
            os.remove(filename)
        self.count += 1

def main():
    myappid = u'mycompany.myproduct.subproduct.version' # arbitrary string
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    app = QApplication(sys.argv)
    w = MainWindow()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
