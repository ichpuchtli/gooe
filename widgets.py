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
import winsound
from filters import Filters
import numpy

class WaveFormSlot(QtGui.QWidget):

    def __init__(self, num, width, height, parent = None):
        super(WaveFormSlot, self).__init__(parent)

        self.width = width
        self.height = height

        self.waveFilePath = ""
        self.waveFileName = ""
        self.wavefile = None
        
        self.num = num

        self.dataSet = numpy.array([])

        self.setAcceptDrops(True)

        # WaveForm Widget
        ##################################################
        self.waveformWidgetContainer = QtGui.QGroupBox("Sample " + str(self.num+1) + ": ", self)
        self.waveformWidgetLayout = QtGui.QHBoxLayout(self)

        # Waveform Area instance
    	self.waveformArea = WaveformPaintArea(self, width, height)

        self.waveformWidgetLayout.addWidget(self.waveformArea)
        self.waveformWidgetContainer.setLayout(self.waveformWidgetLayout)

        # Option Form Widget
        ##################################################
        self.formWidgetContainer = QtGui.QGroupBox("Functions", self)
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

        # Signals/Slots
        ##################################################
        self.optionForm.addDelay.connect(self.addDelay)
        self.optionForm.addEcho.connect(self.addVolume)
        self.optionForm.addDecimator.connect(self.addDecimator)
        self.optionForm.addBitCrusher.connect(self.addBitCrusher)
        self.optionForm.addPitchShift.connect(self.addPitchShift)
        self.optionForm.addVolume.connect(self.addVolume)

        self.optionForm.playButton.clicked.connect(self.playSample)

    def addVolume(self):

        ok = False
        while not ok:
            percentage, ok = QtGui.QInputDialog.getDouble(self,
                    "Scale Volume (Percent%)", "Scale:", 50.0)

        self.waveformArea.updateDataSet(Filters.ScaleVolume(self.wavefile.getData(),  percentage))

    def addDelay(self):
        ok = False
        while not ok:
            delay, ok = QtGui.QInputDialog.getDouble(self,
                    "Set Delay (Seconds)", "Delay:", 1.0)

        ok = False

        while not ok:
            alpha, ok = QtGui.QInputDialog.getDouble(self,
                    "Set Alpha", "Alpha:", 0.5)

        self.waveformArea.updateDataSet(Filters.Delay(self.wavefile.getData(), delay, alpha ))

    def addEcho(self):
        ok = False
        while not ok:
            delay, ok = QtGui.QInputDialog.getDouble(self,
                    "Set Echo (Seconds)", "Delay:", 1.0)

        ok = False

        while not ok:
            alpha, ok = QtGui.QInputDialog.getDouble(self,
                    "Set Alpha", "Alpha:", 0.5)

        self.waveformArea.updateDataSet(Filters.Echo(self.wavefile.getData(), delay, alpha ))

    def addDecimator(self):
        ok = False
        while not ok:
            percentage, ok = QtGui.QInputDialog.getDouble(self,
                    "Set Decimator Percentage", "Decimator:", 50.0)

        self.waveformArea.updateDataSet(Filters.Decimator(self.wavefile.getData(), percentage/100.0 ))
        self.waveformArea.update()

    def addBitCrusher(self):
        ok = False
        while not ok:
            bits, ok = QtGui.QInputDialog.getInteger(self,
                    "Set Num of Bits", "Bits:", 8)

        self.waveformArea.updateDataSet(Filters.BitCrusher(self.wavefile.getData(), bits))

    def addPitchShift(self):
        ok = False
        while not ok:
            frequency, ok = QtGui.QInputDialog.getInteger(self,
                    "Set the New Frequency", "Frequency:", 44100, step=1000)

        self.waveformArea.updateDataSet(Filters.PitchShift(self.wavefile.getData(), frequency))

    def sizeHint(self):
        return QtCore.QSize(self.width, self.height)

    def dragEnterEvent(self, e):
        e.acceptProposedAction()

    def playSample(self):
        self.wavefile.play()

    def dropEvent(self, e):
        path = e.mimeData().urls()[0].toLocalFile().toLocal8Bit().data()
        if os.path.isfile(path):
            QtCore.qDebug(path)

            e.acceptProposedAction()

            self.waveFilePath = path
            self.waveFileName = os.path.basename(path)

            self.waveformWidgetContainer.setTitle("Sample " + str(self.num+1) + ": " + self.waveFileName)
            QtCore.qDebug(self.waveFileName)

            SysCtl.mkdir("tmp")

            copypath = "tmp/raw" + str(self.num) + ".wav"

            SysCtl.copyFile(path, copypath)
            
            self.wavefile = WavFileReader(copypath)
      
            self.waveformArea.updateDataSet(self.wavefile.getData())

            #TODO import wave dialog with progress bar
            #TODO emit update data set
        
class WaveformPaintArea(QtGui.QWidget):

  def __init__(self, parent, width, height):
    super(WaveformPaintArea, self).__init__(parent)

    self.width = width
    self.height = height

    self.dataSet = []
    self.wavfile = None
    self.step = 1
    self.division = 1
    self.undersample = 32

  def sizeHint(self):
      return QtCore.QSize(self.width, self.height)

  #Slot
  def updateDataSet(self, data):
      self.dataSet = data
      Filters.FloatToInt(self.dataSet)
      self.division = int(Filters.Peak2Peak(self.dataSet)/self.height)
      self.step = int(len(self.dataSet) / self.undersample)
      self.update()

  def paintEvent(self, event):

    painter = QtGui.QPainter()

    painter.begin(self)

    self.drawWaveForm(painter)

    painter.end()

  def drawWaveForm(self, painter):

    painter.setRenderHint(QtGui.QPainter.Antialiasing);

    pen = QtGui.QPen(QtGui.QColor(0,200,200))
    pen.setWidth(1) #pixel
    painter.setPen(pen)
  
    step = len(self.dataSet) / 16

    for i in range(step):
      y = self.height/2 + self.dataSet[i*16] / self.division
      x = i * self.width / step
      painter.drawPoint(x, y)

class WaveOptionForm(QtGui.QWidget):
    playPressed = QtCore.pyqtSignal()

    addDelay = QtCore.pyqtSignal()
    addEcho = QtCore.pyqtSignal()
    addDecimator = QtCore.pyqtSignal()
    addPitchShift = QtCore.pyqtSignal()
    addBitCrusher = QtCore.pyqtSignal()
    addVolume = QtCore.pyqtSignal()

    def __init__(self, parent):
        super(WaveOptionForm, self).__init__(parent)

        layout = QtGui.QGridLayout(self)

        self.slider = QtGui.QSlider()
        self.playButton = QtGui.QPushButton("Play")
        self.effectsButton = QtGui.QPushButton("Add Effect")

        self.syncButton = QtGui.QPushButton("Sync")
        self.sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        self.sizePolicy.setHeightForWidth(self.syncButton.sizePolicy().hasHeightForWidth())
        self.syncButton.setSizePolicy(self.sizePolicy)

        menu = QtGui.QMenu(self)

        self.volumeAction = QtGui.QAction(self)
        self.volumeAction.setText("&Volume")
        self.volumeAction.triggered.connect(self.addVolume)

        self.echoAction = QtGui.QAction(self)
        self.echoAction.setText("&Echo")
        self.echoAction.triggered.connect(self.addEcho)

        self.delayAction = QtGui.QAction(self)
        self.delayAction.setText("&Delay")
        self.delayAction.triggered.connect(self.addDelay)

        self.decimatorAction = QtGui.QAction(self)
        self.decimatorAction.setText("&Decimator")
        self.decimatorAction.triggered.connect(self.addDecimator)

        self.bitCrusherAction = QtGui.QAction(self)
        self.bitCrusherAction.setText("&Bit Crush")
        self.bitCrusherAction.triggered.connect(self.addBitCrusher)

        self.pitchShiftAction = QtGui.QAction(self)
        self.pitchShiftAction.setText("&Pitch Shift")
        self.pitchShiftAction.triggered.connect(self.addPitchShift)

        menu.addAction(self.echoAction)
        menu.addAction(self.delayAction)
        menu.addAction(self.decimatorAction)
        menu.addAction(self.bitCrusherAction)
        menu.addAction(self.pitchShiftAction)

        self.effectsButton.setMenu(menu)

        layout.addWidget(self.slider, 0, 1, 2, 1)
        layout.addWidget(self.playButton, 0, 2)
        layout.addWidget(self.effectsButton, 1, 2)
        layout.addWidget(self.syncButton, 0, 3, 2, 2)

        layout.setColumnStretch(1, 10)
        layout.setColumnStretch(2, 20)

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
