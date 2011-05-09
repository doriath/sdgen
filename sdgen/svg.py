# -*- coding: utf-8 -*-
from pysvg.structure import *
from pysvg.core import *
from pysvg.text import *
from pysvg.shape import *
from pysvg.builders import *
import json

from sdgen.fixes import *
from sdgen.utils import *
from sdgen.views import *
from sdgen.configuration import *

def as_svg(data, path = None, conf = None):
  '''
  Generate a svg image(s). This function can generate multiple images.
  @param data: input data
  @param path: path were to save files;
               if the value is None no file is saved, overwriting is forbidden (raise exception)
  @param conf: configuration to substitute the default one
  @return: a list of tuples, each tuple contains two fields: a name and an image in svg format
  '''
  return create_diagram(data, Configuration(conf))

def main():
  conf = {
    "default": {
      "thickness": 1,
      "padding": 10,
      "font" : {
        "name": "Courier",
        "size": 16,
        "typeface": "bold"
      },
      "name": {
        "padding": 10,
        "font": {
          "name": "Times",
          "size": 16,
          "typeface": "bold italic"
        }
      }
    },
    "nonterminal": {
      "font": {
        "name": "Times",
        "size": 16,
        "typeface": "bold italic"
      }
    },
    "connection": {
      "thickenss": 1,
      "marker": "normal"
    }
  }
  as_svg('examples/input.example', None, conf)

if __name__ == '__main__':
  main()
