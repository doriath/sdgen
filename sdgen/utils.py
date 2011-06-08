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
            self.weight = "normal"

class Text(object):
    def __init__(self, content, font, color='black'):
        self.content = content
        self.font = font
        self.color = color
        (self.width, self.height) = self.calculate_text_size(self.content, self.font)

    def calculate_text_size(self, content, font):
        if font.style == 'normal':
            font.style = 'roman'
        tk_font = tkFont.Font(family=font.family, size=font.size, weight=font.weight, slant=font.style)
        (w, h) = (tk_font.measure(content), tk_font.metrics("linespace"))
        return (w, h)

    def render(self, svg, x, y):
        t = text(self.content, x, y + self.height * 3 / 4)
        t.set_font_size(self.font.size)
        t.set_font_family(self.font.family)
        t.set_font_style(self.font.style)
        t.set_font_weight(self.font.weight)
        t.set_fill(self.color)
        svg.addElement(t)

class PrettyText(Text):
    def __init__(self, content, font, color='black'):
        if content == " ":
            content = "spacja"
            font.style = "italic"
            font.family = "Times New Roman"
        content = content.replace(" ", u'\u02FD')
        Text.__init__(self, content, font, color)

class Line(object):
    def __init__(self, x_diff, y_diff, conf, arrow=False):
        self.x_diff = x_diff
        self.y_diff = y_diff
        self.conf = conf
        self.arrow = arrow

    def render(self, svg, x, y):
        stroke_width = self.conf.connection.thickness
        shape_builder = ShapeBuilder()
        if self.arrow:
            l = shape_builder.createLine(x, y, x + self.x_diff - self.arrow_width() * stroke_width, y + self.y_diff, strokewidth=stroke_width)
            l._attributes['marker-end'] = "url(#{0}-right-arrow)".format(self.conf.connection.marker)
            svg.addElement(l)
        else:
            l = shape_builder.createLine(x, y, x + self.x_diff, y + self.y_diff, strokewidth=stroke_width)
            svg.addElement(l)

    def arrow_width(self):
        if self.conf.connection.marker == "small":
            return 3
        if self.conf.connection.marker == "normal":
            return 5
        if self.conf.connection.marker == "large":
            return 7


class Arrow(g):
    def __init__(self, name='right-arrow', width=5):
        self.width = width

        BaseElement.__init__(self, 'marker')
        self._attributes['id'] = name
        self._attributes['viewBox'] = '0 0 20 20'
        self._attributes['refX'] = '0'
        self._attributes['refY'] = '10'
        self._attributes['orient'] = 'auto'
        self._attributes['markerWidth'] = width
        self._attributes['markerHeight'] = 2 * width
        self.addElement(path("M 0 0 L 20 10 L 0 20 z"))
