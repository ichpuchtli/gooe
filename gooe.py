#TODO Simple USART console
#TODO Simple mpc state model
#TODO message protocol
#TODO mpc model -> json

import sys
import random

#from PyQt4.QtCore import *
#from PyQt4.QtGui import *
from PyQt4 import QtGui, QtCore

class MediaCentre(QtGui.QWidget):

    # This function simply calls the parent QWidget.__init__() function,
    # then calls our setup function
    def __init__(self):
        super(MediaCentre, self).__init__()
        self.setup()

    # Setup all the windows/buttons etc..
    def setup(self):

        # Setup our window here these function are defined inthe QWidget Class
        self.setGeometry(300, 300, 500, 500)
        self.setWindowTitle('Media Centre')
        self.keyboard=QtGui.QGroupBox("Keyboard",self)
        self.keyboard.setGeometry(QtCore.QRect(100,30, 350, 200))
        self.keyboard.setObjectName("Keyboard")
        self.buttonGroup = QtGui.QButtonGroup()


        # Create a button
        #self.btn = QtGui.QPushButton('Button!', self)
        #self.btn.resize(self.btn.sizeHint())
        #self.btn.move(30,30)
        #self.btn.show()
        #self.buttonGroup.addButton(self.btn,1)

        #self.btnlist = range(16)
        #for i in range(16):
        #        self.btnlist[i] = QtGui.QPushButton("Button")
        #        self.btnlist[i].show()
        #for i in range(16):
        #        self.buttonGroup.addButton(self.btnlist[i],i)


        #Create buttons first row
        self.btn = QtGui.QPushButton("Button1", self.keyboard)
        self.btn.resize(self.btn.sizeHint())
        self.btn.move(10,20)
        self.btn.show()
        self.buttonGroup.addButton(self.btn,1)

        self.btn2 = QtGui.QPushButton("Button2", self.keyboard)
        self.btn2.resize(self.btn.sizeHint())
        self.btn2.move(90,20)
        self.btn2.show()
        self.buttonGroup.addButton(self.btn2,2)

        self.btn3= QtGui.QPushButton("Button2", self.keyboard)
        self.btn3.resize(self.btn.sizeHint())
        self.btn3.move(170,20)
        self.btn3.show()
        self.buttonGroup.addButton(self.btn,3)

        self.btn4 = QtGui.QPushButton("Button4", self.keyboard)
        self.btn4.resize(self.btn.sizeHint())
        self.btn4.move(250,20)
        self.btn4.show()
        self.buttonGroup.addButton(self.btn,4)

        #Creat buttons second row
        self.btn5 = QtGui.QPushButton("Button5", self.keyboard)
        self.btn5.resize(self.btn.sizeHint())
        self.btn5.move(10,50)
        self.btn5.show()
        self.buttonGroup.addButton(self.btn5,5)

        self.btn6 = QtGui.QPushButton("Button6", self.keyboard)
        self.btn6.resize(self.btn.sizeHint())
        self.btn6.move(90,50)
        self.btn6.show()
        self.buttonGroup.addButton(self.btn6,6)

        self.btn7= QtGui.QPushButton("Button7", self.keyboard)
        self.btn7.resize(self.btn.sizeHint())
        self.btn7.move(170,50)
        self.btn7.show()
        self.buttonGroup.addButton(self.btn7,7)

        self.btn8 = QtGui.QPushButton("Button8", self.keyboard)
        self.btn8.resize(self.btn.sizeHint())
        self.btn8.move(250,50)
        self.btn8.show()
        self.buttonGroup.addButton(self.btn8,8)

        #Creat buttons third row
        self.btn9 = QtGui.QPushButton("Button9", self.keyboard)
        self.btn9.resize(self.btn.sizeHint())
        self.btn9.move(10,80)
        self.btn9.show()
        self.buttonGroup.addButton(self.btn9,9)

        self.btn10 = QtGui.QPushButton("Button10", self.keyboard)
        self.btn10.resize(self.btn.sizeHint())
        self.btn10.move(90,80)
        self.btn10.show()
        self.buttonGroup.addButton(self.btn10,10)

        self.btn11= QtGui.QPushButton("Button11", self.keyboard)
        self.btn11.resize(self.btn.sizeHint())
        self.btn11.move(170,80)
        self.btn11.show()
        self.buttonGroup.addButton(self.btn11,11)

        self.btn12 = QtGui.QPushButton("Button12", self.keyboard)
        self.btn12.resize(self.btn.sizeHint())
        self.btn12.move(250,80)
        self.btn12.show()
        self.buttonGroup.addButton(self.btn12,12)

        #Creat buttons fourth row
        self.btn13 = QtGui.QPushButton("Button13", self.keyboard)
        self.btn13.resize(self.btn.sizeHint())
        self.btn13.move(10,110)
        self.btn13.show()
        self.buttonGroup.addButton(self.btn9,9)

        self.btn14 = QtGui.QPushButton("Button14", self.keyboard)
        self.btn14.resize(self.btn.sizeHint())
        self.btn14.move(90,110)
        self.btn14.show()
        self.buttonGroup.addButton(self.btn14,14)

        self.btn15= QtGui.QPushButton("Button15", self.keyboard)
        self.btn15.resize(self.btn.sizeHint())
        self.btn15.move(170,110)
        self.btn15.show()
        self.buttonGroup.addButton(self.btn15,15)

        self.btn16 = QtGui.QPushButton("Button16", self.keyboard)
        self.btn16.resize(self.btn.sizeHint())
        self.btn16.move(250,110)
        self.btn16.show()
        self.buttonGroup.addButton(self.btn16,16)











        # "Connect" a button press event with a function in this case buttonPress()
        self.connect(self.btn, QtCore.SIGNAL("clicked()"), self.buttonPress)

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
