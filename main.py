#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#
#        This file is part of Spellor
#
#        Copyright (C) 2022 Satya N.V. Arjunan
#
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#
#
# Spellor is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public
# License as published by the Free Software Foundation; either
# version 2 of the License, or (at your option) any later version.
# 
# Spellor is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public
# License along with Spellor -- see the file COPYING.
# If not, write to the Free Software Foundation, Inc.,
# 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
# 
#END_HEADER
#
# written by Satya N. V. Arjunan <satya.arjunan@gmail.com>

from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QFont
import ctypes
import sys
import pandas as pd
from playsound import playsound #pip install playsound==1.2.2 if has errors
from gtts import gTTS
import os

db_filename = "database.csv"

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__()
        self.main_widget = Widget(self)
        self.setCentralWidget(self.main_widget)
        self.initialise_ui()

    def initialise_ui(self):
        self.statusbar = self.statusBar()
        self.statusbar.showMessage("Ready")
        self.setWindowTitle("Aritya's Spellor")
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
        if not os.path.isfile(db_filename):
            words = pd.read_csv("words8.csv").columns.to_list()
            self.df = pd.DataFrame(words, columns=["words"]) 
            self.df["incorrect_count"] = -1
        else:
            self.df = pd.read_csv(db_filename)

    def reset(self):
        return

    def initialise_ui(self):
        hbox = QHBoxLayout()
        self.e1 = QLineEdit()
        self.e1.setFont(QFont("Arial", 20))
        btn1 = QPushButton(QIcon(QApplication.style().standardIcon(
            QStyle.SP_DialogApplyButton)), "Check", self)
        btn2 = QPushButton(QIcon(QApplication.style().standardIcon(
            QStyle.SP_ArrowForward)), "Next", self)
        btn3 = QPushButton(QIcon(QApplication.style().standardIcon(
            QStyle.SP_DialogCancelButton)), "Exit", self)
        self.e1.returnPressed.connect(self.check)
        btn1.clicked.connect(self.check)
        btn2.clicked.connect(self.next)
        btn3.clicked.connect(self.quit)
        hbox.addWidget(self.e1)
        hbox.addWidget(btn1)
        hbox.addWidget(btn2)
        hbox.addWidget(btn3)
        self.setLayout(hbox)

    def quit(self):
        self.df.to_csv(db_filename, index=False)
        QApplication.instance().quit()

    def check(self):
        if (self.count > 0):
            answer = self.e1.text().lower()
            word = self.df.words[self.count-1].lower()
            if (answer == word):
                msg = "That is correct!"
            else:
                msg = ("I'm sorry, that is incorrect. The correct spelling" +
                       " is '" + word + "'")
        else:
            msg = "Click on Next to start"
        self.parent.statusbar.showMessage(msg)
        self.repaint()

    def next(self):
        self.e1.setText("")
        self.parent.statusbar.showMessage("Ready")
        self.repaint()
        if (self.count < self.df.shape[0]):
            word = self.df.words[self.count]
            obj = gTTS(text=word, lang="en", slow=False)
            filename = f"{word}.mp3"
            obj.save(filename)
            playsound(filename)
            os.remove(filename)
        self.count += 1

def main():
    myappid = u"mycompany.myproduct.subproduct.version" # arbitrary string
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    app = QApplication(sys.argv)
    w = MainWindow()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
