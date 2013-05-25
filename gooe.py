# gooe.py - TP2 Gui (MediaCentre)

import os
import sys
from cfg import USBConfig
from usbms import USBController
from wavfile import WavFileReader, WavFileWriter
import widgets

from PyQt4 import QtGui, QtCore
import winsound

class MediaCentre(QtGui.QMainWindow):

    def __init__(self,parent=None):
        QtGui.QWidget.__init__(self,parent)

	self.cfg = USBConfig()
	self.usb = USBController()

        self.setupUi()

    def keyPressEvent(self, evt):
        key = evt.key()
        modifier = evt.modifiers()

        if key == QtCore.Qt.Key_Escape:
            QtGui.QApplication.exit()

        IS_PASTE = (modifier == QtCore.Qt.ControlModifier and key == QtCore.Qt.Key_V)
        if IS_PASTE:
            clipboard = QtGui.QApplication.clipboard()
            mime_data = clipboard.mimeData()

            for url in mime_data.urls():
                path = url.toLocalFile().toLocal8Bit().data()
                if os.path.isfile(path):
                    QtCore.qDebug(path)

            QtCore.qDebug( "urls:" + str([i.toLocalFile() for i in mime_data.urls()]))
            QtCore.qDebug( "text:" + str(mime_data.text()) )
            QtCore.qDebug( "html:" + str(mime_data.html()) )

    def menuOpenDirEvent(self):
	    self.userdir = QtGui.QFileDialog.getExistingDirectory(self, "Choose Sample Directory", ".")
	    QtCore.qDebug(self.userdir)

	    self.listWidget.clear()

	    for filename in self.usb.ls(self.userdir):
		    if ".wav" in filename:
			    self.listWidget.addItem(QtGui.QListWidgetItem(filename))

    def listItemDoubleClicked(self, widget):
	    widget = self.sender()
	    QtCore.qDebug(str(widget))
	    filePath = self.userdir + "\\" + widget.currentItem().text()
	    QtCore.qDebug(str(filePath))
	    winsound.PlaySound(filePath, winsound.SND_FILENAME | winsound.SND_ASYNC)

    def setupList(self, parent):

        #Setup listwidget
        self.listWidget = QtGui.QListWidget(parent)
	self.listWidget.itemDoubleClicked.connect(self.listItemDoubleClicked)
        self.listWidget.setDragEnabled(True)

        for filename in self.usb.ls("sounds"):
                if ".wav" in filename:
                        self.listWidget.addItem(QtGui.QListWidgetItem(filename))
        self.boxLayout = QtGui.QVBoxLayout(self.listWidget)

    def setupKeypad(self, parent):

        #Setup Keypad
        box_x = 280
        box_y = 280

        self.keypad = QtGui.QGroupBox("Keypad", parent)
        self.keypad.setGeometry(QtCore.QRect(420, 10, box_x, box_y))

        #change keypad position
        self.keypad.setAlignment(QtCore.Qt.AlignCenter)

        self.gridLayoutWidget = QtGui.QWidget(self.keypad)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(10, 20, box_x - 20, box_y - 30))
        #change button size

        self.gridLayout = QtGui.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setMargin(0)

        self.buttonList = [None]*(16)

        for i in range(16):
            self.buttonList[i] = widgets.MPCPadButton("Button%d" % (i+1), self.gridLayoutWidget, i)
            self.sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
            self.sizePolicy.setHeightForWidth(self.buttonList[i].sizePolicy().hasHeightForWidth())
            self.buttonList[i].setSizePolicy(self.sizePolicy)
            self.gridLayout.addWidget(self.buttonList[i], int(i/4), int(i%4), 1, 1)

        # Connect a button press event with a function buttonPress
        for i in range (16):
            self.buttonList[i].clicked.connect(self.buttonPress)

    # This function is "connected" to the clicked event signal from ButtonList
    def buttonPress(self):
	button = self.sender()
        # Print message of "Button# pressed"
        #self.connect(self.tetrisboard, QtCore.SIGNAL("messageToStatusbar(QString)"),
        self.statusBar().showMessage("Button Pressed: " + button.text())
	QtCore.qDebug("Button Pressed: " + button.text())

    def usbSelectEvent(self, boolean):
	action = self.sender()
	QtCore.qDebug("USB Device: " + action.text() + " Selected")

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
	self.actionOpenDir.triggered.connect(self.menuOpenDirEvent)

        self.actionLoadSesh = QtGui.QAction(self)
        self.actionLoadSesh.setText("Load Session")

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
        self.menuEdit.setTitle("USB Select ")

	self.letterActions = [None]*26
	i = 0
	for letter in self.usb.listDriveLetters():
		self.letterActions[i] = QtGui.QAction(self)
		self.letterActions[i].setText("(" + letter + ") Device")
		self.menuEdit.addAction(self.letterActions[i])
		self.letterActions[i].triggered.connect(self.usbSelectEvent)

        self.menuBar.addAction(self.menuFile.menuAction())
        self.menuBar.addAction(self.menuEdit.menuAction())

        self.setMenuBar(self.menuBar)

    def setupTabs(self, parent):

        # Setup tabs
        tabWidget = QtGui.QTabWidget(parent)
        tabWidget.setGeometry(QtCore.QRect(0, 0, 1040, 640))
        tab = QtGui.QWidget()
        tabWidget.addTab(tab,"Tab1")
        tab_2 = QtGui.QWidget()
        tabWidget.addTab(tab_2,"Tab2")

        return tab, tab_2

    # Setup all the windows/buttons etc..
    def setupUi(self):

        # Setup our window here these function are defined inthe QWidget Class
        self.setWindowTitle('Media Centre')
        self.resize(960,480);
        self.statusBar().showMessage('Ready')

        self.centralWidget = QtGui.QWidget(self)
        self.setCentralWidget(self.centralWidget)

        self.setupMenuBar()

        self.tab1, self.tab2 = self.setupTabs(self.centralWidget)

        #self.scrollarea = QtGui.QScrollArea(self.tab2)

        self.layout = QtGui.QHBoxLayout()

	self.waveFormArea = widgets.WavePaintArea(self.tab1, 0, 0, 200, 40)
        self.optionForm = widgets.WaveOptionForm(self.tab1)

        self.layout.addWidget(self.waveFormArea)
        self.layout.addWidget(self.optionForm)

        self.tab1.setLayout(self.layout)

	#self.waveform = widgets.WaveFormSlot(self.tab1)

        #self.scrollarea.setWidget(self.waveform)

        #self.scrollarea.setMinimumSize(640,120)

        self.setupKeypad(self.tab2)

        #self.setupList(self.tab1)


# Create the main QApplication
app = QtGui.QApplication(sys.argv)

# Create our widget & Show it
window = MediaCentre()
window.show()
window.raise_()


# Execute this app
sys.exit(app.exec_())
