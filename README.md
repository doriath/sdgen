Syntax Diagram Generator
========================

Installation
------------

    python setup.py install

Getting started
---------------

First, execute some examples:

    python examples/http.py > http.svg
    python examples/isbn.py > isbn.svg

Then, generate simple diagram for IP grammar:

    import sdgen.svg
    data = {
      "children": [
        {"value": "0..255", "view": "Terminal"},
        {"value": "0..255", "view": "Terminal"},
        {"value": "0..255", "view": "Terminal"},
        {"value": "0..255", "view": "Terminal"}
      ],
      "view": "Group",
      "name": "IP address"
    }

    # Generate all images to 'out' directory
    as_svg(data, "out")

Authors
-------

Tomasz Zurkowski, Piotr Slatala, Marek Kuzora, Anna Ferster

Idea & Specification of graph view & requirements invented and specified by Bartosz Alchimowicz.

Licence
-------

Syntax Diagram Generator is released under the MIT license.
