from PyQt5.QtCore import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys

import numpy as np
import cv2
from tensorflow import keras
import os

class MainWidget(QWidget):

   def __init__(self, *args, **kwargs):
      super(MainWidget, self).__init__(*args, **kwargs)
      mainLayout = QHBoxLayout()
      self.uploadPushButton = QPushButton("Upload Image...")
      self.uploadPushButton.setFixedSize(300, 70)
      self.uploadPushButton.clicked.connect(self.slotUploadPushButtonClicked)
      mainLayout.addWidget(self.uploadPushButton)
      self.setLayout(mainLayout)
      self.setFixedSize(800, 300)
      self.pashtoList = ['ا', 'ب', 'پ', 'ت', 'ټ', 'ث', 'ج', 'چ',
      'ح', 'خ', 'څ', 'ځ', 'د', 'ډ', 'ر', 'ړ', 'ز', 'ژ', 'ږ', 'س',
      'ش', 'ښ', 'ص', 'ض', 'ط', 'ظ', 'ع', 'غ', 'ف', 'ق', 'ک', 'ګ',
      'ل', 'م', 'ن', 'ڼ', 'و', 'ه', 'ء', 'ي', 'ې', 'ی', 'ئ']
      
   def slotUploadPushButtonClicked(self):
      #try:
      fname = QFileDialog.getOpenFileName(self, 'Open File', '', "Image Files (*.jpg *.png *.gif)")[0]
      self.model = keras.models.load_model('phasto.h5')
      img = cv2.imread(fname)
      img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
      img = cv2.resize(img, (28, 28))
      imgSum = np.sum(img)
      if imgSum > 99900:
         img = cv2.bitwise_not(img)
      img = img.reshape(1, 28, 28, 1)
      img = img / 255
      
      
      predictedLabel = self.model.predict(img).argmax()
      predictedChar = self.pashtoList[predictedLabel]
      print(predictedChar)
      self.msg = QMessageBox()
      self.msg.setText('The alphabet is ' + predictedChar)
      self.msg.show()
      """except:
         self.errMsg = QMessageBox()
         self.errMsg.setIcon(QMessageBox.Warning)
         self.errMsg.setText('Make sure that your input file is correct form. 28 * 28')
         self.errMsg.show()"""

      

app = QApplication(sys.argv)
w = MainWidget()
w.show()
app.exec_()