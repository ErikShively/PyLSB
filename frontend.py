#!/usr/bin/env python3
import sys
import lsb
import filetype
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5 import QtCore
from pathlib import Path

class Dashboard(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    def initUI(self):
        #There should also be a picture preview here once that's taken care of
        self.label = QLabel()
        self.label.setStyleSheet("border: 2px solid")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.encode = QPushButton("Encode")
        self.encode.clicked.connect(self.func_encode)
        self.encode.setEnabled(False)
        self.decode = QPushButton("Decode")
        self.decode.clicked.connect(self.func_decode)
        self.decode.setEnabled(False)

        self.grid = QGridLayout()
        self.grid.setSpacing(5)

        self.grid.addWidget(self.label,0,0,1,2)
        self.grid.addWidget(self.encode,3,0)
        self.grid.addWidget(self.decode,3,1)
        self.setLayout(self.grid)
    def func_encode(self):
        home_dir = str(Path.home())
        #Dialog Box 1
        instructions_1 = QMessageBox.information(self,"Step 1","Select the file you wish to hide", QMessageBox.Ok)
        handle = QFileDialog.getOpenFileName(self, "Open file", home_dir,"Text or Images(*.txt *.jpg *.jpeg *.png)")[0]
        if(handle):
            open_success = steg.openFile(handle)
            if(open_success):
                instructions_2 = QMessageBox.information(self,"Step 2","Choose how you want to save the encoded image.", QMessageBox.Ok)
                handle = QFileDialog.getSaveFileName(self, "Save file", home_dir,"Text or Images(*.png)")[0]
                encode_success = steg.encodeImg(handle=handle)
                if(encode_success == False):
                    encode_fail = QMessageBox.warning(self,"Encode Failure","The file you chose is incompatible with the host image. Likely too big to store.", QMessageBox.Ok)

    def func_decode(self):
        print("Decoding")
        home_dir = str(Path.home())
        instructions_1 = QMessageBox.information(self,"Step 1","Choose how to save the decode. Note that you may just receive noise if the host wasn't encoded.", QMessageBox.Ok)
        handle = QFileDialog.getSaveFileName(self, "Save file", home_dir,"All Files(*.*)")[0]
        decode_success = steg.decodeImg(handle)
        if(decode_success):
            results = QMessageBox.information(self,"Success","File decoded and saved.", QMessageBox.Ok)
        else:
            results = QMessageBox.information(self,"Decode Failure","Something went wrong with the decode.", QMessageBox.Ok)


        #File dialog to save. Maybe a warning if it doesn't decode.


class Meta(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
    def initUI(self):
        self.dashboard = Dashboard()
        self.setCentralWidget(self.dashboard)
        self.setGeometry(200,200,500,400)

        self.open_image = QAction("&Open Host Image", self)
        self.menubar = self.menuBar()
        self.menu = self.menubar.addMenu('&File')
        self.menu.addAction(self.open_image)

        self.open_image.triggered.connect(self.func_open_image)

        self.setWindowTitle("PyLSB")

        self.show()

    def func_open_image(self):
        home_dir = str(Path.home())
        handle = QFileDialog.getOpenFileName(self, "Open file", home_dir,"Images(*.png *.jpg)")[0]
        if(handle):
            file_ready = True
            #Put in a JPG warning.
            if((filetype.guess(handle).extension == "jpg") | (filetype.guess(handle).extension == "jpeg")):
                jpg_warning = QMessageBox.question(self,"JPG Warning","JPG is a lossy format. If the image is encoded, it will be saved as a PNG file.", QMessageBox.Ok | QMessageBox.Cancel)
                if(jpg_warning == QMessageBox.Cancel):
                    file_ready = False
                    handle = ''
            if(file_ready):
                image_preview = QPixmap(handle).scaled(self.dashboard.label.width(),self.dashboard.label.height(),QtCore.Qt.KeepAspectRatio)
                self.dashboard.label.setPixmap(image_preview)
                self.dashboard.encode.setEnabled(True)
                self.dashboard.decode.setEnabled(True)
                steg.openHost(handle)



if __name__ == '__main__':

    #Because this program already calls its functionality from something that's designed to be called,
    #we shouldn't have to worry about calling any of the UI functions by themselves by including this in
    #another project. That's why it's fine to have a global steg frame declared here in main.

    steg = lsb.frame()

    app = QApplication(sys.argv)
    window = Meta()

    sys.exit(app.exec_())
