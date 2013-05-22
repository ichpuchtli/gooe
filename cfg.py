#!/usr/bin/python2

class Configuration():

  # Constants
  LATCH = "latched"
  HOLD = "hold"

  ECHO = "echo"
  DELAY = "delay"
  LFO = "lfo"

  def __init__(self):
    self.wavSizes = [0] * 16
    self.effects = [0] * 4
    self.wavLatchHold = [0] * 16

  def setWaveSize(self, wavNum, size):
    self.wavSizes[wavNum] = size

  def getWaveSize(self, wavNum):
    return self.wavSizes[wavNum]

  def setLatch(self, wavNum):
    self.setLatchHold(wavNum, Configuration.LATCH)

  def setHold(self, wavNum):
    self.setLatchHold(wavNum, Configuration.HOLD)

  def setLatchHold(self, wavNum, HoldLatch):
    self.wavLatchHold[wavNum] = HoldLatch

  def getLatchHold(self, wavNum):
    return self.wavLatchHold[wavNum]

  def setEffect(self, knobNum, effect):
    self.effects[knobNum] = effect

  def getEffect(self, knobNum):
    return self.effects[knobNum]

  def setEcho(self, knobNum):
    self.setEffect(knobNum, Configuration.ECHO)

  def toText(self):

    text = ""

    for i in range(16):
      text += str(self.getWaveSize(i)) + "\n"

    for i in range(4):
      text += str(self.getEffect(i)) + "\n"

    for i in range(16):
      text += str(self.getLatchHold(i)) + "\n"

    return text
    
  def fromText(self, text):
    i = 0
    for line in text:
      
      if(line[0] == "#"):
        continue

      if( i < 16 ):
        self.setWaveSize(i, int(line))

      if( i >= 16 and i < 20 ):
        self.setEffect(i - 16, line)

      if( i >= 20 ):
        self.setLatchHold(i - 20, line)

      i += 1
