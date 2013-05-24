# gooe.py - TP2 Gui (MediaCentre)

import sys
from cfg import USBConfig
from usbms import USBController
from wavfile import WavFileReader, WavFileWriter
import widgets

from PyQt4 import QtGui, QtCore
import winsound

class MediaCentre(QtGui.QMainWindow):

    # This function simply calls the parent QWidget.__init__() function,
    # then calls our setup function
    def __init__(self,parent=None):
        QtGui.QWidget.__init__(self,parent)

	self.cfg = USBConfig()
	self.usb = USBController()

        self.setup()


    def menuOpenDirEvent(self):
	    self.userdir = QtGui.QFileDialog.getExistingDirectory(self, "Choose Dir", ".")
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
	#self.connect(self.listWidget, QtCore.SIGNAL(itemDoubleClicked)
        self.boxLayout = QtGui.QVBoxLayout(self.listWidget)

    def setupKeypad(self, parent):

        #Setup Keypad
        self.keypad = QtGui.QGroupBox("Keypad", parent)
        self.keypad.setGeometry(QtCore.QRect(480,40, 471, 461))

        #change keypad position
        self.keypad.setAlignment(QtCore.Qt.AlignCenter)

        self.gridLayoutWidget = QtGui.QWidget(self.keypad)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(30, 40, 411, 381))
        #change button size

        self.gridLayout = QtGui.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setMargin(0)

        self.buttonList = [None]*(16)

        for i in range(16):
            self.buttonList[i] = QtGui.QPushButton("Button%d" % (i+1), self.gridLayoutWidget)
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
        self.actionOpenDir.setText("Open")
	self.actionOpenDir.triggered.connect(self.menuOpenDirEvent)

        self.actionSave = QtGui.QAction(self)
        self.actionSave.setText("Save")

        self.actionClose = QtGui.QAction(self)
        self.actionClose.setText("Close")

        self.menuFile.addAction(self.actionOpenDir)
        self.menuFile.addAction(self.actionSave)
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
    def setup(self):

        # Setup our window here these function are defined inthe QWidget Class
        self.setWindowTitle('Media Centre')
        self.resize(1040,640);

        self.centralWidget = QtGui.QWidget(self)
        self.setCentralWidget(self.centralWidget)

        self.setupMenuBar()

        self.tab1, self.tab2 = self.setupTabs(self.centralWidget)

	self.waveform = widgets.WaveFormWidget(self.tab2, 0,0, 500, 500)

        self.setupKeypad(self.tab1)

        self.setupList(self.tab1)


# Create the main QApplication
app = QtGui.QApplication(sys.argv)

# Create our widget & Show it
window = MediaCentre()
window.show()


# Execute this app
sys.exit(app.exec_())
