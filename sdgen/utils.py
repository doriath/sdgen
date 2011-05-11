# -*- coding: utf-8 -*-
from pysvg.builders import *
from pysvg.structure import *
from pysvg.text import *
from pysvg.shape import *
import Tkinter as tk
import tkFont

# required for calculating size of the text
tk.Tk()

class Font(object):
  def __init__(self, conf):
    self.size = int(conf.size)
    self.family = conf.name

    if conf.typeface.find("italic") != -1:
      self.style = "italic"
    else:
      self.style = "normal"

    if conf.typeface.find("bold") != -1:
      self.weight = "bold"
    else:
      self.weigth = "normal"

class Text(object):
  def __init__(self, content, font, color='black', raw=False):
    self.content = content
    self.font = Font(font)

    if not raw:
      if self.content == " ":
        self.content = "spacja"
        self.font.style = "italic"
        self.font.family = "Times"
      self.content = self.content.replace(" ", u'\u02FD')

    self.color = color
    (self.width, self.height) = self.calculateTextSize(self.content, self.font.family, self.font.size, self.font.weight, self.font.style)

  def calculateTextSize(self, content, family, size, weight, style):
    if style == 'normal':
      style = 'roman'
    font = tkFont.Font(family=family, size = size, weight = weight, slant = style)
    (w,h) = (font.measure(content),font.metrics("linespace"))
    return (w,h/2)

  def render(self, svg, x, y):
    shape_builder = ShapeBuilder()
    frame = shape_builder.createRect(x, y, self.width, self.height)
    svg.addElement(frame)

    t = text(self.content, x, y + self.height)
    t.set_font_size(self.font.size)
    t.set_font_family(self.font.family)
    t.set_font_style(self.font.style)
    t.set_font_weight(self.font.weight)
    t.set_fill(self.color)
    svg.addElement(t)

# TODO small, normal, big
class arrow(g):
  def __init__(self):
    BaseElement.__init__(self, 'marker')
    self._attributes['id'] = 'right-arrow'
    self._attributes['viewBox'] = '0 0 10 10'
    self._attributes['refX'] = '0'
    self._attributes['refY'] = '5'
    self._attributes['markerUnits'] = 'strokeWidth'
    self._attributes['markerWidth'] = '5'
    self._attributes['markerHeight'] = '3'
    self._attributes['orient'] = 'auto'
    self.addElement(path("M 0 0 L 10 5 L 0 10 z"))
