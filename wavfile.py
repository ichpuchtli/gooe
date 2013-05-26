#!/usr/bin/python2

import wave
import sys
import array
import struct
import filter

def isWindows():
  return sys.platform == "win32"

if isWindows():
  import winsound

class WavFileReader:

  def __init__(self, path):

    self.path = path
    self.fp = wave.open(path, "r")

    raw = []
    data = []
    # 32bit
    if self.getBitDepth() == 4:
        for i in range(self.getNumFrames()):
            waveFrame = self.fp.readframes(1)
            raw += waveFrame
            data += [(struct.unpack("<i", waveFrame)[0] >> 16)]

    # 16bit
    if self.getBitDepth() == 2:
        for i in range(self.getNumFrames()):
            waveFrame = self.fp.readframes(1)
            raw += waveFrame
            data += [struct.unpack("<h", waveFrame)[0]]

    self.mono = []
    # convert dual channel to single channel (mono)
    if self.getNumChannels() == 2:
        for i in range(len(data)):
            self.mono[i] = (data[i] + data[i+1])/2
    else:
        self.mono = data

    self.rawMono = ""
    for sample in data:
        self.rawMono += struct.pack("<h", sample)
        
    if self.getSampleFrequency() == 22050:
        Filters.OverSample(self.mono)

    self.close()

  def close(self):
    self.fp.close()

  def play(self):
    if isWindows():
      #TODO Realtime e.g. create wav file
      winsound.PlaySound(self.path, winsound.SND_FILENAME | winsound.SND_ASYNC)

  def getData(self):
      return self.mono

  def getRawData(self):
      return self.rawMono

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

  def writeRawData(self, string):
    self.fp.writeframes(string)

  def writeData(self, data):
    raw = ""
    for sample in data:
        raw += struct.pack('<h', sample)

    self.writeRawData(raw)
