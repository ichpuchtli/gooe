#!/usr/bin/python2

try:
    from PyQt4 import QtGui, QtCore
except ImportError:
    from PySide import QtGui, QtCore

import random
import math
import os
from util import SysCtl
from wavfile import WavFileReader

class WaveFormSlot(QtGui.QWidget):

    def __init__(self, num, width, height, parent = None):
        super(WaveFormSlot, self).__init__(parent)

        self.width = width
        self.height = height

        # WaveForm Widget
        ##################################################
        self.waveformWidgetContainer = QtGui.QGroupBox("Waveform", self)
        self.waveformWidgetLayout = QtGui.QHBoxLayout(self)

        # Waveform Area instance
	self.waveformArea = WaveformPaintArea(self, width, height)

        self.waveformWidgetLayout.addWidget(self.waveformArea)
        self.waveformWidgetContainer.setLayout(self.waveformWidgetLayout)

        # Option Form Widget
        ##################################################
        self.formWidgetContainer = QtGui.QGroupBox("Form layout", self)
        self.formWidgetLayout = QtGui.QHBoxLayout(self)

        # WaveOptionForm instance
        self.optionForm = WaveOptionForm(self)

        self.formWidgetLayout.addWidget(self.optionForm)
        self.formWidgetContainer.setLayout(self.formWidgetLayout)

        # Slot Layout
        ##################################################
        self.slotLayout = QtGui.QHBoxLayout()
        self.slotLayout.addWidget(self.waveformWidgetContainer)
        self.slotLayout.addWidget(self.formWidgetContainer)
        self.setLayout(self.slotLayout)

        self.setSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Minimum)

        self.setAcceptDrops(True)

        self.waveFilePath = ""
        self.waveFileName = ""
        
        self.dataSet = []

        self.num = num

    def sizeHint(self):
        return QtCore.QSize(self.width, self.height)

    def dragEnterEvent(self, e):
        e.acceptProposedAction()

    def dropEvent(self, e):
        path = e.mimeData().urls()[0].toLocalFile().toLocal8Bit().data()
        if os.path.isfile(path):
            QtCore.qDebug(path)

            self.waveFilePath = path
            self.waveFileName = os.path.basename(path)
            QtCore.qDebug(self.waveFileName)

            SysCtl.mkdir("tmp")

            copypath = "tmp/raw" + str(self.num) + ".wav"

            SysCtl.copyFile(path, copypath)
            
            self.waveformArea.updateDataSet(copypath)
            #TODO import wave dialog with progress bar
            #TODO emit update data set
        
class WaveformPaintArea(QtGui.QWidget):

  def __init__(self, parent, width, height):
    super(WaveformPaintArea, self).__init__(parent)

    self.width = width
    self.height = height

    self.dataSet = []
    self.wavfile = None

  def sizeHint(self):
      return QtCore.QSize(self.width, self.height)

  #Slot
  def updateDataSet(self, wavfile):
      self.wavfile = WavFileReader(wavfile)
      self.dataSet = self.wavfile.getData()
      self.update()

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
  
    step = len(self.dataSet) / 2

    for i in range(step):
      y = self.height/2 + self.dataSet[i*2] / 500
      x = int(i * self.width / step)
      painter.drawPoint(x, y)

class WaveOptionForm(QtGui.QWidget):

    def __init__(self, parent):
        super(WaveOptionForm, self).__init__(parent)

        layout = QtGui.QFormLayout(self)
        layout.addRow(QtGui.QLabel("Line 1:"), QtGui.QLineEdit())
        layout.addRow(QtGui.QLabel("Line 2, long text:"), QtGui.QComboBox())
        layout.addRow(QtGui.QLabel("Line 3:"), QtGui.QSpinBox())
        self.setLayout(layout)
    

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

    def selectButton(self):
      pass
    #TODO change font-weight slot indicate when a button has a sample
