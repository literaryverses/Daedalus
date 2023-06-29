# Generates letters (5x5) within a 7x7 frame in orthogonal mazes

from objects import Grid
from random import sample


def alphabet(phrase: str):  # letter coordinates for masking
  coord_letters = []
  coord_holes = []
  y, x = 1, 1  # set original coordinates

  for letter in phrase.upper():
    if letter == 'A':
      for _x in range(x + 0, x + 5):
        coord_letters.append((y, _x))
        coord_letters.append((y + 2, _x))
      for _y in range(y + 3, y + 5):
        coord_letters.append((_y, x))
        coord_letters.append((_y, x + 4))
      for _y in range(y + 1, y + 2):
        coord_letters.append((_y, x))
        coord_letters.append((_y, x + 4))
      coord_holes.append((y + 1, x + 1))
    elif letter == 'B':
      for _y in range(y, y + 5):
        coord_letters.append((_y, x))
      for _x in range(x + 1, x + 5):
        coord_letters.append((y + 4, _x))
        coord_letters.append((y + 2, _x))
      coord_letters.append((y + 1, x + 2))
      coord_letters.append((y + 3, x + 4))
      coord_letters.append((y, x + 1))
      coord_letters.append((y, x + 2))
      coord_holes.append((y + 3, x + 1))
    elif letter == 'C':
      for _y in range(y, y + 5):
        coord_letters.append((_y, x))
      for _x in range(x + 1, x + 5):
        coord_letters.append((y, _x))
        coord_letters.append((y + 4, _x))
      coord_letters.append((y + 3, x + 4))
      coord_letters.append((y + 1, x + 4))
    elif letter == 'D':
      for _y in range(y, y + 5):
        coord_letters.append((_y, x))
      for _x in range(x + 1, x + 4):
        coord_letters.append((y, _x))
        coord_letters.append((y + 4, _x))
      for _y in range(y + 1, y + 4):
        coord_letters.append((_y, x + 4))
      coord_letters.append((y + 1, x + 3))
      coord_letters.append((y + 3, x + 3))
      coord_holes.append((y + 1, x + 1))
    elif letter == 'E':
      for _x in range(x, x + 5):
        coord_letters.append((y, _x))
        coord_letters.append((y + 2, _x))
        coord_letters.append((y + 4, _x))
      coord_letters.append((y + 1, x))
      coord_letters.append((y + 3, x))
    elif letter == 'F':
      for _x in range(x, x + 5):
        coord_letters.append((y, _x))
        coord_letters.append((y + 2, _x))
      coord_letters.append((y + 1, x))
      coord_letters.append((y + 3, x))
      coord_letters.append((y + 4, x))
    elif letter == 'G':
      for _x in range(x, x + 5):
        coord_letters.append((y, _x))
        coord_letters.append((y + 4, _x))
      for _y in range(y + 2, y + 4):
        coord_letters.append((_y, x))
        coord_letters.append((_y, x + 4))
      coord_letters.append((y + 1, x))
      coord_letters.append((y + 2, x + 3))
    elif letter == 'H':
      for _y in range(y, y + 5):
        coord_letters.append((_y, x))
        coord_letters.append((_y, x + 4))
      for _x in range(x + 1, x + 5):
        coord_letters.append((y + 2, _x))
    elif letter == 'I':
      for _x in range(x, x + 5):
        coord_letters.append((y, _x))
        coord_letters.append((y + 4, _x))
      for _y in range(y + 1, y + 5):
        coord_letters.append((_y, x + 2))
    elif letter == 'J':
      for _x in range(x, x + 4):
        coord_letters.append((y, _x))
        coord_letters.append((y + 4, _x))
      for _y in range(y + 1, y + 5):
        coord_letters.append((_y, x + 3))
      coord_letters.append((y, x + 4))
      coord_letters.append((y + 3, x))
    elif letter == 'K':
      for _y in range(y, y + 3):
        coord_letters.append((_y, x))
        coord_letters.append((_y, x + 2))
      for _y in range(y + 3, y + 5):
        coord_letters.append((_y, x))
        coord_letters.append((_y, x + 4))
        coord_letters.append((_y - 1, x + 3))
      coord_letters.append((y + 2, x + 1))
      coord_letters.append((y, x + 3))
    elif letter == 'L':
      for _x in range(x, x + 5):
        coord_letters.append((y + 4, _x))
      for _y in range(y, y + 4):
        coord_letters.append((_y, x))
    elif letter == 'M':
      for _x in range(x, x + 5):
        coord_letters.append((y, _x))
      for _y in range(y + 1, y + 5):
        coord_letters.append((_y, x))
        coord_letters.append((_y, x + 2))
        coord_letters.append((_y, x + 4))
    elif letter == 'N':
      for _y in range(y, y + 5):
        coord_letters.append((_y, x))
        coord_letters.append((_y, x + 4))
      #for _y in range(y, y+2):
      for _y in range(y + 1, y + 3):
        coord_letters.append((_y, x + 1))
        coord_letters.append((_y + 1, x + 2))
        coord_letters.append((_y + 2, x + 3))
    elif letter == 'O':
      for _x in range(x, x + 5):
        coord_letters.append((y, _x))
        coord_letters.append((y + 4, _x))
      for _y in range(y + 1, y + 5):
        coord_letters.append((_y, x))
        coord_letters.append((_y, x + 4))
      coord_holes.append((y + 1, x + 1))
    elif letter == 'P':
      for _x in range(x + 1, x + 5):
        coord_letters.append((y, _x))
        coord_letters.append((y + 2, _x))
      for _y in range(y, y + 5):
        coord_letters.append((_y, x))
      coord_letters.append((y + 1, x + 4))
      coord_holes.append((y + 1, x + 1))
    elif letter == 'Q':
      for _x in range(x, x + 4):
        coord_letters.append((y, _x))
        coord_letters.append((y + 3, _x))
      for _y in range(y + 1, y + 3):
        coord_letters.append((_y, x))
        coord_letters.append((_y, x + 3))
      coord_letters.append((y + 4, x + 3))
      coord_letters.append((y + 4, x + 4))
      coord_holes.append((y + 1, x + 1))
    elif letter == 'R':
      for _y in range(y, y + 5):
        coord_letters.append((_y, x))
      for _x in range(x + 1, x + 5):
        coord_letters.append((y, _x))
        coord_letters.append((y + 2, _x))
      coord_letters.append((y + 1, x + 4))
      for _x in range(x + 2, x + 5):
        coord_letters.append((y + 4, _x))
      coord_letters.append((y + 3, x + 2))
      coord_holes.append((y + 1, x + 1))
    elif letter == 'S':
      for _x in range(x, x + 5):
        coord_letters.append((y, _x))
        coord_letters.append((y + 2, _x))
        coord_letters.append((y + 4, _x))
      coord_letters.append((y + 1, x))
      coord_letters.append((y + 3, x + 4))
    elif letter == 'T':
      for _x in range(x, x + 5):
        coord_letters.append((y, _x))
      for _y in range(y + 1, y + 5):
        coord_letters.append((_y, x + 2))
    elif letter == 'U':
      for _x in range(x, x + 4):
        coord_letters.append((y + 4, _x))
      for _y in range(y, y + 5):
        coord_letters.append((_y, x))
        coord_letters.append((_y, x + 4))
    elif letter == 'V':
      for _y in range(y, y + 3):
        coord_letters.append((_y, x))
        coord_letters.append((_y, x + 4))
      for _y in range(y + 2, y + 4):
        coord_letters.append((_y, x + 1))
        coord_letters.append((_y + 1, x + 2))
        coord_letters.append((_y, x + 3))
    elif letter == 'W':
      for _x in range(x, x + 5):
        coord_letters.append((y + 4, _x))
      for _y in range(y, y + 4):
        coord_letters.append((_y, x))
        coord_letters.append((_y, x + 2))
        coord_letters.append((_y, x + 4))
    elif letter == 'X':
      for _y in range(y, y + 2):
        coord_letters.append((_y, x))
        coord_letters.append((_y, x + 4))
        coord_letters.append((_y + 3, x))
        coord_letters.append((_y + 3, x + 4))
      for _y in range(y + 1, y + 4):
        coord_letters.append((_y, x + 1))
        coord_letters.append((_y, x + 3))
      coord_letters.append((y + 2, x + 2))
    elif letter == 'Y':
      for _y in range(y, y + 2):
        coord_letters.append((_y, x))
        coord_letters.append((_y, x + 4))
      for _x in range(x, x + 5):
        coord_letters.append((y + 2, _x))
        coord_letters.append((y + 4, _x))
      coord_letters.append((y + 3, x + 4))
    elif letter == 'Z':
      for _x in range(x, x + 5):
        coord_letters.append((y, _x))
        coord_letters.append((y + 2, _x))
        coord_letters.append((y + 4, _x))
      coord_letters.append((y + 1, x + 4))
      coord_letters.append((y + 3, x))
    elif letter == '?':
      for _x in range(x + 1, x + 4):
        coord_letters.append((y, _x))
        coord_letters.append((y + 2, _x + 1))
      for _y in range(y, y + 2):
        coord_letters.append((_y, x))
        coord_letters.append((_y, x + 4))
      coord_letters.append((y + 4, x + 2))
    elif letter == '!':
      for _y in range(y, y + 3):
        coord_letters.append((_y, x + 2))
      coord_letters.append((y + 4, x + 2))
    elif letter == '.':
      coord_letters.append((y + 4, x + 2))
    elif letter == ' ':  # space operates as newline
      x = -5
      y += 6  # reset pointer
    x += 6  # increment for next word
  return coord_letters, coord_holes


def __mazify(grid, coord, isHole):  # recursive backtracker
  stack = []
  stack.append(grid.getCell(coord[0], coord[1]))
  while stack:
    cell = stack[-1]
    if isHole:
      grid.mask_alone(coord[0], coord[1])
    neighbors = [n for n in cell.getNeighbors() if not n.getLinks()]
    if neighbors:
      neighbor = sample(neighbors, 1)[0]
      cell.link(neighbor)
      stack.append(neighbor)
    else:
      stack.pop()
  return grid


def mask_word(phrase: str) -> Grid:  # inputs string and outputs maze
  words = phrase.split(' ')
  total_rows = 6 * len(words) + 1
  total_cols = 6 * len(max(words, key=len)) + 1
  grid = Grid(total_rows, total_cols)
  coord_mask, coord_holes = alphabet(phrase)
  for coord in coord_mask:
    grid.mask(coord[0], coord[1])
  for coord in coord_holes:
    __mazify(grid, coord, True)
  return str(__mazify(grid, grid.getRandom().coord, False))