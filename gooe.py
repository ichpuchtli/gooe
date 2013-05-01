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
        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('Media Centre')

        # Create a button
        self.btn = QtGui.QPushButton('Button!', self)
        self.btn.resize(self.btn.sizeHint())
        self.btn.move(30,30)
        self.btn.show()

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
