#!/usr/bin/python2

import numpy
import scikits.samplerate as sp

class Filters:

  @staticmethod
  def Clone(data):
    return data[:]

  @staticmethod
  def CloneSlice(data, lower, upper):
      return Filters.Clone(data[lower:upper])

  @staticmethod
  def Replace(dest, src):
      del dest[:]

      for i in range(len(src[:len(dest)])):
          dest[i] = src[i]
   
      dest.extend(src[len(dest):])

  @staticmethod
  def InPlaceSlice(data, lower, upper):
      del data[lower:upper]

  @staticmethod
  def UnderSample(data, factor):

      copy = []
      copy = Filters.Clone(data)

      for i in range(len(data)/factor):
          data[i] = copy[i*factor] 

      del data[len(data)/factor:]

      del copy

  @staticmethod
  def OverSample(data, factor):

      copy = []
      copy = Filters.Clone(data)

      for i in range(len(data)):
          for num in range(factor):
              data[(i*factor)+num] = copy[i] 

      del copy

  @staticmethod
  def ScaleVolume(data, factor):
      for sample in data:
          sample *= factor

  @staticmethod
  def FloatToInt(data):
      for i in range(len(data)):
          data[i] = int(data[i])

  @staticmethod
  def Resample(data, ratio):
      arr = numpy.array(data)
      Filters.Replace(data,sp.resample(arr, ratio, 'linear').tolist())
      Filters.FloatToInt(data)

