#!/usr/bin/python2

import sys
import os
import shutil

import string
from ctypes import windll

class USBController:

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
  
  def listDriveLetters(self):
    if self.isWindows():
      drives = []
      bitmask = windll.kernel32.GetLogicalDrives()
      for letter in string.uppercase:
        if bitmask & 1:
          drives.append(letter)
        bitmask >>= 1

      return drives

    else:
      return os.listdir("/run/media/sam")

  def copyFile(self, srcPath, destPath):
    copyfile(srcPath, destPath)

  def pwd(self):
    return os.getcwd()

  def ls(self, path="."):
    return os.listdir(path)

  def cd(self,path):
    os.chdir(path)

  def openDirLetter(self,letter):
    if self.isWindows():
      os.chdir(letter + ":\\")
      return os.listdir(".")
    else:
      os.chdir("/run/media/sam/" + letter)
      return os.listdir(".")
  
