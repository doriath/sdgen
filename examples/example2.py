from sdgen.svg import *

data = {
  'children':
  [
    {
      'type': 'OptionQuantity',
      'children':
      [
        {
          'children':
          [
            {'type': 'Number', 'value': '97', 'view': 'Terminal'},
            {
              'children':
              [
                {'type': 'Character', 'value': '8', 'view': 'Terminal'},
                {'type':'Character', 'value': '9', 'view': 'Terminal'}
              ],
              'type':'CharacterClass',
              'name': None,
              'view': 'InvTerminal'
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
                  'type': 'CharacterClass',
                  'name': None,
                  'view': 'InvTerminal'
                }
              ],
              'type': 'Concat',
              'name': None,
              'view': 'Non Terminal'
            }
          ],
          'type': 'Concat',
          'name': None,
          'view': 'Group'
        }
      ],
      'value': '0..1',
      'view': 'quantity_detour'
    },
    {
      'type': 'RangeQuantity',
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
      'value': '1..5',
      'view': 'quantity_above'
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
          'type': 'CharacterClass',
          'name': None,
          'view': 'InvTerminal'
        }
      ],
      'type': 'Concat',
      'name': None,
      'view': 'Non Terminal'
    },
    {
      'type': 'RangeQuantity',
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
      'value': '2..7',
      'view': 'quantity_above'
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
          'type': 'CharacterClass',
          'name': None,
          'view': 'InvTerminal'
        }
      ],
      'type': 'Concat',
      'name': None,
      'view': 'NonTerminal'
    },
    {
      'type': 'RangeQuantity',
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
      'view': 'quantity_above'
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
          'type': 'CharacterClass',
          'name': None,
          'view': 'InvTerminal'
        }
      ],
      'type': 'Concat',
      'name': None,
      'view': 'NonTerminal'
    },
    {
      'children':
      [
        {'type': 'Range', 'value': '0..9', 'view': 'Terminal'},
        {'type': 'Character', 'value': 'X', 'view': 'Terminal'}
      ],
      'type': 'CharacterClass',
      'name': None,
      'view': 'InvTerminal'
    }
  ],
  'type': 'Concat',
  'name': "Main",
  'view': "Group"
}

result = as_svg(data)
print result
