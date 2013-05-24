#!/usr/bin/python2

class Filter:

  def apply(self, frames):
    raise Error()


class VolumeFilter(Filter):

  def __init__(self, level_perc):
    self.perc = level_perc

  def apply(self, frames):
    for byte in frames:
      byte *= self.perc
