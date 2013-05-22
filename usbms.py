#!/usr/bin/python2

import sys
import os

class USBMSController():

  def __init__(self):

    self.os = sys.platform
    self.drive = os.path.abspath("/")

    #print os.getcwd()
    #print os.uname()
    #print os.path.abspath(".")

  def isWindows(self):
    return (self.os == "win32")#

  def isLinux(self):
    return (self.os == "linux2")

  def writeData(filePath, data):

    filp = open(filePath, 'w')
    filp.write(data)

    filp.flush()
    fsync(filp.fileno())

    filp.close()

  def writeConfig(filePath, config):
    self.writeData(filePath, config.toText())

  def readConfig(filePath, config):
    filp = open(filePath, 'r')
    config.fromText(filp.read())
    filp.close()
  
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

  def copyFile(srcPath, destPath):
    #TODO import shutil
    pass

  def openDirLetter(self,letter):
    os.chdir(letter + ":\\")
    return os.listdir("/")
  
