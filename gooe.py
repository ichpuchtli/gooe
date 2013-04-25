#TODO Simple USART console
#TODO Simple mpc state model
#TODO message protocol
#TODO mpc model -> json

import sys

from PyQt4.QtCore import *
from PyQt4.QtGui import *

# Create the application object
app = QApplication(sys.argv)

# Create a simple dialog box
msgBox = QMessageBox()
msgBox.setText("Hello World!")
msgBox.exec_()

