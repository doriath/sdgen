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
              'name': None,
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
                  'name': None,
                  'view': 'InvTerminal'
                }
              ],
              'name': "None",
              'view': 'NonTerminal'
            }
          ],
          'name': "None",
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
          'name': None,
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
          'name': None,
          'view': 'InvTerminal'
        }
      ],
      'name': "None",
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
      'name': "None",
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
      'name': "None",
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
  'name': "Main",
  'view': "Group"
}

result = as_svg(data)
print result[1].encode('utf-8')
