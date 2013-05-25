#!/usr/bin/python2

from PyQt4 import QtGui, QtCore

import random
import math

class WaveFormSlot(QtGui.QWidget):

    def __init__(self, parent):
        super(WaveFormSlot, self).__init__(parent)

        self.layout = QtGui.QHBoxLayout()
    
        # WaveForm Area contianer with label thing
	self.waveFormArea = WavePaintArea(self, 0, 0, 300, 80)

        self.waveformContainer = QtGui.QGroupBox("Waveform", self)
        self.waveformlayout = QtGui.QBoxLayout()
        self.waveformlayout.addWidget(self.waveFormArea)
        self.waveformContainer.setLayout(self.waveformlayout)

        self.optionForm = WaveOptionForm(self)

        self.layout.addWidget(self.waveFormArea)
        self.layout.addWidget(self.optionForm)

        self.setLayout(self.layout)

class WavePaintArea(QtGui.QWidget):

  def __init__(self, parent, pos_x, pos_y, width, height):
    super(WavePaintArea, self).__init__(parent)

    self.x = pos_x
    self.y = pos_y
    self.width = width
    self.height = height

    self.dataSet = []

    self.setGeometry(self.x, self.y, self.width, self.height)

  #Slot
  def updateDataSet(self, data):
      self.dataSet = data

  def paintEvent(self, event):

    painter = QtGui.QPainter()

    painter.begin(self)

    self.drawWaveForm(painter)

    painter.end()

  def drawWaveForm(self, painter):

    painter.setRenderHint(QtGui.QPainter.Antialiasing);

    pen = QtGui.QPen(QtGui.QColor(255,0,0))
    pen.setWidth(1) #pixel
    painter.setPen(pen)
  
    for i in range(self.width):
      x = i
      y = (1 + math.sin(x*(8*math.pi/self.width))) * self.height/4 + self.height/4
      painter.drawPoint(x, y)


class WaveOptionForm(QtGui.QWidget):

    def __init__(self, parent):
        super(WaveOptionForm, self).__init__(parent)

        self.formGroupBox = QtGui.QGroupBox("Form layout", self)
        layout = QtGui.QFormLayout(self)
        layout.addRow(QtGui.QLabel("Line 1:"), QtGui.QLineEdit())
        layout.addRow(QtGui.QLabel("Line 2, long text:"), QtGui.QComboBox())
        layout.addRow(QtGui.QLabel("Line 3:"), QtGui.QSpinBox())
        self.formGroupBox.setLayout(layout)
    

class MPCPadButton(QtGui.QPushButton):

    def __init__(self, title, parent, num):
        super(MPCPadButton, self).__init__(title, parent)
        self.setAcceptDrops(True)
        self.num = num

    def dragEnterEvent(self, e):
        QtCore.qDebug("MPCPadButton: dragEnterEvent(" + str(e) + ")" )
        e.acceptProposedAction()

    def dropEvent(self, e):
        QtCore.qDebug("MPCPadButton: dropEvent(" + str(e) + ")" )
        QtCore.qDebug(e.mimeData().text())

