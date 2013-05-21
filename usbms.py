#!/usr/bin/python2

import sys
import os

class USBMSController():

  #TODO Determine operating system
  #TODO Create Buffers for each sample
  def __init__(self):

    self.os = sys.platform
    self.drive = os.path.abspath("/")

    print os.getcwd()
    print os.uname()
    print os.path.abspath(".")

  def isWindows(self):
    return (self.os == "win32")

  def isLinux(self):
    return (self.os == "linux2")

  def writeData(filePath, data):

    filp = open(filePath, 'w')
    filp.write(data)
    filp.close()
    
    print "writeWaveData", filp

  def writeConfig(filePath, config):
    self.writeData(filePath, config.toText())
  
  def listDriveLetters(self):
    if self.isWindows():
      drives = []
      bitmask = windll.kernel32.GetLogicalDrives()
      for letter in string.uppercase:
        if bitmask & 1:
          drives.append(letter)
        bitmask >>= 1

      return drives

    else
      return os.listdirs("/run/media")

  def openDirLetter(self,letter):
    os.chdir(letter + ":\\")
    return os.listdir("/")
  
