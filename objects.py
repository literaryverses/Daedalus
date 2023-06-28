from random import randint, random, shuffle, choice
'''
NOTES:
-binary trees, sidewinder, recursive_backtracking, ellers, twist_and_turn, and kruskals are for orthogonal grids only
-do not use the following algos for masking
'''


class Cell:

  def __init__(self, row: int, column: int, level=0):
    self.coord = (row, column, level)
    self.neighbors = {}
    self.links = {}

  def link(self, cell):
    self.links[cell] = True
    cell.links[self] = True

  def unlink(self, cell):
    self.links.pop(cell, None)
    cell.links.pop(self, None)

  def getLinks(self):  # returns all linked neighbors
    return self.links.keys()

  def isLinked(self, cell):
    return self.links.get(cell)

  def isMasked(self):
    return self.isLinked(None)

  def getNeighbors(self, masking=True):  # returns all neighbors
    neighbors = [n for n in self.neighbors.values() if n is not None]
    if not masking:  # gets all existing neighbor cells
      return neighbors
    else:  # applies masking by retrieving neighbors that are unmasked
      return list(filter(lambda n: not n.isMasked(), neighbors))

  def getDirections(self):  # returns directions to linked neighbors
    directions = self.neighbors.keys()
    return list(
      filter(lambda d: True if self.neighbors.get(d) else False, directions))


class Grid:  # orthogonal maze (shape == 4) by default

  def __init__(self, rows: int, columns: int, levels=1, shape=4):
    self.rows = rows
    self.cols = columns
    self.lvls = levels
    self.grid = [[[0 for c in range(columns)] for r in range(rows)]
                 for l in range(levels)]
    self.borders = {
      'north': '---',
      'south': '---',
      'west': '|',
      'east': '|',
      'up': 'O',
      'vdoor': '   ',
      'hdoor': ' ',
      'down': '0',
      'through': '@'
    }
    self.__prepareGrid(shape)

  def __str__(self):
    is_print_horizontal = False if 10 * self.rows < self.cols else True
    maze = ''
    for row in self.each_row():
      row_layout = [''] * 3
      for cell in row:
        row_layout = self._drawCell(row_layout, cell)
      maze += '\n'.join(row_layout)
    if is_print_horizontal and self.lvls > 1:
      maze = maze.split('\n')
      length = len(max(maze, key=len))
      for i, maze_rows in enumerate(maze[:-1]):
        row_end = 2 * self.rows + 1
        if i > row_end - 1:
          maze[i % (row_end)] += maze_rows.ljust(length + 3)
        else:
          maze[i] = maze_rows.ljust(length + 3)
      return '\n'.join(maze[:row_end])
    return maze

  def __prepareGrid(self, shape):
    for row in range(self.rows):
      for col in range(self.cols):
        for lvl in range(self.lvls):
          self.grid[lvl][row][col] = Cell(row, col, lvl)
    for cell in self.each_cell(False):
      self.__configureCells(cell, shape)

  def __configureCells(self, cell, shape):
    row, col, lvl = cell.coord
    if shape == 3:
      if sum(cell.coord[:-1]) % 2:
        cell.neighbors['north'] = self.getCell(row - 1, col, lvl)
        cell.neighbors['southeast'] = self.getCell(row, col + 1, lvl)
        cell.neighbors['southwest'] = self.getCell(row, col - 1, lvl)
      else:
        cell.neighbors['south'] = self.getCell(row + 1, col, lvl)
        cell.neighbors['northeast'] = self.getCell(row, col + 1, lvl)
        cell.neighbors['northwest'] = self.getCell(row, col - 1, lvl)
    elif shape == 4:
      cell.neighbors['north'] = self.getCell(row - 1, col, lvl)
      cell.neighbors['south'] = self.getCell(row + 1, col, lvl)
      cell.neighbors['west'] = self.getCell(row, col - 1, lvl)
      cell.neighbors['east'] = self.getCell(row, col + 1, lvl)
    elif shape == 6:
      north_diagonal = (lambda r, c: r if c % 2 else r - 1)(row, col)
      south_diagonal = (lambda r, c: r + 1 if c % 2 else r)(row, col)
      cell.neighbors['north'] = self.getCell(row - 1, col, lvl)
      cell.neighbors['south'] = self.getCell(row + 1, col, lvl)
      cell.neighbors['northwest'] = self.getCell(north_diagonal, col - 1, lvl)
      cell.neighbors['southwest'] = self.getCell(south_diagonal, col - 1, lvl)
      cell.neighbors['northeast'] = self.getCell(north_diagonal, col + 1, lvl)
      cell.neighbors['southeast'] = self.getCell(south_diagonal, col + 1, lvl)
    if self.lvls > 1:
      cell.neighbors['up'] = self.getCell(row, col, lvl + 1)
      cell.neighbors['down'] = self.getCell(row, col, lvl - 1)

  def _drawCell(self, row_layout, cell):
    top, middle, bottom = row_layout[0], row_layout[1], row_layout[2]
    top += self._drawCorner(cell.coord[0], cell.coord[1], cell.coord[2])
    top += self._drawBorder(cell, 'north')  # draw top wall
    middle += f"{self._drawBorder(cell, 'west')} {self._drawBorder(cell, 'within')} "
    if cell.coord[0] == self.rows - 1:  # if last row
      bottom += self._drawCorner(cell.coord[0] + 1, cell.coord[1],
                                 cell.coord[2])
      bottom += self._drawBorder(cell, 'south')  # draw bottom wall
    if cell.coord[1] == self.cols - 1:  # if last column
      top += self._drawCorner(cell.coord[0], cell.coord[1] + 1, cell.coord[2])
      middle += self._drawBorder(cell, 'east')  # draw right wall
    if sum(cell.coord[:-1]) == self.cols + self.rows - 2:  # last cell
      bottom += f'{self._drawCorner(self.rows, self.cols, cell.coord[2])}\n'
    return [top, middle, bottom]

  def __drawWithin(self, cell: Cell) -> str:
    directions = ['up', 'down']
    for i, direction in enumerate(directions):
      if direction in cell.neighbors.keys() and\
          cell.isLinked(cell.neighbors[direction]) and\
              cell.neighbors[direction] != None:
        directions[i] = self.borders[direction]
      else:
        directions[i] = False
    if directions[0] and directions[1]: return self.borders['through']
    elif directions[0]: return self.borders['up']
    elif directions[1]: return self.borders['down']
    else: return

  def _drawBorder(self, cell: Cell, direction: str) -> str:
    if direction == 'within':
      if (within := self.__drawWithin(cell)):
        return within
    elif (direction in cell.neighbors.keys() and\
        not cell.isLinked(cell.neighbors[direction])):
      return self.borders[direction]
    if len(direction) == 5:  # north / south
      return self.borders['vdoor']
    else:  # horizontal / diagonal
      return self.borders['hdoor']

  def _drawCorner(self,
                  y: int,
                  x: int,
                  z=0) -> str:  # given two diagonal cells
    adjacents = [True] * 4
    if y == self.rows:
      adjacents[2] = adjacents[3] = False
    elif y - 1 < 0:
      adjacents[0] = adjacents[1] = False
    if x == self.cols:
      adjacents[0] = adjacents[3] = False
    elif x - 1 < 0:
      adjacents[1] = adjacents[2] = False

    for order, make_cell in enumerate(adjacents):
      long = (lambda o: 'WE'[o < 3 and o > 0])(order)
      lat = (lambda o: 'NS'[o < 2])(order)
      skews = {'N': 'north', 'S': 'south', 'W': 'west', 'E': 'east'}

      def upRight():
        return self.getCell(y - 1, x, z)

      def upLeft():
        return self.getCell(y - 1, x - 1, z)

      def downLeft():
        return self.getCell(y, x - 1, z)

      def downRight():
        return self.getCell(y, x, z)

      if make_cell:
        cell = [upRight, upLeft, downLeft, downRight][order]()
        if not cell.isLinked(cell.neighbors[skews[long]]) or\
        not cell.isLinked(cell.neighbors[skews[lat]]):
          return '+'
    return ' '

  # disconnects from graph and other masked cells
  def mask_alone(self, row: int, col: int, lvl=0):
    cell = self.getCell(row, col, lvl)
    cell.links[None] = True

  def getCell(self, row: int, col: int, lvl=0) -> Cell:
    if row < 0 or col < 0 or lvl < 0 or \
        row == self.rows or col == self.cols or lvl == self.lvls:
      return  # if out of bounds
    else:
      return self.grid[lvl][row][col]

  def getRandom(self) -> Cell:
    while (True):
      cell = self.grid[randint(0, self.lvls-1)][randint(0, self.rows-1)]\
          [randint(0, self.cols-1)]
      if not cell.isMasked():
        return cell

  def getSize(self, masking=True) -> int:
    if not masking:
      return self.lvls * self.rows * self.cols
    else:
      return len(set(self.each_cell()))

  def each_row(self):
    for lvl in range(self.lvls):
      for row in range(self.rows):
        yield self.grid[lvl][row]

  def each_cell(self, masking=True):
    for lvl in range(self.lvls):
      for row in range(self.rows):
        for col in range(self.cols):
          cell = self.grid[lvl][row][col]
          if not masking:
            yield cell
          elif not cell.isMasked():
            yield cell

  def mask(self,
           row: int,
           col: int,
           lvl=0):  # disconnects cell from rest of grid
    if row < 0 or row >= self.rows:
      raise Exception(f'Row {row} not within parameters')
    if col < 0 or col >= self.cols:
      raise Exception(f'Column {col} not within parameters')
    if lvl < 0 or lvl >= self.lvls:
      raise Exception(f'Level {lvl} not within parameters')
    cell = self.getCell(row, col, lvl)
    cell.links[None] = True
    for neighbor in cell.getNeighbors(False):
      if neighbor.isMasked() and neighbor != cell.neighbors.get('up')\
          and neighbor != cell.neighbors.get('down'): # prevent z-axis linking between masked cells
        cell.link(neighbor)

  # link up dead ends
  def braid(self, p=1):  # p == proportion of dead ends allowed
    notLinked = (lambda n: True if n not in cell.getLinks() else False)
    deadEnds = (lambda c: True if len(c.getLinks()) == 1 else False)
    total_dead_ends = list(filter(deadEnds, self.each_cell()))
    shuffle(total_dead_ends)
    for cell in total_dead_ends:
      if len(cell.getLinks()) != 1 or random() > p:
        continue
      # get unlinked neighbors
      neighbors = list(filter(notLinked, cell.getNeighbors()))
      # best option is joining two dead ends
      best = list(filter(deadEnds, neighbors))
      if not best:
        best = neighbors
      neighbor = choice(best)
      cell.link(neighbor)

  def getOpposite(self, cell, neighbor):  # returns cell opposite to neighbor
    if cell not in neighbor.getLinks():
      return None
    keyList = list(neighbor.neighbors.keys())
    valList = list(neighbor.neighbors.values())
    position = valList.index(cell)
    direction = keyList[position]
    return cell.neighbors.get(direction)


class TriGrid(Grid):  # delta grid (shape = 3)

  def __init__(self, rows: int, columns: int, levels=1):
    super().__init__(rows, columns, levels, shape=3)
    self.borders = {
      'north': '---',
      'south': '---',
      'northwest': '/',
      'northeast': '\\',
      'southwest': '\\',
      'southeast': '/',
      'vdoor': '   ',
      'hdoor': ' ',
      'up': 'O',
      'down': '0',
      'through': '@'
    }

  def _drawCell(self, row_layout, cell):
    top, middle, bottom = row_layout[0], row_layout[1], row_layout[2]
    if sum(cell.coord[:-1]) % 2:
      if cell.coord[1] == 0:  # 1st column
        top += self._drawCorner(cell.coord[0], cell.coord[1] - 1,
                                cell.coord[2])
        middle += f" {self._drawBorder(cell, 'southwest')}"
      top += self._drawBorder(cell, 'north')
      top += self._drawCorner(cell.coord[0], cell.coord[1] + 1, cell.coord[2])
      middle += f"{self._drawBorder(cell,'within')}{self._drawBorder(cell, 'southeast')}"
      if cell.coord[1] == 0 and cell.coord[
          0] == self.rows - 1:  # last cell in 1st column
        bottom += '  '  # indentation
      if sum(cell.coord[:-1]) == self.cols + self.rows - 2:  # last cell
        bottom += f'{self._drawCorner(cell.coord[0]+1, cell.coord[1], cell.coord[2])}\n'
    else:  # if is pointy
      if cell.coord[1] == 0:  # 1st column
        top += f'  {self._drawCorner(cell.coord[0], cell.coord[1], cell.coord[2])}'
        middle += f" {self._drawBorder(cell, 'northwest')}"
      if cell.coord[0] == self.rows - 1:  # last row
        bottom += self._drawCorner(cell.coord[0] + 1, cell.coord[1] - 1,
                                   cell.coord[2])
        bottom += self._drawBorder(cell, 'south')
      middle += f"{self._drawBorder(cell,'within')}{self._drawBorder(cell, 'northeast')}"
      if sum(cell.coord[:-1]) == self.cols + self.rows - 2:  # last cell
        bottom += f'{self._drawCorner(cell.coord[0]+1, cell.coord[1]+1, cell.coord[2])}\n'
    return [top, middle, bottom]

  def _drawCorner(self,
                  y: int,
                  x: int,
                  z=0) -> str:  # given two diagonal cells
    adjacents = [True] * 6
    if y == self.rows:
      adjacents[0] = adjacents[1] = adjacents[5] = False
    elif y - 1 < 0:
      adjacents[2] = adjacents[3] = adjacents[4] = False
    if x == self.cols or x == -1:
      adjacents[0] = adjacents[3] = False
    if x + 1 >= self.cols:
      adjacents[1] = adjacents[2] = False
    elif x <= 0:
      adjacents[4] = adjacents[5] = False

    for order, make_cell in enumerate(adjacents):
      if make_cell and order == 0:
        downMid = self.getCell(y, x, z)
        if not downMid.isLinked(downMid.neighbors['northwest']) or \
            not downMid.isLinked(downMid.neighbors['northeast']):
          return 'x'
      elif make_cell and order == 1:
        downRight = self.getCell(y, x + 1, z)
        if not downRight.isLinked(downRight.neighbors['north']) or \
            not downRight.isLinked(downRight.neighbors['southwest']):
          return 'x'
      elif make_cell and order == 2:
        upRight = self.getCell(y - 1, x + 1, z)
        if not upRight.isLinked(upRight.neighbors['south']) or \
            not upRight.isLinked(upRight.neighbors['northwest']):
          return 'x'
      elif make_cell and order == 3:
        upMid = self.getCell(y - 1, x, z)
        if not upMid.isLinked(upMid.neighbors['southeast']) or \
            not upMid.isLinked(upMid.neighbors['southwest']):
          return 'x'
      elif make_cell and order == 4:
        upLeft = self.getCell(y - 1, x - 1, z)
        if not upLeft.isLinked(upLeft.neighbors['northeast']) or \
            not upLeft.isLinked(upLeft.neighbors['south']):
          return 'x'
      elif make_cell and order == 5:
        downLeft = self.getCell(y, x - 1, z)
        if not downLeft.isLinked(downLeft.neighbors['north']) or \
            not downLeft.isLinked(downLeft.neighbors['southeast']):
          return 'x'
    return ' '


class HexGrid(Grid):  # sigma maze (shape = 6)

  def __init__(self, rows: int, columns: int, levels=1):
    super().__init__(rows, columns, levels, shape=6)

  def __str__(self):  # creates sigma maze from delta maze
    template = TriGrid(2 * self.rows + 1, self.cols * 3, self.lvls)
    self.__hexify(template)
    for row in self.each_row():
      for cell in row:
        template = self.__reformat(cell, template)
    return str(template)

  # link up triangular grid to match the links of hexagonal maze
  def __reformat(self, hex_cell: Cell, triGrid: TriGrid) -> TriGrid:
    for direction in hex_cell.neighbors.keys():
      neighbor = hex_cell.neighbors[direction]
      if neighbor and hex_cell.isLinked(neighbor):
        triangle = self.__getTriangle(hex_cell, direction, triGrid)
        triangle.link(triangle.neighbors[direction])
      elif hex_cell.isLinked(None):  # hex cell links to none, hence is masked
        triangle = self.__getTriangle(hex_cell, 'up',
                                      triGrid)  # get corresp triangle
        self.__maskUp(triGrid, False, triangle.coord[0], triangle.coord[1],
                      triangle.coord[2])
    return triGrid

  # returns corresponding triangular cell according to direction of hexagonal cell
  def __getTriangle(self, hex_cell: Cell, direction: str,
                    triGrid: TriGrid) -> Cell:
    row, col, lvl = hex_cell.coord

    def y_adjust(col, direction):
      adjust = 0
      if direction[0] == 's': adjust += 1
      if col % 2: adjust += 1
      return adjust

    def x_adjust(direction):
      adjust = 0
      if len(direction) == 5: adjust += 1
      if direction[-4:] == 'east': adjust += 2
      return adjust

    return triGrid.getCell(2 * row + y_adjust(col, direction),
                           3 * col + x_adjust(direction), lvl)

  # create hexagonal grid from triangular grid
  def __hexify(self, triGrid: TriGrid):
    for z in range(self.lvls):
      y = x = 0
      for _ in range(self.rows * self.cols):  # make sigma maze
        if x == 3 * self.cols:
          x = 0
          y += 2  # reset coord
        if x % 2:
          self.__linkUp(triGrid, y + 1, x, z)
          if y == 0:
            self.__maskUp(triGrid, True, y, x, z)
        else:
          self.__linkUp(triGrid, y, x, z)
          if y == 2 * self.rows - 2:
            self.__maskUp(triGrid, True, y, x, z)
        x += 3

  # link triangular cells into hexagonal cell
  def __linkUp(self, triGrid: TriGrid, row: int, col: int, lvl=0):
    current = triGrid.getCell(row, col, lvl)
    for _x in range(1, 3):
      temp, current = current, triGrid.getCell(row, col + _x, lvl)
      temp.link(current)
    for _x in range(2, -1, -1):
      temp, current = current, triGrid.getCell(row + 1, col + _x, lvl)
      temp.link(current)
    current.link(triGrid.getCell(row, col, lvl))

  # imposes masking from sigma maze to delta maze
  def __maskUp(self,
               triGrid: TriGrid,
               isEdge: bool,
               row: int,
               col: int,
               lvl=0):
    y_edge = (lambda r: 2 if r == triGrid.rows - 3 else 0)(row)
    if isEdge:  # if formating edge
      for x in range(3):
        triGrid.mask(row + y_edge, col + x, lvl)
    else:
      for x in range(3):
        triGrid.mask(row, col + x, lvl)  # top row of hexagon
        triGrid.mask(row + 1, col + x, lvl)  # bottom row of hexagon


from maze_generation import *

grid = Grid(5, 5)
grid.mask(0, 0)
grid.mask(4, 4)
aldousBroder(grid)
grid.braid()
print(grid)
