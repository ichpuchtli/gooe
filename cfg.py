#!/usr/bin/python2

class USBConfig:

  # Constants
  LATCH = "latched"
  HOLD = "hold"

  ECHO = "echo"
  DELAY = "delay"
  LFO = "lfo"
  NO_EFFECT = "no_effect"

  def __init__(self):
    self.wavSizes = [0] * 16
    self.effects = [USBConfig.NO_EFFECT] * 4
    self.wavLatchHold = [USBConfig.HOLD] * 16
    self.wavFiles = [""] * 16
    self.tempo = 240

  def setWavFile(self, wavNum, wavFilePath):
    self.wavFiles[wavNum] = wavFilePath

  def getWaveFile(self, wavNum):
    return self.wavFiles[wavNum]

  def clearWavFile(self, wavNum):
    self.setWavFile(wavNum, "")

  def setTempo(self, tempo):
    self.tempo = tempo

  def setWaveSize(self, wavNum, size):
    self.wavSizes[wavNum] = size

  def getWaveSize(self, wavNum):
    return self.wavSizes[wavNum]
  
  def zeroWaveSize(self, wavNum):
    self.setWaveSize(wavNum, 0)

  def setLatch(self, wavNum):
    self.setLatchHold(wavNum, USBConfig.LATCH)

  def setHold(self, wavNum):
    self.setLatchHold(wavNum, USBConfig.HOLD)

  def setLatchHold(self, wavNum, HoldLatch):
    self.wavLatchHold[wavNum] = HoldLatch

  def getLatchHold(self, wavNum):
    return self.wavLatchHold[wavNum]

  def setEffect(self, knobNum, effect):
    self.effects[knobNum] = effect

  def getEffect(self, knobNum):
    return self.effects[knobNum]

  def setEcho(self, knobNum):
    self.setEffect(knobNum, USBConfig.ECHO)

  def toFile(self, path):
    filp = open(path,"wb")
    filp.write(self.toText())
    filp.close()

  def toText(self):

    text = ""

    for i in range(16):
      text += str(self.getWaveSize(i)) + "\n"

    text += str(self.tempo) + "\n"
    """
    for i in range(4):
      text += str(self.getEffect(i)) + "\n"

    for i in range(16):
      text += str(self.getLatchHold(i)) + "\n"
    """

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
