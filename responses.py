from objects import Grid, TriGrid, HexGrid
from alphabet import mask_word
from maze_generation import *


def get_response(message: str) -> str:
  p_message = message.lower()

  if p_message == 'hello' or p_message == 'hi':
    return f"\n{mask_word('hi')}"

  p_message = p_message.split()

  if p_message[0] == '!message':
    if p_message[1] == '!vertical':
      for i in range(2, len(p_message)):
        p_message[i] = ' '.join(p_message[i])
      note = '  '.join(p_message[2:])
    else:
      note = ' '.join(p_message[1:])
    return mask_word(note)

  if p_message == '!help':
    note = 'The following parameters are required to create a maze\n'
    note += '\'!side [number = 3 or 4 or 6]\'\n'
    note += 'To determine number of sides of a cell\n'
    note += '\n\'!dim [number]x[number]\''
    note += 'To create dimensions of cell (can add one additional dimension to give the maze \'height\')\n'
    note += '\nThe following are optional:\n'
    note += '\n\'!braid\' to remove dead ends\n'
    note += '\n\'!mask ([number],[number]),([number],[number]),...\'\n'
    note += 'To separate individual cells from the maze by their coordinates\n'
    note += '\n!algo [algorithm] to define the maze-generating algorithm\n'
    note += 'Algorithms available:\naldousBroder\ngrowingTree\nhunt_and_kill\nrecursive_backtracker\nrecursive_division\nwilsons\n'
    note += 'Growing Tree is capable of another parameter from 0 - 1 that determines the number of dead ends\n'
    note += '\nExample: !side 4 !dim 5x5x2 !braid !algo recursive_backtracker'
    return note

  return 'I didn\'t understand what you wrote. Try typing "!help"'
