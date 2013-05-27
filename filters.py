#!/usr/bin/python2

import numpy
import scikits.samplerate as sp

class Filters:

  FREQ = 44100
  MIN_SHORT = -2**15+1
  MAX_SHORT = 2**15-1

  @staticmethod
  def BitCrusher(data, bits):

    Filters.FloatToInt(data)

    for i in range(len(data)):
      data[i] >>= bits
      data[i] <<= bits

    Filters.IntToFloat(data)

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
      for i in range(len(data)):
          data[i] *= factor

  @staticmethod
  def FloatToInt(data):
      for i in range(len(data)):
          data[i] = int(data[i])

  @staticmethod
  def IntToFloat(data):
      for i in range(len(data)):
          data[i] = float(data[i])

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
  def PitchShift(data, perc):
    return Filters.Resample(data,perc) 

  @staticmethod
  def Delay(data, delay, alpha):

    pivot = delay*Filters.FREQ

    delayed = numpy.array([])

    delayed.resize(len(data) + pivot)

    for i in range(len(delayed)):

      if i < pivot:
        continue

      delayed[i] = delayed[i] + data(i-pivot)*alpha

    return numpy.clip(delayed, Filters.MIN_SHORT, Filters.MAX_SHORT)

  @staticmethod
  def Echo(data, delay, alpha):

    pivot = delay*Filters.FREQ

    delayed = numpy.array([])

    delayed.resize(len(data) + pivot)

    for i in range(len(delayed)):

      if i < pivot:
        continue

      delayed[i] = delayed[i] + delayed(i-pivot)*alpha

    return numpy.clip(delayed, Filters.MIN_SHORT, Filters.MAX_SHORT)
