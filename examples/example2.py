# -*- coding: utf-8 -*-
import sys
sys.path.append('.')
from sdgen.svg import *

data = {
  'children':
  [
    {
      'children':
      [
        {
          'children':
          [
            {'value': '97', 'view': 'Terminal'},
            {
              'children':
              [
                {'value': '8', 'view': 'Terminal'},
                {'value': '9', 'view': 'Terminal'}
              ],
              'view': 'InvTerminal'
            },
            {
              'children':
              [
                {
                  'children':
                  [
                    {'value': '-', 'view': 'Terminal'},
                    {'value': ' ', 'view': 'Terminal'}
                  ],
                  'view': 'InvTerminal'
                }
              ],
              'name': "Separator",
              'view': 'NonTerminal'
            }
          ],
          'name': u"Grupa początkowa",
          'view': 'Group'
        }
      ],
      'view': 'Detour'
    },
    {
      'children':
      [
        {
          'children':
          [
            {'value': '0..9', 'view': 'Terminal'}
          ],
          'view': 'InvTerminal'
        }
      ],
      'value': '1..5',
      'view': 'QuantityAbove'
    },
    {
      'children':
      [
        {
          'children':
          [
            {'type': 'Character', 'value': '-', 'view': 'Terminal'},
            {'type': 'Character', 'value': ' ', 'view': 'Terminal'}
          ],
          'view': 'InvTerminal'
        }
      ],
      'name': "Separator",
      'view': 'NonTerminal'
    },
    {
      'children':
      [
        {
          'children':
          [
            {'value': '0..9', 'view': 'Terminal'}
          ],
          'name': None,
          'view': 'InvTerminal'
        }
      ],
      'value': '2..7',
      'view': 'QuantityAbove'
    },
    {
      'children':
      [
        {
          'children':
          [
            {'value': '-', 'view': 'Terminal'},
            {'value': ' ', 'view': 'Terminal'}
          ],
          'name': None,
          'view': 'InvTerminal'
        }
      ],
      'name': "Separator",
      'view': 'NonTerminal'
    },
    {
      'children':
      [
        {
          'children':
          [
            {'type': 'Range', 'value': '0..9', 'view': 'Terminal'}
          ],
          'type': 'CharacterClass',
          'name': None,
          'view': 'InvTerminal'
        }
      ],
      'value': '1..6',
      'view': 'QuantityAbove'
    },
    {
      'children':
      [
        {
          'children':
          [
            {'value': '-', 'view': 'Terminal'},
            {'value': ' ', 'view': 'Terminal'}
          ],
          'name': None,
          'view': 'InvTerminal'
        }
      ],
      'name': "Separator",
      'view': 'NonTerminal'
    },
    {
      'children':
      [
        {'value': '0..9', 'view': 'Terminal'},
        {'value': 'X', 'view': 'Terminal'}
      ],
      'name': None,
      'view': 'InvTerminal'
    }
  ],
  'name': u"Identyfikator publikacji",
  'view': "Group"
}

result = as_svg(data)
print result[0][1].encode('utf-8')
