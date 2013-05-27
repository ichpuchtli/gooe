#!/usr/bin/python2

import numpy
import scikits.samplerate as sp

class Filters:

  FREQ = 44100
  MIN_SHORT = -2**15+1
  MAX_SHORT = 2**15-1

  @staticmethod
  def BitCrusher(data, bits):

    data = Filters.FloatToInt(data)

    for i in range(len(data)):
      data[i] >>= bits
      data[i] <<= bits

    data = Filters.IntToFloat(data)

    return data

  @staticmethod
  def Clone(data):
    return numpy.array(data)

  @staticmethod
  def CloneSlice(data, lower, upper):
      return Filters.Clone(data[lower:upper])

  @staticmethod
  def InPlaceSlice(data, lower, upper):
      #del data[lower:upper]
      pass

  @staticmethod
  def ScaleVolume(data, factor):
    return data*factor

  @staticmethod
  def FloatToInt(data):
      return data.astype(int)

  @staticmethod
  def IntToFloat(data):
      return data.astype(float)

  @staticmethod
  def Peak2Peak(data):
      return numpy.amax(data) - numpy.amin(data)

  @staticmethod
  def MinMax(data):
      return numpy.amin(data), numpy.amax(data)

  @staticmethod
  def Resample(data, ratio):
    return sp.resample(data, ratio, 'linear')

  @staticmethod
  def Decimator(data, perc):
    return Filters.Resample(Filters.Resample(data,perc),1/perc) 

  @staticmethod
  def PitchShift(data, frequency):
    return Filters.Resample(data,Filters.FREQ/frequency) 

  @staticmethod
  def Delay(data, delay, alpha):

    pivot = delay*Filters.FREQ

    delayed = numpy.array(data)

    delayed.resize(len(data) + pivot)

    for i in range(len(delayed)):

      if i < pivot:
        continue

      delayed[i] = delayed[i] + data[i-pivot]*alpha

    return numpy.clip(delayed, Filters.MIN_SHORT, Filters.MAX_SHORT)

  @staticmethod
  def Echo(data, delay, alpha):

    pivot = delay*Filters.FREQ

    delayed = numpy.array(data)

    delayed.resize(len(data) + pivot)

    for i in range(len(delayed)):

      if i < pivot:
        continue

      delayed[i] = delayed[i] + delayed[i-pivot]*alpha

    return numpy.clip(delayed, Filters.MIN_SHORT, Filters.MAX_SHORT)
