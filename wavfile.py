#!/usr/bin/python2

import wave
import sys

def isWindows():
  return sys.platform == "win32"

if isWindows():
  import winsound

class WavFileReader:

  def __init__(self, filename):
    self.fp = wave.open(filename, "r")
    self.frames = self.getFramesFromFile()

  def close(self):
    self.fp.close()

  def getFrameFromFile(self, n):
    #rewind
    #setpos
    #readframes(1)
    return []

  def play(self):
    if isWindows():
      winsound.PlaySound(self.frames, winsound.SND_MEMORY)

  def playRegion(self, lower, upper):
    if isWindows():
      winsound.PlaySound(self.frames, winsound.SND_MEMORY)

  def getFrame(self, n):
    return self.frames[n]

  def pos(self):
    return self.fp.tell()

  def seek(self, n):
    self.fp.setpos(n)

  def rewind(self):
    self.fp.rewind()

  def getFrames(self):
    return self.frames

  def getFramesFromFile(self):
    #rewind
    return self.fp.readframes(self.getNumFrames())

  def getNumFrames(self):
    return self.fp.getnframes()

  def getNumChannels(self):
    return self.fp.getnchannels()

  def getSampleFrequency(self):
    return self.fp.getframerate()

  def getBitDepth(self):
    return self.fp.getsampwidth()

class WavFileWriter:

  def __init__(self, filename):
    self.fp = wave.open(filename, "w")
    self.setNumChannels(1)
    self.setBitDepth(2) # Bytes - 16bits
    self.setSampleFrequency(44100)
    self.data = ""

  def close(self):
    self.fp.close()

  def setNumChannels(self, num):
    self.fp.setnchannels(num)
  
  def setBitDepth(self, depth):
    self.fp.setsampwidth(depth)

  def setSampleFrequency(self, freq):
    self.fp.setframerate(freq)

  def writeFrame(self, n, frame):
    self.data[n] = frame[0]
    self.data[n+1] = frame[1]

  def writeFrames(self, frames):
    self.data += frames

  def sync(self):
    self.fp.writeframes(self.data)
