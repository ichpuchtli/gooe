# gooe.py - TP2 Gui (MediaCentre)

import os
import sys

from PySide import QtGui, QtCore

import random
import math
import numpy

# User Modules
from filters import Filters
from cfg import USBConfig
from usb import USBInterface
from wavfile import WavFileReader, WavFileWriter
from util import SysCtl

try:
    import winsound
except ImportError:
    pass

cfg = USBConfig()

class MediaCentre(QtGui.QMainWindow):

    def __init__(self,parent=None):
        QtGui.QMainWindow.__init__(self,parent)
        self.usb = USBInterface("")
        self.setupUi()

    def keyPressEvent(self, evt):
        key = evt.key()
        if key == QtCore.Qt.Key_Escape:
            QtGui.QApplication.exit()

    def setupMenuBar(self):

        # Setup Menubar
        self.menuBar = QtGui.QMenuBar(self)
        self.sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Minimum)
        self.sizePolicy.setHeightForWidth(self.menuBar.sizePolicy().hasHeightForWidth())
        self.menuBar.setSizePolicy(self.sizePolicy)

        # File Menu
        self.menuFile = QtGui.QMenu(self.menuBar)
        self.menuFile.setTitle("File")

        self.actionOpenDir = QtGui.QAction(self)
        self.actionOpenDir.setText("Import Folder")
        #self.actionOpenDir.triggered.connect(self.menuOpenDirEvent)

        self.actionLoadSesh = QtGui.QAction(self)
        self.actionLoadSesh.setText("Load Session")
        self.actionLoadSesh.triggered.connect(self.loadSession)

        self.actionSaveSesh = QtGui.QAction(self)
        self.actionSaveSesh.setText("Save Session")

        self.actionClose = QtGui.QAction(self)
        self.actionClose.setText("Close")
        self.actionClose.triggered.connect(QtGui.QApplication.exit)

        self.menuFile.addAction(self.actionOpenDir)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionLoadSesh)
        self.menuFile.addAction(self.actionSaveSesh)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionClose)

        # Edit Menu
        self.menuEdit = QtGui.QMenu(self.menuBar)
        self.menuEdit.setTitle("Settings")

        self.tempoAction = QtGui.QAction(self)
        self.tempoAction.setText("Set Board Tempo")

        self.menuEdit.addAction(self.tempoAction)

        self.tempoAction.triggered.connect(self.setTempo)

        self.menuBar.addAction(self.menuFile.menuAction())
        self.menuBar.addAction(self.menuEdit.menuAction())

        self.setMenuBar(self.menuBar)

    def setTempo(self):
        tempo, ok = QtGui.QInputDialog.getInteger(self,
                        "Set the Tempo", "Tempo:", 240)

        if ok:
            cfg.setTempo(tempo)

    def loadSession(self):
       drive, ok = QtGui.QInputDialog.getItem(self, "Select USB Device", "Drive Letter:",
         SysCtl.listDriveLetters(), 0, False)   

       for i in range(16):

         filename = "wav" + str(i+1) + ".wav" if i > 8 else "wav0" + str(i+1) + ".wav"

         if os.access(drive + ":\\" + filename, os.F_OK):
            SysCtl.copyFile(drive + ":\\" + filename,"tmp" + "\\" + filename)

         self.slotList[i].addSample("tmp" + "\\" + filename)

    # Setup all the windows/buttons etc..
    def setupUi(self):

        # Setup our window here these function are defined inthe QWidget Class
        self.setWindowTitle('Media Centre')
        self.resize(1500,900);

        # Menu bar
        self.setupMenuBar()

        self.slotTableWidget = QtGui.QWidget()

        self.slotTableLayout = QtGui.QVBoxLayout()
        self.slotTableLayout.setSpacing(0)
        #self.slotTableLayout.setMargin(0)

        self.slotList = [None]*(16)

        for i in range(16):
            self.slotList[i] = WaveFormSlot(i, 1300, 125)
            self.slotTableLayout.addWidget(self.slotList[i])

        self.slotTableWidget.setLayout(self.slotTableLayout)

        self.scrollarea = QtGui.QScrollArea(self)
        self.scrollarea.setWidget(self.slotTableWidget)

        self.scrollarea.setWidgetResizable(True)

        self.setCentralWidget(self.scrollarea)


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
        self.waveformWidgetContainer = QtGui.QGroupBox("Sample/Pad " + str(self.num+1) + ": ", self)
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
        self.optionForm.addEcho.connect(self.addEcho)
        self.optionForm.addDecimator.connect(self.addDecimator)
        self.optionForm.addBitCrusher.connect(self.addBitCrusher)
        self.optionForm.addPitchShift.connect(self.addPitchShift)
        self.optionForm.addVolume.connect(self.addVolume)

        self.optionForm.syncPressed.connect(self.sync)
        self.optionForm.resetPressed.connect(self.reset)
        self.optionForm.playPressed.connect(self.playSample)

        self.optionForm.leftSlider.connect(self.waveformArea.updateLeftSlice)
        self.optionForm.rightSlider.connect(self.waveformArea.updateRightSlice)
        self.optionForm.slicePressed.connect(self.slice)

    def sync(self):

        filename = "wav" + str(self.num+1) + ".wav" if self.num > 8 else "wav0" + str(self.num+1) + ".wav"

        writefile = WavFileWriter("tmp" + "\\" + filename)                
        writefile.writeData(self.waveformArea.getData())
        writefile.close()

        drive, ok = QtGui.QInputDialog.getItem(self, "Select USB Device", "Drive Letter:",
         SysCtl.listDriveLetters(), 0, False)  

        self.optionForm.syncButton.setChecked(True)

        SysCtl.copyFile("tmp" + "\\" + filename, drive + ":\\" + filename)

        #TODO Update cfg
        cfg.setWaveSize(self.num, len(self.waveformArea.getData()) )

        cfg.toFile(drive + ":\\" + "config.txt")

        self.optionForm.syncButton.setChecked(False)

    def slice(self):
       self.waveformArea.updateDataSet(
        Filters.Slice(
            self.waveformArea.getData(),self.waveformArea.sliceLeftValue*len(self.waveformArea.getData())
            , self.waveformArea.sliceRightValue*len(self.waveformArea.getData())))

    def reset(self):
        self.waveformArea.updateDataSet(self.wavefile.getData())

    def addVolume(self):

        percentage, ok = QtGui.QInputDialog.getDouble(self,
                "Scale Volume (Percent%)", "Scale:", 50.0)

        if ok:
            self.waveformArea.updateDataSet(Filters.ScaleVolume(self.waveformArea.getData(),  percentage/100))

    def addDelay(self):

        delay, ok = QtGui.QInputDialog.getDouble(self,
                "Set Delay (Seconds)", "Delay:", 1.0)

        if ok:

            alpha, ok = QtGui.QInputDialog.getDouble(self,
                        "Set Alpha", "Alpha:", 0.5)

            if ok:
                self.waveformArea.updateDataSet(Filters.Delay(self.waveformArea.getData(), delay, alpha ))

    def addEcho(self):

        delay, ok = QtGui.QInputDialog.getDouble(self,
                "Set Echo (Seconds)", "Delay:", 1.0)
        if ok:
            alpha, ok = QtGui.QInputDialog.getDouble(self,
                        "Set Alpha", "Alpha:", 0.5)

            if ok:
                self.waveformArea.updateDataSet(Filters.Echo(self.waveformArea.getData(), delay, alpha ))

    def addDecimator(self):
        percentage, ok = QtGui.QInputDialog.getDouble(self,
                "Set Decimator Percentage", "Decimator:", 50.0)


        if ok:
            self.waveformArea.updateDataSet(Filters.Decimator(self.waveformArea.getData(), percentage/100.0 ))

    def addBitCrusher(self):
        bits, ok = QtGui.QInputDialog.getInteger(self,
                "Set Num of Bits", "Bits:", 8)

        if ok:
            self.waveformArea.updateDataSet(Filters.BitCrusher(self.waveformArea.getData(), bits))

    def addPitchShift(self):
        frequency, ok = QtGui.QInputDialog.getInteger(self,
                "Set the New Frequency", "Frequency:", 44100, step=1000)

        if ok:
            self.waveformArea.updateDataSet(Filters.PitchShift(self.waveformArea.getData(), float(frequency)))

    def sizeHint(self):
        return QtCore.QSize(self.width, self.height)

    def dragEnterEvent(self, e):
        e.acceptProposedAction()

    def playSample(self):
        Filters.Play(self.waveformArea.getData())

    def addSample(self, path):

        if os.path.isfile(path):

            self.waveFilePath = path
            self.waveFileName = os.path.basename(path)

            self.wavefile = WavFileReader(path)

            if self.wavefile.getBitDepth() == 1:
              QtGui.QMessageBox.information(self, "Unsupported Format", "8Bit wav files are unsupported!")
              return

            self.waveformWidgetContainer.setTitle("Sample/Pad " + str(self.num+1) + ": " + self.waveFileName)
            self.waveformArea.updateDataSet(self.wavefile.getData())


    def dropEvent(self, e):
        path = e.mimeData().urls()[0].toLocalFile()
        e.acceptProposedAction()
        self.addSample(path)

class WaveformPaintArea(QtGui.QWidget):

  def __init__(self, parent, width, height):
    super(WaveformPaintArea, self).__init__(parent)

    self.width = width
    self.height = height

    self.dataSet = []
    self.wavfile = None
    self.step = 1
    self.division = 1
    self.undersample = 2

    self.sliceLeft = 0
    self.sliceRight = 0

    self.sliceLeftValue = 0
    self.sliceRightValue = 0

    self.pixBuffer = QtGui.QPixmap(width,height)
    self.pixBuffer.fill(QtGui.QColor(0,0,0))

  def getData(self):
    return Filters.IntToFloat(self.dataSet)

  def sizeHint(self):
    return QtCore.QSize(self.width, self.height)

  #Slot
  def updateDataSet(self, data):
    self.dataSet = Filters.FloatToInt(data)
    self.division = int(Filters.Peak2Peak(self.dataSet)/self.height)
    self.step = int(len(self.dataSet) / self.undersample)
    self.pixBuffer.fill(QtGui.QColor(0,0,0))
    self.updateBuffer()

  def paintEvent(self, event):

    painter = QtGui.QPainter()

    painter.begin(self)

    painter.drawPixmap(0,0,self.pixBuffer)
    self.drawSlices(painter)

    painter.end()

  def updateBuffer(self):

    painter = QtGui.QPainter(self.pixBuffer)

    self.drawWaveForm(painter)

    self.update()

  @QtCore.Slot(int)
  def updateRightSlice(self,value):
    self.sliceRightValue = value
    self.sliceRight = int(value*self.width/1000.0)
    self.updateBuffer()

  @QtCore.Slot(int)
  def updateLeftSlice(self,value):
    self.sliceLeftValue = value
    self.sliceLeft = int(value*self.width/1000.0)
    self.updateBuffer()

  def drawSlices(self, painter):

    painter.setRenderHint(QtGui.QPainter.Antialiasing);

    pen = QtGui.QPen(QtGui.QColor(255,0,0))
    pen.setWidth(1) #pixel
    painter.setPen(pen)

    painter.drawLine(self.sliceLeft,0,self.sliceLeft,self.height)
    painter.drawLine(self.sliceRight,0,self.sliceRight,self.height)


  def drawWaveForm(self, painter):

    painter.setRenderHint(QtGui.QPainter.Antialiasing);

    pen = QtGui.QPen(QtGui.QColor(0,200,200))
    pen.setWidth(1) #pixel
    painter.setPen(pen)

    step = len(self.dataSet) / self.undersample

    for i in range(step):
      y = self.height/2 + self.dataSet[i*self.undersample] / self.division
      x = i * self.width / step
      painter.drawPoint(x, y)

class WaveOptionForm(QtGui.QWidget):
    playPressed = QtCore.Signal()
    resetPressed = QtCore.Signal()
    syncPressed = QtCore.Signal()

    addDelay = QtCore.Signal()
    addEcho = QtCore.Signal()
    addDecimator = QtCore.Signal()
    addPitchShift = QtCore.Signal()
    addBitCrusher = QtCore.Signal()
    addVolume = QtCore.Signal()

    leftSlider = QtCore.Signal(int)
    rightSlider = QtCore.Signal(int)
    slicePressed = QtCore.Signal()

    def __init__(self, parent):
        super(WaveOptionForm, self).__init__(parent)

        layout = QtGui.QGridLayout(self)

        self.reset = QtGui.QPushButton("Reset")
        self.playButton = QtGui.QPushButton("Play")
        self.effectsButton = QtGui.QPushButton("Add Effect")
        self.syncButton = QtGui.QPushButton("Sync")
        self.syncButton.setCheckable(True)

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

        menu.addAction(self.volumeAction)
        menu.addAction(self.echoAction)
        menu.addAction(self.delayAction)
        menu.addAction(self.decimatorAction)
        menu.addAction(self.bitCrusherAction)
        menu.addAction(self.pitchShiftAction)

        self.effectsButton.setMenu(menu)

        self.reset.clicked.connect(self.resetPressed)
        self.playButton.clicked.connect(self.playPressed)
        self.syncButton.clicked.connect(self.syncPressed)

        layout.addWidget(self.playButton, 0, 1)
        layout.addWidget(self.reset, 0, 2)
        layout.addWidget(self.effectsButton, 1, 1)
        layout.addWidget(self.syncButton, 1, 2)

        self.leftSliderSlider = QtGui.QSlider(QtCore.Qt.Horizontal,self)
        self.leftSliderSlider.setMaximum(1000)

        self.rightSliderSlider = QtGui.QSlider(QtCore.Qt.Horizontal,self)
        self.rightSliderSlider.setMaximum(1000)
        self.rightSliderSlider.setValue(self.rightSliderSlider.maximum())

        layout.addWidget(self.leftSliderSlider, 2, 1)
        layout.addWidget(self.rightSliderSlider, 2, 2)

        self.leftSliderSlider.valueChanged.connect(self.leftSlider)
        self.rightSliderSlider.valueChanged.connect(self.rightSlider)

        self.loop_int = QtGui.QComboBox(self)
        self.loop_int.addItems(["1/2", "1/4", "1/8", "1/16", "1/32"])

        self.sliceButton = QtGui.QPushButton("Slice",self) 
        self.sliceButton.clicked.connect(self.slicePressed)

        layout.addWidget(self.sliceButton, 3, 1 )
        layout.addWidget(self.loop_int, 3, 2 )

        layout.setColumnStretch(1, 10)
        layout.setColumnStretch(2, 20)


# Create the main QApplication
app = QtGui.QApplication(sys.argv)

# Create our widget & Show it
window = MediaCentre()
window.show()

# Execute this app
sys.exit(app.exec_())
