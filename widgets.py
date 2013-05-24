#!/usr/bin/python2

from PyQt4 import QtGui, QtCore

import random
import math

class WaveFormWidget(QtGui.QWidget):

  def __init__(self, parent, pos_x, pos_y, width, height):
    super(WaveFormWidget, self).__init__(parent)

    self.x = pos_x
    self.y = pos_y
    self.width = width
    self.height = height

    self.setGeometry(self.x, self.y, self.width, self.height)

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
  
    for i in range(self.width):
      x = i
      y = (1 + math.sin(x*(8*math.pi/self.width))) * self.height/4 + self.height/4
      painter.drawPoint(x, y)
