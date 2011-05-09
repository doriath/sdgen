import os
from setuptools import setup

def read(file_name):
  return open(os.path.join(os.path.dirname(__file__), file_name)).read()

setup(
  name = "sdgen",
  version = "0.0.1",
  author = "Tomasz Zurkowski, Piotr Slatala, Marek Kuzora, Anna Fenster",
  author_email = "doriath88@gmail.com piotr@sepio.pl marek.kuzora@gmail.com noireffe@gmail.com",
  description = "",
  licence = "MIT",
  keywords = "diagram generator",
  url = "http://github.com/doriath/sdgen",
  packages = ["sdgen", "tests"],
  long_description = read("README"),
  classifiers = [],
)
