from objects import Grid, TriGrid, HexGrid
from alphabet import mask_word
from maze_generation import *
from re import compile


def get_response(message: str) -> str:
  p_message = message.lower()

  # get dimensions
  dimRegex = compile(r'\d+x\d+(?:x\d+)?')
  dim = dimRegex.findall(p_message)
  if dim and len(dim) == 1:
    dim = dim[0].split('x')
    if len(dim) < 3:
      dim.append(1)
    gridx, gridy, gridz = [int(d) for d in dim]
  elif dim:  # extra dimensions were provided
    return 'Please only give one set of dimensions'

  # get masks
  masks = []
  maskRegex = compile(r'\d+,\d+(?:,\d+)?|\d+, \d+(?:, \d+)?')
  for mask in maskRegex.findall(p_message):
    if mask[mask.index(',') + 1].isdigit():
      mask = [int(d) for d in mask.split(',')]
    else:
      mask = [int(d) for d in dim.split(', ')]
    if len(mask) < 3:
      mask.append(0)
    x, y, z = mask
    masks.append((y, x, z))

  # response to hello or hi
  if p_message == 'hello' or p_message == 'hi':
    return f"\n{mask_word('hi')}"

  # instructions when requested
  if p_message == '!help':
    note = 'The following parameters are required to create a maze\n'
    note += '\'!side [number = 3 or 4 or 6]\'\n'
    note += 'To determine number of sides of a cell\n'
    note += '\n\'!dim [number]x[number]\''
    note += 'To create dimensions of cell (can add one additional dimension to give the maze \'height\')\n'
    note += '\n!algo [algorithm] to define the maze-generating algorithm\n'
    note += 'Algorithms available:\naldousBroder\ngrowingTree\nhunt_and_kill\nwilsons\n'
    note += '\nThe following are optional:\n'
    note += '\n\'!braid\' to remove dead ends\n'
    note += '\n\'!mask ([number],[number]),([number],[number]),...\'\n'
    note += 'To separate individual cells from the maze by their coordinates\n'
    note += '\nExample: !side 4 !dim 5x5x2 !braid !algo aldousBroder'
    note += '\nYou can also create messages through \'!message {letters}\'\n'
    note += 'To implement it vertically, use \'!vertical\' in between'
    note += '\nExample: !message !vertical hello world!'
    return note

  p_message = p_message.split()

  # creating mazes based off message
  if p_message[0] == '!message':
    if p_message[1] == '!vertical':
      for i in range(2, len(p_message)):
        p_message[i] = ' '.join(p_message[i])
      note = '  '.join(p_message[2:])
    else:
      note = ' '.join(p_message[1:])
    return mask_word(note)

  braid_p = cellType = grid = 0
  slider = 0.5  # default slider for growingTree
  #algoType = 'recursive_backtracker'  # default algo
  algoType = 0

  for i, command in enumerate(p_message):  # check other commands
    print(f'\n{i}: {command}\n')
    if command == '!braid':
      print('\nBraiding cmd\n')
      '''if p_message[i + 1].isdecimal():
        print('\nBraiding decimal check\n')
        braid_p = float(p_message[i + 1])
    else:'''
      braid_p = 1
    if command == '!side':
      print('\n checking if taking in celltype\n')
      cellType = int(p_message[i + 1])
    if command == '!algo':
      algoType = p_message[i + 1]
      '''if algoType == 'growingtree' and p_message[i + 2].isdecimal():
        slider = float(p_message[i + 2])'''
    if command == '!dim':
      if gridx and gridy and gridz:
        continue
      else:  # dimensions is not given although command is
        return 'Please check your formatting on dimensions'
    if command == '!mask':
      if not masks:  # masks are not given although command is
        return 'Please check your formatting on masks'

  # create grid
  if cellType == 4:
    grid = Grid(gridy, gridx, gridz)
  elif cellType == 3:
    grid = TriGrid(gridy, gridx, gridz)
  elif cellType == 6:
    grid = HexGrid(gridy, gridx, gridz)
  elif cellType:
    return 'There are no cells with that number of sides available. Please only use 3, 4, or 6'

  # implement masking
  for mask_coord in masks:
    grid.mask(*mask_coord)

  # implement algorithm
  if algoType == 'wilsons':
    wilsons(grid)
  elif algoType == 'growingtree':
    growingTree(grid, slider)
  elif algoType == 'aldousbroder':
    aldousBroder(grid)
  elif algoType == 'hunt_and_kill':
    hunt_and_kill(grid)
  elif grid and algoType:
    return 'There are no available algorithms with that name. Type !help to see which algorithms are available'

  # implement braiding
  if braid_p:
    grid.braid(braid_p)

  # return grid
  if grid:
    return str(grid)

  # return on all other cases
  return 'I didn\'t understand what you wrote. Try typing "!help"'
