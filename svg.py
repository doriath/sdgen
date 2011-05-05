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

class Bunch(object):
  def __init__(self, **kwds):
    for key in kwds:
      if isinstance(kwds[key], dict):
        self.__dict__[key] = Bunch(**kwds[key])
      else:
        self.__dict__[key] = kwds[key]

  def merge(self, data):
    for key in data.__dict__:
      if (key in self.__dict__) and isinstance(self.__dict__[key], Bunch):
        self.__dict__[key].merge(data.__dict__[key])
      else:
        self.__dict__[key] = data.__dict__[key]

  def copy(self):
    new_bunch = Bunch()
    for key in self.__dict__:
      if isinstance(self.__dict__[key], Bunch):
        new_bunch.__dict__[key] = self.__dict__[key].copy()
      else:
        new_bunch.__dict__[key] = self.__dict__[key]
    return new_bunch

def convert(data):
  if isinstance(data, unicode):
    return str(data)
  elif isinstance(data, dict):
    return dict(map(convert, data.iteritems()))
  elif isinstance(data, (list, tuple, set, frozenset)):
    return type(data)(map(convert, data))
  else:
    return data

class Configuration(object):
  def __init__(self, conf):
    conf = convert(conf)
    self.default = Bunch(thickness = 1, padding = 10, font = Bunch(name = "Courier", size = 16, typeface = "bold"))
    if "default" in conf:
      self.default.merge(Bunch(**conf["default"]))

    self.group = self.default.copy()
    if "group" in conf:
      self.group.merge(Bunch(**conf["group"]))

    self.terminal = self.default.copy()
    if "terminal" in conf:
      self.terminal.merge(Bunch(**conf["terminal"]))

    self.nonterminal = self.default.copy()
    self.nonterminal.font = Bunch(name = "Times", size = "16", typeface = "bold italic")
    if "nonterminal" in conf:
      self.nonterminal.merge(Bunch(**conf["nonterminal"]))

    self.invterminal = self.default.copy()
    if "invterminal" in conf:
      self.invterminal.merge(Bunch(**conf["invterminal"]))

    self.alternation = self.default.copy()
    if "alternation" in conf:
      self.alternation.merge(Bunch(**conf["alternation"]))

    self.connection = Bunch(thickness = 1, marker = "normal")
    if "connection" in conf:
      self.connection.merge(Bunch(**conf["connection"]))

class Text(object):
  def __init__(self, content, font, color = 'black'):
    self.content = content
    self.font = Font(font)
    self.color = color
    self.width = len(content) * 10
    self.height = font.size * 3 / 4

  def render(self, svg, x, y):
    t = text(self.content, x, y + self.height)
    t.set_font_size(self.font.size)
    t.set_font_family(self.font.family)
    t.set_font_style(self.font.style)
    t.set_font_weight(self.font.weight)
    t.set_fill(self.color)
    svg.addElement(t)






class Cardinality(object):
  def __init__(self, content, data, conf):
    self.padding = conf.default.padding
    self.content = content
    self.text = Text(data["cardinality"], conf.default.font)
    self.width = content.width
    self.height = content.height + self.text.height + self.padding
    self.connect_y = content.connect_y + self.text.height + self.padding

  def render(self, svg, x, y):
    self.text.render(svg, x + self.content.width / 2 - self.text.width / 2, y)
    self.content.render(svg, x, y + self.text.height + self.padding)







def create_element(data, conf):
  result = None
  if data["view"] == "Group":
    result = Group(data, conf)
  if data["view"] == "Terminal":
    result = Terminal(data, conf)
  if data["view"] == "InvTerminal":
    result = InvTerminal(data, conf)
  if data["view"] == "Non Terminal":
    result = NonTerminal(data, conf)
  if data["view"] == "Alternation":
    result = Alternation(data, conf)
  if data["view"] == "Detour":
    result =  Detour(data, conf)
  if data["view"] == "Loop":
    result =  Loop(data, conf)

  if result == None:
    raise "Unknow view"

  if "cardinality" in data:
    return Cardinality(result, data, conf)

  return result

class SimpleArrows(object):
  def __init__(self, data, conf):
    self.width = self.content_width + 20
    self.height = self.content_height
    self.connect_y = self.content_height / 2

  def render(self, svg, x, y):
    self.render_content(svg, x + 10, y)
    shape_builder = ShapeBuilder()

    l = shape_builder.createLine(x, y + self.content_height / 2, x + 10 - 9, y + self.content_height / 2, strokewidth = 3)
    l._attributes['marker-end'] = 'url(#right-arrow)'
    svg.addElement(l)

    l = shape_builder.createLine(x + self.content_width + 10, y + self.content_height / 2, x + self.content_width + 20, y + self.content_height / 2, strokewidth = 3)
    svg.addElement(l)

class Terminal(SimpleArrows):
  def __init__(self, data, conf):
    self.text = Text(data["value"], conf.terminal.font)
    self.padding = conf.terminal.padding
    self.content_width = self.text.width + 2 * self.padding
    self.content_height = self.text.height + 2 * self.padding
    SimpleArrows.__init__(self, data, conf)

  def render_content(self, svg, x, y):
    shape_builder = ShapeBuilder()
    frame = shape_builder.createRect(x, y, self.content_width, self.content_height, self.content_height / 2 - 1, self.content_height / 2 - 1)
    svg.addElement(frame)

    self.text.render(svg, x + self.padding, y + self.padding)

class InvTerminal(SimpleArrows):
  def __init__(self, data, conf):
    self.padding = conf.invterminal.padding
    self.children = []
    self.content_width = self.content_height = 0
    for raw_child in data['children']:
      child = Text(raw_child["value"], conf.nonterminal.font)
      child.color = 'white'
      self.content_width += child.width + 2 * self.padding
      self.content_height = max(self.content_height, child.height)
      self.children.append(child)
    self.content_height += 2 * self.padding
    SimpleArrows.__init__(self, data, conf)

  def render_content(self, svg, x, y):
    shape_builder = ShapeBuilder()
    frame = shape_builder.createRect(x, y, self.content_width, self.content_height, self.content_height / 2 - 1, self.content_height / 2 - 1, fill = 'black')
    svg.addElement(frame)

    first = True
    for child in self.children:
      if first:
        first = False
      else:
        l = shape_builder.createLine(x, y + 3, x, y + self.content_height - 3, stroke = 'white', strokewidth = 2)
        svg.addElement(l)

      child.render(svg, x + self.padding, y + self.padding)
      x += child.width + 2 * self.padding

class NonTerminal(SimpleArrows):
  def __init__(self, data, conf):
    self.text = Text(data["name"], conf.nonterminal.font)
    self.padding = conf.nonterminal.padding
    self.data = data
    self.conf = conf
    self.content_width = self.text.width + 2 * self.padding
    self.content_height = self.text.height + 2 * self.padding
    SimpleArrows.__init__(self, data, conf)

  def render_content(self, svg, x, y):
    shape_builder = ShapeBuilder()
    frame = shape_builder.createRect(x, y, self.content_width, self.content_height)
    svg.addElement(frame)

    self.text.render(svg, x + self.padding, y + self.padding)

    create_diagram(self.data, self.text.content + '.svg', self.conf)

class GroupBody(object):
  def __init__(self, data, conf):
    self.padding = conf.group.padding
    self.content = LinearLayout(data["children"], conf)

    self.content_width = self.content.width
    self.width = self.content_width + 2 * self.padding + 20
    self.height = self.content.height + 2 * self.padding

  def render(self, svg, x, y):
    x += self.padding

    # draw arrows
    shape_builder = ShapeBuilder()
    connect_y = y + self.padding + self.content.connect_y
    l = shape_builder.createLine(x, connect_y, x + 10, connect_y, strokewidth = 3)
    svg.addElement(l)
    l = shape_builder.createLine(x + self.content_width + 10, connect_y, x + self.content_width + 11, connect_y, strokewidth = 3)
    l._attributes['marker-end'] = 'url(#right-arrow)'
    svg.addElement(l)

    # draw children
    self.content.render(svg, x + 10, y + self.padding)


class Group(SimpleArrows):
  def __init__(self, data, conf):
    # create content and calulcate size
    self.conf = conf
    self.header_padding = conf.group.name.padding
    self.padding = conf.group.padding

    self.body = GroupBody(data, conf)

    self.content_width = 0
    self.content_height = 0

    # create header
    self.header_text = Text(data["name"], conf.group.name.font, 'white')
    self.header_width = self.header_text.width + 2 * self.padding
    self.header_height = self.header_text.height + 2 * self.padding

    self.content_width = max(self.body.width, self.header_width)
    self.content_height = self.body.height + self.header_height
    SimpleArrows.__init__(self, data, conf)

  def render_content(self, svg, x, y):
    self.render_frame(svg, x, y)
    self.body.render(svg, x, y + self.header_height)

  def render_frame(self, svg, x, y):
    shape_builder = ShapeBuilder()
    frame = shape_builder.createRect(x, y, self.content_width, self.content_height)
    svg.addElement(frame)

    header_box = shape_builder.createRect(x, y, self.header_width, self.header_height, fill = 'black')
    svg.addElement(header_box)

    self.header_text.render(svg, x + self.header_padding, y + self.header_padding)


class LinearLayout(object):
  def __init__(self, data, conf):
    self.width = 0
    self.height_above = 0
    self.height_below = 0
    self.children = []
    for raw_child in data:
      child = create_element(raw_child, conf)
      self.width += child.width
      self.height_above = max(self.height_above, child.connect_y)
      self.height_below = max(self.height_below, child.height - child.connect_y)
      self.children.append(child)
    self.height = self.height_above + self.height_below
    self.connect_y = self.height_above

  def render(self, svg, x, y):
    max_height = 0
    for child in self.children:
      max_height = max(max_height, child.height)

    connect_y = y + self.connect_y
    for child in self.children:
      child.render(svg, x, connect_y - child.connect_y)
      x += child.width


class Alternation(object):
  def __init__(self, data, conf):
    self.padding = conf.alternation.padding
    self.top = LinearLayout(data['top_children'], conf)
    self.bottom = LinearLayout(data['bottom_children'], conf)

    self.height = self.top.height + self.bottom.height + self.padding
    self.content_width = max(self.top.width, self.bottom.width)
    self.width = self.content_width + 40
    self.connect_y = self.height / 2

  def render(self, svg, x, y):
    shape_builder = ShapeBuilder()
    start_x = x
    start_y = y + self.connect_y
    end_x = x + self.content_width + 20

    x += 20
    for child in [self.top, self.bottom]:
      child.render(svg, x, y)

      l = shape_builder.createLine(x + child.width, y + child.connect_y, x + self.content_width, y + child.connect_y, strokewidth = 3)
      svg.addElement(l)
      path_data = "m {0},{1} c {2},0 0,{3} {2},{3}".format(start_x, start_y, 20, y + child.connect_y - start_y)
      svg.addElement(path(path_data, stroke = "black", fill = "none", stroke_width = 3))
      path_data = "m {0},{1} c {2},0 0,{3} {2},{3}".format(end_x, y + child.connect_y, 20, start_y - (y + child.connect_y))
      svg.addElement(path(path_data, stroke = "black", fill = "none", stroke_width = 3))

      y += child.height + self.padding

class Detour(object):
  def __init__(self, data, conf):
    self.content = LinearLayout(data["children"], conf)
    self.width = self.content.width + 40
    self.height = self.content.height + 20
    self.connect_y = self.content.height / 2

  def render(self, svg, x, y):
    shape_builder = ShapeBuilder()
    connect_y = y + self.connect_y
    bottom_y = y + self.content.height + 10

    self.content.render(svg, x + 20, y)

    path_data = "m {0},{1} c 10,0 10,{3} {2},{3}".format(x, connect_y, 20, bottom_y - connect_y)
    svg.addElement(path(path_data, stroke = "black", fill = "none", stroke_width = 3))
    path_data = "m {0},{1} c 10,0 10,{3} {2},{3}".format(x + 20 + self.content.width, bottom_y, 20, connect_y - bottom_y)
    svg.addElement(path(path_data, stroke = "black", fill = "none", stroke_width = 3))

    l = shape_builder.createLine(x + 20 + self.content.width / 2, bottom_y, x + 20 + self.content.width / 2, bottom_y, strokewidth = 3)
    l._attributes['marker-end'] = 'url(#right-arrow)'
    svg.addElement(l)
    l = shape_builder.createLine(x + 20, bottom_y, x + 20 + self.content.width, bottom_y, strokewidth = 3)
    svg.addElement(l)
    l = shape_builder.createLine(x, connect_y, x + 20, connect_y, strokewidth = 3)
    svg.addElement(l)
    l = shape_builder.createLine(x + 20 + self.content.width, connect_y, x + 20 + self.content.width + 20, connect_y, strokewidth = 3)
    svg.addElement(l)

class Loop(object):
  def __init__(self, data, conf):
    self.content = LinearLayout(data["children"], conf)
    self.width = self.content.width + 40
    self.height = self.content.height + 20
    self.connect_y = self.content.connect_y + 20

  def render(self, svg, x, y):
    self.content.render(svg, x + 20, y + 20)

    connect_y = y + self.connect_y
    above_y = connect_y - self.content.height_above - 10
    path_data = "m {0},{1} c -10,0 -10,{3} 0,{3}".format(x + 20, connect_y, 20, above_y - connect_y)
    svg.addElement(path(path_data, stroke = "black", fill = "none", stroke_width = 3))
    path_data = "m {0},{1} c 10,0 10,{3} 0,{3}".format(x + 20 + self.content.width, above_y, 20, connect_y - above_y)
    svg.addElement(path(path_data, stroke = "black", fill = "none", stroke_width = 3))

    shape_builder = ShapeBuilder()
    l = shape_builder.createLine(x + 20 + self.content.width / 2, above_y, x + 19 + self.content.width / 2, above_y, strokewidth = 3)
    l._attributes['marker-end'] = 'url(#right-arrow)'
    svg.addElement(l)
    l = shape_builder.createLine(x + 20, above_y, x + 20 + self.content.width, above_y, strokewidth = 3)
    svg.addElement(l)
    l = shape_builder.createLine(x, connect_y, x + 20, connect_y, strokewidth = 3)
    svg.addElement(l)
    l = shape_builder.createLine(x + 20 + self.content.width, connect_y, x + 20 + self.content.width + 20, connect_y, strokewidth = 3)
    svg.addElement(l)


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

def create_diagram(data, output, conf):
  diagram = Group(data, conf)
  s = svg()

  d = defs()
  m = arrow()
  d.addElement(m)
  s.addElement(d)

  diagram.render_content(s, 0, 0)

  # print s.getXML()
  s.save(output)

def main():
  conf = json.loads(open('conf.example').read())
  data = json.loads(open('input.example').read())
  create_diagram(data, 'out.svg', Configuration(conf))

if __name__ == '__main__':
  main()
