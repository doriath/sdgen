# -*- coding: utf-8 -*-
from sdgen.fixes import *
from sdgen.views import *
from sdgen.configuration import *

def as_svg(data, path=None, conf=None):
  '''
  Generate a svg image(s). This function can generate multiple images.
  @param data: input data
  @param path: path were to save files;
               if the value is None no file is saved, overwriting is forbidden (raise exception)
  @param conf: configuration to substitute the default one
  @return: a list of tuples, each tuple contains two fields: a name and an image in svg format
  '''
  return create_diagram(data, Configuration(conf))
