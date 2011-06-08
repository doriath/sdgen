# -*- coding: utf-8 -*-
import sys
sys.path.append('.')
from sdgen import *

data = {
  "children":
  [
    {
      "children":
      [
          {"value": "y w", "view": "Terminal"}
      ],
      "view": "Return"
    },
    {
      "children":
      [
	{"value": "piotr", "view": "Terminal"},
	{"value": " ", "view": "Terminal"}
      ],
      "view": "Detour"
    },
    {"value": "97", "view": "Terminal"},
    {
      "children":
      [
	{"value": ".", "view": "Terminal"},
	{"value": "tomek", "view": "Terminal"}
      ],
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
          "children":
          [
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
                },
                {
                  "value": "tomek",
                  "view": "Terminal"
                },
                {
                  "children":
                  [
                    {"value": "i", "view": "Terminal"},
                    {
                      "children":
                      [
                        {
                          "children":
                          [
                            {
                              "children":
                              [
                                {"value": u"wwąww", "view": "Terminal"},
                                {"value": "i", "view": "Terminal"}
                              ],
                              "view": "Detour"
                            },
                            {
                              "children":
                              [
                                {"value": "wwwww", "view": "Terminal"},
                              ],
                              "value": "5..",
                              "view": "QuantityAbove"
                            },
                          ],
                          "view": "Sequence"
                        },
                        {
                          "children":
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
                          "view": "Sequence"
                        }
                      ],
                      "name": None,
                      "view": "Alternation"
                    }
                  ],
                  "view": "Sequence"
                }
              ],
              "name": None,
              "view": "Alternation"
            }
          ],
          "view": "Detour"
        }
      ],
      "view": "Return"
    }
  ],
  "name": u"Grupa początkowa",
  "view": "Group"
}

conf = {
  'default': {
    'thickness': 2,
    'padding': 10,
    'font': {
      'name': 'Courier',
      'size': 12,
      'typeface': 'bold',
    },
    'name': {
      'padding': 10,
        'font': {
          'name': 'Times',
          'size': 12,
          'typeface': 'bold italic',
        },
    },
  },
  'nonterminal': {
    'font': {
      'name': 'Times',
      'size': 12,
      'typeface': 'bold italic',
    },
  },
  'connection': {
    'thickness': 2,
    'marker': 'normal',
  },
}

result = as_svg(data, None)
print result[0][1].encode('utf-8')
