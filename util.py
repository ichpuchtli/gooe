
import shutil
import os
import sys

import string

try:
  from ctypes import windll
except ImportError:
  pass

class SysCtl:

  @staticmethod
  def isWindows():
    return (sys.platform == "win32")#

  @staticmethod
  def isLinux():
    return (sys.platform == "linux2")

  @staticmethod
  def listDriveLetters():
    if SysCtl.isWindows():
      drives = []
      bitmask = windll.kernel32.GetLogicalDrives()
      for letter in string.uppercase:
        if bitmask & 1:
          drives.append(letter)
        bitmask >>= 1

      return drives

    else:
      return os.listdir("/run/media/sam")

  @staticmethod
  def copyFile(srcPath, destPath):
    shutil.copyfile(srcPath, destPath)

  @staticmethod
  def mkdir(path):
    # Doesn't exists create it
    if(not os.access(path, os.F_OK)):
      os.mkdir(path)

  @staticmethod
  def pwd():
    return os.getcwd()

  @staticmethod
  def ls(path="."):
    return os.listdir(path)

  @staticmethod
  def cd(path):
    os.chdir(path)

  @staticmethod
  def openDirLetter(letter):
    if SysCtl.isWindows():
      os.chdir(letter + ":\\")
      return os.listdir(".")
    else:
      os.chdir("/run/media/sam/" + letter)
      return os.listdir(".")
  
