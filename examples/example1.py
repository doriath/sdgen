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
          {"value": "w w", "view": "Terminal"}
      ],
      "view": "Return"
    },
    {
      "children":
      [
	{"value": "wwwww", "view": "Terminal"},
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
  "name": u"Grupa początkowa",
  "view": "Group"
}

result = as_svg(data)
print result[1].encode('utf-8')
