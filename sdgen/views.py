# -*- coding: utf-8 -*-
from pysvg.builders import *
from sdgen.utils import *

def create_element(data, conf):
  if data["view"] == "Group":
    return Group(data, conf)
  if data["view"] == "Terminal":
    return Terminal(data, conf)
  if data["view"] == "InvTerminal":
    return InvTerminal(data, conf)
  if data["view"] == "NonTerminal":
    return NonTerminal(data, conf)
  if data["view"] == "Alternation":
    return Alternation(data, conf)
  if data["view"] == "Detour":
    return Detour(data, conf)
  if data["view"] == "Return":
    return Return(data, conf)
  if data["view"] == "QuantityAbove":
    return QuantityAbove(data, conf)
  if data["view"] == "Sequence":
    return Sequence(data, conf)
  raise ValueError("Unknow view: " + data['view'])

def create_diagram(data, conf):
  diagram = Group(data, conf)
  s = svg()
  d = defs()
  d.addElement(arrow())
  s.addElement(d)
  diagram.render_content(s, 0, 0)
  return s.getXML()

class QuantityAbove(object):
  def __init__(self, data, conf):
    assert len(data["children"]) == 1
    self.padding = conf.default.padding
    self.content = create_element(data["children"][0], conf)
    self.text = Text(data["value"], Font(conf.default.font))
    self.width = self.content.width
    self.height = self.content.height + self.text.height + self.padding
    self.connect_y = self.content.connect_y + self.text.height + self.padding

  def render(self, svg, x, y):
    self.text.render(svg, x + self.content.width / 2 - self.text.width / 2, y)
    self.content.render(svg, x, y + self.text.height + self.padding)

class SimpleArrows(object):
  def __init__(self, data, conf):
    self.conf = conf
    self.width = self.content_width + 20
    self.height = self.content_height
    self.connect_y = self.content_height / 2

  def render(self, svg, x, y):
    self.render_content(svg, x + 10, y)
    shape_builder = ShapeBuilder()

    Line(10, 0, self.conf, arrow=True).render(svg, x, y + self.content_height / 2)

    l = shape_builder.createLine(x + self.content_width + 10, y + self.content_height / 2, x + self.content_width + 20, y + self.content_height / 2, strokewidth=self.conf.connection.thickness)
    svg.addElement(l)

class Terminal(SimpleArrows):
  def __init__(self, data, conf):
    self.text = PrettyText(data["value"], Font(conf.terminal.font))
    self.padding = conf.terminal.padding
    self.content_width = self.text.width + 2 * self.padding
    self.content_height = self.text.height + 2 * self.padding
    SimpleArrows.__init__(self, data, conf)

  def render_content(self, svg, x, y):
    shape_builder = ShapeBuilder()
    frame = shape_builder.createRect(x, y, self.content_width, self.content_height, self.content_height / 2 - 1, self.content_height / 2 - 1, strokewidth=self.conf.terminal.thickness)
    svg.addElement(frame)

    self.text.render(svg, x + self.padding, y + self.padding)

class InvTerminal(SimpleArrows):
  def __init__(self, data, conf):
    self.padding = conf.invterminal.padding
    self.children = []
    self.content_width = self.content_height = 0
    self.conf = conf
    for raw_child in data['children']:
      child = PrettyText(raw_child["value"], Font(conf.invterminal.font))
      child.color = 'white'
      self.content_width += child.width + 2 * self.padding
      self.content_height = max(self.content_height, child.height)
      self.children.append(child)
    self.content_height += 2 * self.padding
    SimpleArrows.__init__(self, data, conf)

  def render_content(self, svg, x, y):
    shape_builder = ShapeBuilder()
    frame = shape_builder.createRect(x, y, self.content_width, self.content_height, self.content_height / 2 - 1, self.content_height / 2 - 1, fill='black', strokewidth=self.conf.invterminal.thickness)
    svg.addElement(frame)

    first = True
    for child in self.children:
      if first:
        first = False
      else:
        l = shape_builder.createLine(x, y + 3, x, y + self.content_height - 3, stroke = 'white', strokewidth=self.conf.connection.thickness)
        svg.addElement(l)

      child.render(svg, x + self.padding, y + self.padding)
      x += child.width + 2 * self.padding

class NonTerminal(SimpleArrows):
  def __init__(self, data, conf):
    self.text = PrettyText(data["name"], Font(conf.nonterminal.font))
    self.padding = conf.nonterminal.padding
    self.data = data
    self.conf = conf
    self.content_width = self.text.width + 2 * self.padding
    self.content_height = self.text.height + 2 * self.padding
    SimpleArrows.__init__(self, data, conf)

  def render_content(self, svg, x, y):
    shape_builder = ShapeBuilder()
    frame = shape_builder.createRect(x, y, self.content_width, self.content_height, 0, strokewidth=self.conf.nonterminal.thickness)
    svg.addElement(frame)

    self.text.render(svg, x + self.padding, y + self.padding)

class GroupBody(object):
  def __init__(self, data, conf):
    self.padding = conf.group.padding
    self.conf = conf
    self.content = Sequence(data["children"], conf)

    self.content_width = self.content.width
    self.width = self.content_width + 2 * self.padding + 20
    self.height = self.content.height + 2 * self.padding

  def render(self, svg, x, y):
    stroke_width = self.conf.connection.thickness
    x += self.padding

    # draw arrows
    shape_builder = ShapeBuilder()
    connect_y = y + self.padding + self.content.connect_y
    l = shape_builder.createLine(x, connect_y, x + 10, connect_y, strokewidth=stroke_width)
    svg.addElement(l)
    l = shape_builder.createLine(x + self.content_width + 10, connect_y, x + self.content_width + 11, connect_y, strokewidth=stroke_width)
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
    self.header_text = Text(data["name"], Font(conf.group.name.font), 'white')
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
    frame = shape_builder.createRect(x, y, self.content_width, self.content_height, strokewidth=self.conf.group.thickness)
    svg.addElement(frame)

    header_box = shape_builder.createRect(x, y, self.header_width, self.header_height, fill='black', strokewidth=self.conf.group.thickness)
    svg.addElement(header_box)

    self.header_text.render(svg, x + self.header_padding, y + self.header_padding)

class Sequence(object):
  def __init__(self, data, conf):
    self.width = 0
    self.height_above = 0
    self.height_below = 0
    self.children = []
    raw_children = data
    if isinstance(data, dict):
      raw_children = data["children"]
    for raw_child in raw_children:
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
    self.conf = conf
    self.padding = conf.alternation.padding
    self.children = []
    for raw_child in data['children']:
      self.children.append(create_element(raw_child, conf))

    self.height = 0
    self.content_width = 0
    for child in self.children:
      self.height += child.height + self.padding
      self.content_width = max(self.content_width, child.width)
    self.height -= self.padding
    self.width = self.content_width + 40
    self.connect_y = self.height / 2

  def render(self, svg, x, y):
    stroke_width = self.conf.connection.thickness
    shape_builder = ShapeBuilder()
    start_x = x
    start_y = y + self.connect_y
    end_x = x + self.content_width + 20

    x += 20
    for child in self.children:
      child.render(svg, x, y)

      l = shape_builder.createLine(x + child.width, y + child.connect_y, x + self.content_width, y + child.connect_y, strokewidth=stroke_width)
      svg.addElement(l)
      path_data = "m {0},{1} c {2},0 0,{3} {2},{3}".format(start_x, start_y, 20, y + child.connect_y - start_y)
      svg.addElement(path(path_data, stroke = "black", fill="none", stroke_width=stroke_width))
      path_data = "m {0},{1} c {2},0 0,{3} {2},{3}".format(end_x, y + child.connect_y, 20, start_y - (y + child.connect_y))
      svg.addElement(path(path_data, stroke = "black", fill="none", stroke_width=stroke_width))

      y += child.height + self.padding

class Detour(object):
  def __init__(self, data, conf):
    self.conf = conf
    self.content = Sequence(data["children"], conf)
    self.width = self.content.width + 40
    self.height = self.content.height + 20
    self.connect_y = self.content.height / 2

  def render(self, svg, x, y):
    stroke_width = self.conf.connection.thickness

    shape_builder = ShapeBuilder()
    connect_y = y + self.connect_y
    bottom_y = y + self.content.height + 10

    self.content.render(svg, x + 20, y)

    path_data = "m {0},{1} c 10,0 10,{3} {2},{3}".format(x, connect_y, 20, bottom_y - connect_y)
    svg.addElement(path(path_data, stroke = "black", fill = "none", stroke_width=stroke_width))
    path_data = "m {0},{1} c 10,0 10,{3} {2},{3}".format(x + 20 + self.content.width, bottom_y, 20, connect_y - bottom_y)
    svg.addElement(path(path_data, stroke = "black", fill = "none", stroke_width=stroke_width))

    l = shape_builder.createLine(x + 20 + self.content.width / 2, bottom_y, x + 20 + self.content.width / 2, bottom_y, strokewidth=stroke_width)
    l._attributes['marker-end'] = 'url(#right-arrow)'
    svg.addElement(l)
    l = shape_builder.createLine(x + 20, bottom_y, x + 20 + self.content.width, bottom_y, strokewidth=stroke_width)
    svg.addElement(l)
    l = shape_builder.createLine(x, connect_y, x + 20, connect_y, strokewidth=stroke_width)
    svg.addElement(l)
    l = shape_builder.createLine(x + 20 + self.content.width, connect_y, x + 20 + self.content.width + 20, connect_y, strokewidth=stroke_width)
    svg.addElement(l)

class Return(object):
  def __init__(self, data, conf):
    self.conf = conf
    self.content = Sequence(data["children"], conf)
    self.width = self.content.width + 40
    self.height = self.content.height + 20
    self.connect_y = self.content.connect_y + 20

  def render(self, svg, x, y):
    self.content.render(svg, x + 20, y + 20)

    stroke_width = self.conf.connection.thickness

    connect_y = y + self.connect_y
    above_y = connect_y - self.content.height_above - 10
    path_data = "m {0},{1} c -10,0 -10,{3} 0,{3}".format(x + 20, connect_y, 20, above_y - connect_y)
    svg.addElement(path(path_data, stroke = "black", fill = "none", stroke_width=stroke_width))
    path_data = "m {0},{1} c 10,0 10,{3} 0,{3}".format(x + 20 + self.content.width, above_y, 20, connect_y - above_y)
    svg.addElement(path(path_data, stroke = "black", fill = "none", stroke_width=stroke_width))
    shape_builder = ShapeBuilder()
    l = shape_builder.createLine(x + 20 + self.content.width / 2, above_y, x + 19 + self.content.width / 2, above_y, strokewidth=stroke_width)
    l._attributes['marker-end'] = 'url(#right-arrow)'
    svg.addElement(l)
    l = shape_builder.createLine(x + 20, above_y, x + 20 + self.content.width, above_y, strokewidth=stroke_width)
    svg.addElement(l)
    l = shape_builder.createLine(x, connect_y, x + 20, connect_y, strokewidth=stroke_width)
    svg.addElement(l)
    l = shape_builder.createLine(x + 20 + self.content.width, connect_y, x + 20 + self.content.width + 20, connect_y, strokewidth=stroke_width)
    svg.addElement(l)
