# -*- coding: utf-8 -*-
from pysvg.structure import *
from pysvg.core import *
from pysvg.text import *
from pysvg.shape import *
from pysvg.builders import *
import json

def as_svg(data, path = None, conf = None):
  '''
  Generate a svg image(s). This function can generate multiple images.
  @param data: input data
  @param path: path were to save files;
               if the value is None no file is saved, overwriting is forbidden (raise exception)
  @param conf: configuration to substitute the default one
  @return: a list of tuples, each tuple contains two fields: a name and a image in svg format
  '''
  print 'test'

def create_element(data, conf):
  if data["view"] == "Group":
    return Group(data, conf)
  if data["view"] == "Terminal":
    return Terminal(data, conf)
  if data["view"] == "InvTerminal":
    return InvTerminal(data, conf)
  if data["view"] == "Non Terminal":
    return NonTerminal(data, conf)
  raise "Unknow view"

class Font(object):
  def __init__(self, conf):
    self.size = int(conf["size"])
    self.family = conf["name"]

    if conf["typeface"].find("italic") != -1:
      self.style = "italic"
    else:
      self.style = "normal"

    if conf["typeface"].find("bold") != -1:
      self.weight = "bold"
    else:
      self.weigth = "normal"

class Bunch:
  def __init__(self, **kwds):
    self.__dict__.update(kwds)

class Configuration(object):
  def __init__(self, conf):
    self.default = Bunch(thickness = 1, padding = 10, font = Font(conf["default"]["font"]))
    name = Bunch(padding = 10, font = Font(conf["default"]["name"]["font"]))
    self.group = Bunch(padding = 10, name = name)
    self.terminal = Bunch(padding = 10, font = self.default.font)
    self.nonterminal = Bunch(padding = 10, font = Font(conf["nonterminal"]["font"]))

class Text(object):
  def __init__(self, content, font, color = 'black'):
    self.content = content
    self.font = font
    self.color = color
    self.width = len(content) * 8
    self.height = font.size * 3 / 4

  def render(self, svg, x, y):
    t = text(self.content, x, y + self.height)
    t.set_font_size(self.font.size)
    t.set_font_family(self.font.family)
    t.set_font_style(self.font.style)
    t.set_font_weight(self.font.weight)
    t.set_fill(self.color)
    svg.addElement(t)

class Terminal(object):
  def __init__(self, data, conf):
    self.text = Text(data["value"], conf.terminal.font)
    self.padding = conf.terminal.padding
    self.width = self.text.width + 2 * self.padding
    self.height = self.text.height + 2 * self.padding

  def render(self, svg, x, y):
    shape_builder = ShapeBuilder()
    frame = shape_builder.createRect(x, y, self.width, self.height, self.height / 2 - 1, self.height / 2 - 1)
    svg.addElement(frame)

    self.text.render(svg, x + self.padding, y + self.padding)

class NonTerminal(object):
  def __init__(self, data, conf):
    self.text = Text(data["name"], conf.nonterminal.font)
    self.padding = conf.nonterminal.padding
    self.data = data
    self.conf = conf
    self.width = self.text.width + 2 * self.padding
    self.height = self.text.height + 2 * self.padding

  def render(self, svg, x, y):
    shape_builder = ShapeBuilder()
    frame = shape_builder.createRect(x, y, self.width, self.height)
    svg.addElement(frame)

    self.text.render(svg, x + self.padding, y + self.padding)

    create_diagram(self.data, self.text.content + '.svg', self.conf)

class Group(object):
  def __init__(self, data, conf):
    # create content and calulcate size
    self.conf = conf
    self.header_padding = conf.group.name.padding
    self.padding = conf.group.padding

    self.content_width = 0
    self.content_height = 0
    self.line_length = 20
    self.arrow_length = 9

    self.children = []
    for child in data["children"]:
      c = create_element(child, conf)
      self.children.append(c)
      self.content_width += self.line_length + c.width
      self.content_height = max(self.content_height, c.height)
    self.content_width += self.line_length + 2 * self.padding
    self.content_height += 2 * self.padding

    # create header
    self.header_text = Text(data["name"], conf.group.name.font, 'white')
    self.header_width = self.header_text.width + 2 * self.padding
    self.header_height = self.header_text.height + 2 * self.padding

    self.width = max(self.content_width, self.header_width)
    self.height = self.content_height + self.header_height

  def render(self, svg, x, y):
    self.render_frame(svg, x, y)
    self.render_content(svg, x, y + self.header_height)

  def render_frame(self, svg, x, y):
    shape_builder = ShapeBuilder()
    frame = shape_builder.createRect(x, y, self.width, self.height)
    svg.addElement(frame)

    header_box = shape_builder.createRect(x, y, self.header_width, self.header_height, fill = 'black')
    svg.addElement(header_box)

    self.header_text.render(svg, x + self.header_padding, y + self.header_padding)

  def render_content(self, svg, x, y):
    x += self.padding
    y += self.padding
    shape_builder = ShapeBuilder()

    max_height = 0
    for child in self.children:
      max_height = max(max_height, child.height)

    for child in self.children:
      child_y = y + (max_height - child.height) / 2
      l = shape_builder.createLine(x, child_y + child.height / 2, x + self.line_length - self.arrow_length, child_y + child.height / 2, strokewidth = 3)
      l._attributes['marker-end'] = 'url(#right-arrow)'
      svg.addElement(l)

      child.render(svg, x + self.line_length, child_y)
      x += child.width + self.line_length
    l = shape_builder.createLine(x, child_y + child.height / 2, x + self.line_length - self.arrow_length, child_y + child.height / 2, strokewidth = 3)
    l._attributes['marker-end'] = 'url(#right-arrow)'
    svg.addElement(l)

class InvTerminal(object):
  def __init__(self, data, conf):
    self.padding = 10
    self.children = []
    self.width = 0
    self.height = 0
    for raw_child in data['children']:
      child = create_element(raw_child, conf)
      child.text.color = 'white'
      self.width += child.width
      self.height = max(self.height, child.height)
      self.children.append(child)

  def render(self, svg, x, y):
    shape_builder = ShapeBuilder()
    frame = shape_builder.createRect(x, y, self.width, self.height, self.height / 2 - 1, self.height / 2 - 1, fill = 'black')
    svg.addElement(frame)

    first = True
    for child in self.children:
      if first:
        first = False
      else:
        l = shape_builder.createLine(x, y + 3, x, y + child.height - 3, stroke = 'white', strokewidth = 2)
        svg.addElement(l)

      child.text.render(svg, x + self.padding, y + self.padding)
      x += child.width

class Alternation(object):
  def __init__(self, data, conf):
    print "test"

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

def create_diagram(data, output, conf):
  diagram = Group(data, conf)
  s = svg()

  d = defs()
  m = arrow()
  d.addElement(m)
  s.addElement(d)

  diagram.render(s, 0, 0)

  print s.getXML()
  s.save(output)

def main():
  conf = json.loads(open('conf.example').read())
  data = json.loads(open('input.example').read())
  create_diagram(data, 'out.svg', Configuration(conf))

if __name__ == '__main__':
  main()
