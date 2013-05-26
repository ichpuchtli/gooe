#!/usr/bin/python2

import os

class USBInterface:

  def __init__(self, path):

    self.drive = os.path.abspath("/")

    #print os.getcwd()
    #print os.uname()
    #print os.path.abspath(".")

  def writeData(self, filePath, data):

    filp = open(filePath, 'w')
    filp.write(data)

    filp.flush()
    os.fsync(filp.fileno())

    filp.close()

  def writeConfig(self, filePath, config):
    self.writeData(filePath, config.toText())

  def readConfig(self, filePath, config):
    filp = open(filePath, 'r')
    config.fromText(filp.read())
    filp.close()
