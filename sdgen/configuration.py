# -*- coding: utf-8 -*-

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

class Configuration(object):
  def __init__(self, conf):
    if conf == None:
      conf = {}

    self.default = Bunch(thickness=2, padding=5, font=Bunch(name="Courier New", size=16, typeface="bold"))
    if "default" in conf:
      self.default.merge(Bunch(**conf["default"]))

    self.group = self.default.copy()
    self.group.padding = 10
    self.group.name = Bunch(padding=5, font=Bunch(name="Times New Roman", size=16, typeface="bold italic"))
    if "group" in conf:
      self.group.merge(Bunch(**conf["group"]))

    self.terminal = self.default.copy()
    if "terminal" in conf:
      self.terminal.merge(Bunch(**conf["terminal"]))

    self.nonterminal = self.default.copy()
    self.nonterminal.font = Bunch(name="Times New Roman", size=16, typeface="bold italic")
    if "nonterminal" in conf:
      self.nonterminal.merge(Bunch(**conf["nonterminal"]))

    self.invterminal = self.default.copy()
    if "invterminal" in conf:
      self.invterminal.merge(Bunch(**conf["invterminal"]))

    self.alternation = self.default.copy()
    if "alternation" in conf:
      self.alternation.merge(Bunch(**conf["alternation"]))

    self.connection = Bunch(thickness=2, marker="normal")
    if "connection" in conf:
      self.connection.merge(Bunch(**conf["connection"]))
