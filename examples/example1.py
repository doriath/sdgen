# -*- coding: utf-8 -*-
import sys
sys.path.append('.')
from sdgen.svg import *

data = {
  "children":
  [
    {
      "children":
      [
          {"value": "wwwww", "view": "Terminal"}
      ],
      "view": "Return"
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
        {
          "children":
          [
            {"value": "8", "view": "Terminal"},
            {"value": "9", "view": "Terminal"}
          ],
          "name": "Separator",
          "view": "Group"
        }
      ],
      "value": "3",
      "view": "QuantityAbove"
    },
    {"value": "98", "view": "Terminal"},
    {
      "children":
      [
	{"value": "-", "view": "Terminal"},
	{"value": " ", "view": "Terminal"}
      ],
      "name": "Separator",
      "view": "NonTerminal"
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
                {
                  "children":
                  [
                    {
                      "children":
                      [
                        {"value": "wwwww", "view": "Terminal"},
                        {"value": "i", "view": "Terminal"}
                      ],
                      "view": "Sequence"
                    }
                  ],
                  "value": "5..",
                  "view": "QuantityAbove"
                },
              ],
              "bottom_children":
              [
                {
                  "children":
                  [
                    {"value": "i", "view": "Terminal"}
                  ],
                  "value": "5..10",
                  "view": "QuantityAbove"
                }
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
