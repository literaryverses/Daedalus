from objects import Grid, TriGrid, HexGrid
from alphabet import mask_word
from maze_generation import *
from re import compile


def get_response(message: str) -> str:
  p_message = message.lower()

  # get dimensions via regex
  dimRegex = compile(r'\$dim\s(\d+x\d+(?:x\d+)?)')
  dim = dimRegex.findall(p_message)
  if dim and len(dim) == 1:
    dim = dim[0].split('x')
    if len(dim) < 3:
      dim.append(1)
    gridx, gridy, gridz = [int(d) for d in dim]
  elif dim:  # extra dimensions were provided
    return 'Please only give one set of dimensions'

  # get masks via regex
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
  if p_message == '$bot hello' or p_message == '$bot hi':
    return f"\n{mask_word('hi')}"

  # instructions when requested
  if p_message == '$bot $help':
    note = 'THE FOLLOWING PARAMETERS ARE REQUIRED TO MAKE A MAZE:\n'
    note += '\n\'$bot\' to recieve a response from a bot\n'
    note += '\n\'$side [number = 3 or 4 or 6]\'\n'
    note += 'To determine number of sides of a cell\n'
    note += '\n\'$dim [number]x[number]\'\n'
    note += 'To create dimensions of cell (can add one additional dimension to give the maze \'height\')\n'
    note += '\n$algo [algorithm] to define the maze-generating algorithm\n'
    note += '\nAlgorithms available:\naldousBroder\ngrowingTree\nhunt_and_kill\nwilsons\n'
    note += '\nGrowing Tree is capable of another parameter from 0 - 1 (express as decimal) that determines the number of dead ends\n'
    note += '\nTHE FOLLOWING PARAMETERS ARE OPTIONAL:\n'
    note += '\n$\'private\' after \'$bot\' for the bot to private message you\n'
    note += '\n\'$braid [proportion as decimal]\' to remove dead ends by a rate of [proportion]\n'
    note += '\n\'$mask ([number],[number]),([number],[number]),...\'\n'
    note += 'To separate individual cells from the maze by their coordinates\n'
    note += '\nExamples: $side 4 $dim 5x5x2 $algo aldousBroder\n'
    note += '\nYou can also create messages through \'$message {letters}\'\n'
    note += 'To implement it vertically, use \'$vertical\' after \'$message\'\n'
    note += '\nEXAMPLES:\n$bot $message $vertical hello world!\n$bot $side 4 $dim 5x5x2 $algo aldousBroder\n$bot $side 6 $dim 3x3 $mask (0,0),(2,0) $algo growingTree 1\n$bot $side 3 $dim 12x12 $algo wilsons $braid 0.8'
    return note

  # generate message
  vertRegex = compile(r'\$vertical(?! \$message)')
  isVertical = vertRegex.findall(p_message)  # determine if vertical
  noteRegex = compile(r'\$message\s(?:\$vertical\s)?([\w\.\!\s]+)')
  note = noteRegex.findall(p_message)  # extract message

  if note:
    note = note.pop().split()
    if isVertical:
      for i in range(len(note)):
        note[i] = ' '.join(note[i])
      final_note = '  '.join(note)
    else:
      final_note = ' '.join(note)
    return mask_word(final_note)

  # set defaults
  braid_p = cellSides = grid = algoType = 0

  # create grid
  sideRegex = compile('\$side\s(\d+)')
  cellSides = sideRegex.search(p_message)
  if not cellSides:
    pass
  elif not gridx or not gridy or not gridz:
    return 'Please check your formatting on dimensions'
  elif cellSides.group(1) == '4':
    grid = Grid(gridy, gridx, gridz)
  elif cellSides.group(1) == '3':
    grid = TriGrid(gridy, gridx, gridz)
  elif cellSides.group(1) == '6':
    grid = HexGrid(gridy, gridx, gridz)
  elif cellSides.group(1):
    return 'There are no cells with that number of sides available. Please only use 3, 4, or 6'

  # implement masking
  maskRegex = compile(r'\$mask\s')
  doMask = maskRegex.search(p_message)
  if doMask and masks:  # if mask cmd detected
    for mask_coord in masks:
      grid.mask(*mask_coord)
  elif doMask:
    return 'Please check your formatting on masks'

  # implement algorithm
  algoRegex = compile(r'\$algo\s([\w_]+)')
  algoStr = algoRegex.search(p_message)
  if not algoStr:
    pass
  else:
    algoType = algoStr.group(1)
  if algoType == 'growingtree':
    gtRegex = compile(r'growingtree\s([\d.]+)')
    sliderStr = gtRegex.search(p_message)
    if sliderStr:
      slider = float(sliderStr.group(1))
    else:
      slider = 0.5
    growingTree(grid, slider)
  elif algoType == 'wilsons':
    wilsons(grid)
  elif algoType == 'aldousbroder':
    aldousBroder(grid)
  elif algoType == 'hunt_and_kill':
    hunt_and_kill(grid)
  elif grid and algoType:
    return 'There are no available algorithms with that name. Type !help to see which algorithms are available'

  # implement braiding
  braidRegex = compile(r'\$braid\s([\d.]+)|\$braid[\s$\$]*')
  braidStr = braidRegex.search(p_message)
  if braidStr and braidStr.group(1):
    braid_p = float(braidStr.group(1))
  elif braidStr:
    braid_p = 0.5
  if braid_p:
    grid.braid(braid_p)

  # return grid
  if grid:
    return str(grid)

  # return on all other cases
  return 'I didn\'t understand what you wrote. Try typing "$bot $help"'
