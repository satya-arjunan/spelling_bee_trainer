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
import random
from PyDictionary import PyDictionary

dictionary = PyDictionary()
db_filename = "database.csv"
words_filename = "words8.csv"
recent_count = 5

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
        self.index = -1
        self.is_checked = True
        if not os.path.isfile(db_filename):
            words = pd.read_csv(words_filename).columns.to_list()
            self.df = pd.DataFrame(words, columns=["words"]) 
            self.df["incorrect_count"] = 0
            self.df["correct_count"] = 0
            self.df["meaning"] = ""
            self.df["synonym"] = ""
            self.df["antonym"] = ""
        else:
            self.df = pd.read_csv(db_filename)

    def reset(self):
        return

    def initialise_ui(self):
        vbox = QVBoxLayout()
        vbox2 = QVBoxLayout()
        vbox3 = QVBoxLayout()
        vbox4 = QVBoxLayout()
        hbox = QHBoxLayout()
        hbox2 = QHBoxLayout()
        self.e1 = QLineEdit()
        self.e1.setFont(QFont("Arial", 20))
        self.e_meaning = QPlainTextEdit()
        self.e_meaning.setFont(QFont("Arial", 10))
        self.e_synonym = QPlainTextEdit()
        self.e_synonym.setFont(QFont("Arial", 10))
        self.e_antonym = QPlainTextEdit()
        self.e_antonym.setFont(QFont("Arial", 10))
        self.lbl_meaning = QLabel('Meaning:')
        label2 = QLabel('Synonym:')
        label3 = QLabel('Antonym:')
        btn1 = QPushButton(QIcon(QApplication.style().standardIcon(
            QStyle.SP_DialogApplyButton)), "Check", self)
        btn2 = QPushButton(QIcon(QApplication.style().standardIcon(
            QStyle.SP_ArrowForward)), "Next", self)
        btn3 = QPushButton(QIcon(QApplication.style().standardIcon(
            QStyle.SP_DialogCancelButton)), "Exit", self)
        btn4 = QPushButton(QIcon(QApplication.style().standardIcon(
            QStyle.SP_BrowserReload)), "Repeat", self)
        btn5 = QPushButton(QIcon(QApplication.style().standardIcon(
            QStyle.SP_DesktopIcon)), "Offline", self)
        btn6 = QPushButton(QIcon(QApplication.style().standardIcon(
            QStyle.SP_DialogSaveButton)), "Save", self)
        self.e1.returnPressed.connect(self.return_pressed)
        btn1.clicked.connect(self.check)
        btn2.clicked.connect(self.next)
        btn3.clicked.connect(self.quit)
        btn4.clicked.connect(self.repeat)
        btn5.clicked.connect(self.offline)
        btn6.clicked.connect(self.save)
        hbox.addWidget(self.e1)
        hbox.addWidget(btn1)
        hbox.addWidget(btn2)
        hbox.addWidget(btn4)
        hbox.addWidget(btn5)
        hbox.addWidget(btn6)
        hbox.addWidget(btn3)
        vbox2.addWidget(self.lbl_meaning)
        vbox2.addWidget(self.e_meaning)
        vbox3.addWidget(label2)
        vbox3.addWidget(self.e_synonym)
        vbox4.addWidget(label3)
        vbox4.addWidget(self.e_antonym)
        hbox2.addLayout(vbox2)
        hbox2.addLayout(vbox3)
        hbox2.addLayout(vbox4)
        vbox.addLayout(hbox)
        vbox.addLayout(hbox2)
        self.setLayout(vbox)

    def quit(self):
        self.save()
        QApplication.instance().quit()

    def return_pressed(self):
        if self.is_checked:
            self.next()
        else:
            self.check()

    def update_statusbar(self, msg):
        self.parent.statusbar.showMessage(msg)
        self.repaint()
        self.parent.repaint()

    def offline(self):
        for index in self.df.index:
            if self.df.meaning[index] == "":
                word = self.df.words[index]
                self.update_statusbar(f"downloading {word}...")
                self.df.meaning[index] = str(dictionary.meaning(word))
                self.df.synonym[index] = str(dictionary.synonym(word))
                self.df.antonym[index] = str(dictionary.antonym(word))
                self.update_statusbar("Done.")
        return
    
    def save(self):
        self.df.to_csv(db_filename, index=False)
    
    def update_dictionary(self, index):
        word = self.df.words[index]
        self.lbl_meaning.setText(f"Meaning of {word}:")
        self.e_meaning.setPlainText(self.df.meaning[index])
        self.e_synonym.setPlainText(self.df.synonym[index])
        self.e_antonym.setPlainText(self.df.antonym[index])

    def check(self):
        if (self.index >= 0):
            answer = self.e1.text().lower()
            word = self.df.words[self.index].lower()
            self.update_dictionary(self.index)
            if (answer == word):
                msg = "That is correct!"
                if not self.is_checked:
                    self.df.correct_count[self.index] += 1 
            elif (answer != ""):
                msg = ("I'm sorry, that is incorrect. The correct spelling" +
                       " is '" + word + "'")
                if not self.is_checked:
                    self.df.incorrect_count[self.index] += 1
            else:
                msg = "Ready"
        else:
            msg = "Click on Next to start"
        self.is_checked = True
        self.update_statusbar(msg)

    def update_index(self):
        self.is_checked = False
        indices = self.df[self.df.correct_count == 0].index
        # if all words have at least one correct count:
        if (len(indices) == 0):
            max_incorrect = self.df.incorrect_count.max()
            if (max_incorrect == 0):
                self.index = -1
                return
            indices = self.df[self.df.incorrect_count == max_incorrect].index
        print("choices:", 
            self.df.words[indices[:min(recent_count, len(indices))]])
        self.index = random.choice(indices[:min(recent_count, len(indices))])
        
    def repeat(self):
        if (self.index >= 0):
            word = self.df.words[self.index]
            filename = f"{word}.mp3"
            if os.path.isfile(filename):
                playsound(filename)
        
    def next(self):
        if not self.is_checked:
            self.check()
        self.e1.setText("")
        self.parent.statusbar.showMessage("Ready")
        self.repaint()
        self.update_index()
        if (self.index >= 0):
            word = self.df.words[self.index]
            obj = gTTS(text=word, lang="en", slow=False)
            filename = f"{word}.mp3"
            if not os.path.isfile(filename):
                obj.save(filename)
            playsound(filename)

def main():
    myappid = u"mycompany.myproduct.subproduct.version" # arbitrary string
    #ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    app = QApplication(sys.argv)
    w = MainWindow()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
