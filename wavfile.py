#!/usr/bin/python2

import wave
import sys
import struct

import numpy

from filters import Filters

def isWindows():
  return sys.platform == "win32"

if isWindows():
  import winsound

class WavFileReader:

  def __init__(self, path):

    self.path = path
    self.fp = wave.open(path, "r")

    raw = []
    data = numpy.zeros(self.getNumFrames()*2+1)

    # 32bit
    if self.getBitDepth() == 4:
        for i in range(self.getNumFrames()):
            waveFrame = self.fp.readframes(1)
            if self.getNumChannels() == 2:
                data[2*i] = (struct.unpack("<i<i", waveFrame[:4])[0] >> 16)
                data[2*i+1] = (struct.unpack("<i<i", waveFrame[-4:])[0] >> 16)
            else:
                data[i] = (struct.unpack("<i", waveFrame)[0] >> 16)

    # 16bit
    elif self.getBitDepth() == 2:
        for i in range(self.getNumFrames()):
            waveFrame = self.fp.readframes(1)
            if self.getNumChannels() == 2:
                data[2*i] = struct.unpack("<h", waveFrame[:2])[0]
                data[2*i+1] = struct.unpack("<h", waveFrame[-2:])[0]
            else:
                data[i] = struct.unpack("<h", waveFrame)[0]

    else:
      raise Error()


    # convert dual channel to single channel (mono)
    if self.getNumChannels() == 2:

        self.mono = numpy.zeros(len(data)/2+1)

        for i in range(len(data)/2):
            self.mono[i] = (data[2*i] + data[2*i+1])/2
    else:
        self.mono = data[:len(data)/2+1]

    if self.getSampleFrequency() != Filters.FREQ:
        self.mono = Filters.Resample(self.mono, float(Filters.FREQ)/self.getSampleFrequency())

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
    rawMono = ""
    for sample in self.mono:
        rawMono += struct.pack("<h", sample)
    return rawMono

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
    self.data = numpy.array([])

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
