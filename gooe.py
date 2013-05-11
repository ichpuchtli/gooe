#TODO Simple USART console
#TODO Simple mpc state model
#TODO message protocol
#TODO mpc model -> json

import sys
import random

#from PyQt4.QtCore import *
#from PyQt4.QtGui import *
from PyQt4 import QtGui, QtCore

class MediaCentre(QtGui.QMainWindow):

    # This function simply calls the parent QWidget.__init__() function,
    # then calls our setup function
    def __init__(self,parent=None):
	QtGui.QWidget.__init__(self,parent)
        self.setup()

    # Setup all the windows/buttons etc..
    def setup(self):

        # Setup our window here these function are defined inthe QWidget Class
	self.setWindowTitle('Media Centre')
	self.resize(1040,640);
	self.centralWidget = QtGui.QWidget(self)
	self.setCentralWidget(self.centralWidget)

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
	self.menuEdit.setTitle("Edit")

	self.actionSettings = QtGui.QAction(self)
	self.actionSettings.setText("Settings")

	self.menuEdit.addAction(self.actionSettings)

	self.menuBar.addAction(self.menuFile.menuAction())
	self.menuBar.addAction(self.menuEdit.menuAction())

	self.setMenuBar(self.menuBar)

        # Setup tabs
        self.tabWidget = QtGui.QTabWidget(self.centralWidget)
	self.tabWidget.setGeometry(QtCore.QRect(0, 0, 1040, 640))
        self.tab = QtGui.QWidget()
        self.tabWidget.addTab(self.tab,"Tab1")
        self.tab_2 = QtGui.QWidget()
        self.tabWidget.addTab(self.tab_2,"Tab2")

        #Setup Keypad
        self.keypad = QtGui.QGroupBox("Keypad", self.tab)
	self.keypad.setGeometry(QtCore.QRect(40,40, 471, 461))
        self.keypad.setAlignment(QtCore.Qt.AlignCenter)
        self.gridLayoutWidget = QtGui.QWidget(self.keypad)
	self.gridLayoutWidget.setGeometry(QtCore.QRect(30, 40, 411, 381))
        self.gridLayout = QtGui.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setMargin(0)


        #Create buttons first row
        self.btn = QtGui.QPushButton("Button1", self.gridLayoutWidget)
        self.sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        self.sizePolicy.setHeightForWidth(self.btn.sizePolicy().hasHeightForWidth())
        self.btn.setSizePolicy(self.sizePolicy)
        self.gridLayout.addWidget(self.btn, 0, 0, 1, 1)

        self.btn2 = QtGui.QPushButton("Button2", self.keypad)
        self.sizePolicy.setHeightForWidth(self.btn2.sizePolicy().hasHeightForWidth())
        self.btn2.setSizePolicy(self.sizePolicy)
        self.gridLayout.addWidget(self.btn2, 0, 1, 1, 1)

        self.btn3= QtGui.QPushButton("Button2", self.keypad)
        self.sizePolicy.setHeightForWidth(self.btn3.sizePolicy().hasHeightForWidth())
        self.btn3.setSizePolicy(self.sizePolicy)
        self.gridLayout.addWidget(self.btn3, 0, 2, 1, 1)

        self.btn4 = QtGui.QPushButton("Button4", self.keypad)
        self.sizePolicy.setHeightForWidth(self.btn4.sizePolicy().hasHeightForWidth())
        self.btn4.setSizePolicy(self.sizePolicy)
        self.gridLayout.addWidget(self.btn4, 0, 3, 1, 1)


        #Creat buttons second row
        self.btn5 = QtGui.QPushButton("Button5", self.keypad)
        self.sizePolicy.setHeightForWidth(self.btn5.sizePolicy().hasHeightForWidth())
        self.btn5.setSizePolicy(self.sizePolicy)
        self.gridLayout.addWidget(self.btn5, 1, 0, 1, 1)


        self.btn6 = QtGui.QPushButton("Button6", self.keypad)
        self.sizePolicy.setHeightForWidth(self.btn6.sizePolicy().hasHeightForWidth())
        self.btn6.setSizePolicy(self.sizePolicy)
        self.gridLayout.addWidget(self.btn6, 1, 1, 1, 1)


        self.btn7= QtGui.QPushButton("Button7", self.keypad)
        self.sizePolicy.setHeightForWidth(self.btn7.sizePolicy().hasHeightForWidth())
        self.btn7.setSizePolicy(self.sizePolicy)
        self.gridLayout.addWidget(self.btn7, 1, 2, 1, 1)


        self.btn8 = QtGui.QPushButton("Button8", self.keypad)
        self.sizePolicy.setHeightForWidth(self.btn8.sizePolicy().hasHeightForWidth())
        self.btn8.setSizePolicy(self.sizePolicy)
        self.gridLayout.addWidget(self.btn8, 1, 3, 1, 1)

        #Creat buttons third row
        self.btn9 = QtGui.QPushButton("Button9", self.keypad)
        self.sizePolicy.setHeightForWidth(self.btn9.sizePolicy().hasHeightForWidth())
        self.btn9.setSizePolicy(self.sizePolicy)
        self.gridLayout.addWidget(self.btn9, 2, 0, 1, 1)

        self.btn10 = QtGui.QPushButton("Button10", self.keypad)
        self.sizePolicy.setHeightForWidth(self.btn10.sizePolicy().hasHeightForWidth())
        self.btn10.setSizePolicy(self.sizePolicy)
        self.gridLayout.addWidget(self.btn10, 2, 1, 1, 1)

        self.btn11= QtGui.QPushButton("Button11", self.keypad)
        self.sizePolicy.setHeightForWidth(self.btn11.sizePolicy().hasHeightForWidth())
        self.btn11.setSizePolicy(self.sizePolicy)
        self.gridLayout.addWidget(self.btn11, 2, 2, 1, 1)

        self.btn12 = QtGui.QPushButton("Button12", self.keypad)
        self.sizePolicy.setHeightForWidth(self.btn12.sizePolicy().hasHeightForWidth())
        self.btn12.setSizePolicy(self.sizePolicy)
        self.gridLayout.addWidget(self.btn12, 2, 3, 1, 1)

        #Creat buttons fourth row
        self.btn13 = QtGui.QPushButton("Button13", self.keypad)
        self.sizePolicy.setHeightForWidth(self.btn13.sizePolicy().hasHeightForWidth())
        self.btn13.setSizePolicy(self.sizePolicy)
        self.gridLayout.addWidget(self.btn13, 3, 0, 1, 1)

        self.btn14 = QtGui.QPushButton("Button14", self.keypad)
        self.sizePolicy.setHeightForWidth(self.btn14.sizePolicy().hasHeightForWidth())
        self.btn14.setSizePolicy(self.sizePolicy)
        self.gridLayout.addWidget(self.btn14, 3, 1, 1, 1)

        self.btn15= QtGui.QPushButton("Button15", self.keypad)
        self.sizePolicy.setHeightForWidth(self.btn15.sizePolicy().hasHeightForWidth())
        self.btn15.setSizePolicy(self.sizePolicy)
        self.gridLayout.addWidget(self.btn15, 3, 2, 1, 1)

        self.btn16 = QtGui.QPushButton("Button16", self.keypad)
        self.sizePolicy.setHeightForWidth(self.btn16.sizePolicy().hasHeightForWidth())
        self.btn16.setSizePolicy(self.sizePolicy)
        self.gridLayout.addWidget(self.btn16, 3, 3, 1, 1)

       # print self.buttonGroup.buttons()

       #self.connect(self.buttonGroup.button(1), QtCore.SIGNAL("clicked()"), self.buttonPress)


        # "Connect" a button press event with a function in this case buttonPress()
        #self.connect(self.btn, QtCore.SIGNAL("clicked()"), self.buttonPress)

    # This function is "connected" to the clicked event signal from self.btn
    def buttonPress(self):
        # Move the button to random positions using the random module
        self.btn.move(random.randint(0, 150), random.randint(0,100))

# Create the main QApplication
app = QtGui.QApplication(sys.argv)

# Create our widget & Show it
window = MediaCentre()
window.show()

# Execute this app
sys.exit(app.exec_())
