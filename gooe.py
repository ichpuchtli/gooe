#TODO Simple USART console
#TODO Simple mpc state model
#TODO message protocol
#TODO mpc model -> json

import sys

#from PyQt4.QtCore import *
#from PyQt4.QtGui import *
from PyQt4 import QtGui, QtCore

app = QtGui.QApplication(sys.argv)

widget = QtGui.QWidget()

btn = QtGui.QPushButton('Button!',widget)

btn.resize(btn.sizeHint())
btn.move(50, 50)
btn.show()

widget.setGeometry(300, 300, 250, 150)
widget.setWindowTitle('Window!')
widget.show()
	
sys.exit(app.exec_())
