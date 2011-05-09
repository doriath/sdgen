# -*- coding: utf-8 -*-
from sdgen.svg import *

data = {
  "children":
  [
    {
      "children":
      [
          {"value": "wwwww", "view": "Terminal"}
      ],
      "view": "Loop"
    },
    {
      "children":
      [
	{"value": "wwwww", "view": "Terminal"},
	{"value": "i", "view": "Terminal"}
      ],
      "view": "Detour"
    },
    {"value": "97", "view": "Terminal"},
    {
      "children":
      [
	{"value": "8", "view": "Terminal"},
	{"value": "9", "view": "Terminal"}
      ],
      "name": None,
      "view": "InvTerminal"
    },
    {
      "children":
      [
	{"value": "8", "view": "Terminal"},
	{"value": "9", "view": "Terminal"}
      ],
      "cardinality": "3",
      "name": "Separator",
      "view": "Group"
    },
    {"value": "98", "view": "Terminal"},
    {
      "children":
      [
	{"value": "-", "view": "Terminal"},
	{"value": " ", "view": "Terminal"}
      ],
      "name": "Separator",
      "view": "Non Terminal"
    },
    {
      "children":
      [
        {
          "top_children":
          [
            {"value": "wwwww", "view": "Terminal"},
            {"value": "i", "view": "Terminal"}
          ],
          "bottom_children":
          [
            {"value": "i", "view": "Terminal"},
            {
              "top_children":
              [
                {
                  "children":
                  [
                    {"value": "wwwww", "view": "Terminal"},
                    {"value": "i", "view": "Terminal"}
                  ],
                  "view": "Detour"
                },
                {"value": "wwwww", "view": "Terminal", "cardinality": "5.."},
                {"value": "i", "view": "Terminal"}
              ],
              "bottom_children":
              [
                {"value": "i", "view": "Terminal", "cardinality": "5..10"}
              ],
              "name": None,
              "view": "Alternation"
            }
          ],
          "name": None,
          "view": "Alternation"
        }
      ],
      "view": "Detour"
    }
  ],
  "name": "Grupa poczatkowa",
  "view": "Group"
}

result = as_svg(data)
print result
