# Performs maze generation algorithms

from random import randint, choice, shuffle, random
'''
Aldous-Broder: breaks down walls between unvisited cells until all the cells
in the grid are visited
'''


def aldousBroder(grid):
  cell = grid.getRandom()
  unvisited = grid.getSize() - 1
  while unvisited > 0:
    neighbor = choice(cell.getNeighbors())
    if not neighbor.getLinks():  # checks if neighbor has no links
      cell.link(neighbor)
      unvisited -= 1
    cell = neighbor
  return grid


'''
Growing Tree: implements both simplified and true Prim's algorithms
proportionally based on input from 0 (random selection, Prim's) to 1 (last
selection, recursive backtracking). The Default is set to 0.5, meaning the
two options are equiprobable.
'''


def growingTree(grid, slider=0.5):
  isAvailable = lambda n: True if not n.getLinks() else False
  active = []
  active.append(grid.getRandom())
  while active:
    randomly = (lambda l: choice(l))(active)  # Prim's (simplified)
    last = (lambda l: l[-1])(active)  # Recursive backtracker
    cell = [randomly, last][random() < slider]
    neighbors = list(filter(isAvailable, cell.getNeighbors()))
    if neighbors:
      neighbor = choice(neighbors)
      cell.link(neighbor)
      active.append(neighbor)
    else:
      active.remove(cell)
  return grid


'''
Hunt and Kill: a random-walk based algorithm similar to Aldous-Broder except 
it only allows steps into unvisited cells only
'''


def hunt_and_kill(grid):
  current = grid.getRandom()
  while current:
    neighbors = current.getNeighbors()
    unvisited_neighbors = [n for n in neighbors if not n.getLinks()]
    if unvisited_neighbors:
      neighbor = choice(unvisited_neighbors)
      current.link(neighbor)
      current = neighbor
    else:
      current = None  # to break out while loop if all visited
      for cell in grid.each_cell():
        neighbors = cell.getNeighbors()
        visited_neighbors = [n for n in neighbors if n.getLinks()]
        # if visited neighbors exist and cell has no links
        if visited_neighbors and not cell.getLinks():
          current = cell
          neighbor = choice(visited_neighbors)
          current.link(neighbor)
          break
  return grid


'''
Recursive backtracker: DFS that recursively backtracks from dead ends
'''


def recursive_backtracker(grid):
  stack = []  # stack to recurse through
  stack.append(grid.getRandom())
  while stack:
    cell = stack[-1]
    neighbors = [n for n in cell.getNeighbors() if not n.getLinks()]
    if neighbors:
      neighbor = choice(neighbors)
      cell.link(neighbor)
      stack.append(neighbor)
    else:
      stack.pop()
  return grid


'''
Recursive division: treats the maze as a fractal by adding walls recursively
'''


def recursive_division(grid):

  def divide(row, col, lvl, length, width):
    if length <= 1 or width <= 1:
      return
    if length > width:
      divide_y(row, col, lvl, length, width)
    else:
      divide_x(row, col, lvl, length, width)\

  def divide_y(row, col, lvl, length, width):  # divide horizontally
    divide_south_of = randint(0, length - 2)
    passage_at = randint(0, width - 1)
    for x in range(width):
      if x == passage_at:
        continue
      cell = grid.getCell(row + divide_south_of, col + x, lvl)
      cell.unlink(cell.neighbors['south'])
    divide(row, col, lvl, divide_south_of + 1, width)
    divide(row + divide_south_of + 1, col, lvl, length - divide_south_of - 1,
           width)

  def divide_x(row, col, lvl, length, width):  # divide vertically
    divide_east_of = randint(0, width - 2)
    passage_at = randint(0, length - 1)
    for y in range(length):
      if y == passage_at:
        continue
      cell = grid.getCell(row + y, col + divide_east_of, lvl)
      cell.unlink(cell.neighbors['east'])
    divide(row, col, lvl, length, divide_east_of + 1)
    divide(row, col + divide_east_of + 1, lvl, length,
           width - divide_east_of - 1)

  for cell in grid.each_cell():  # unlinking every cell
    for neighbor in cell.getNeighbors():
      if neighbor != cell.neighbors.get('up') and\
          neighbor != cell.neighbors.get('down'):
        cell.link(neighbor)
  for lvl in range(grid.lvls):  # connects mazes on z-axis
    divide(0, 0, lvl, grid.rows, grid.cols)
    if lvl != grid.lvls - 1 and grid.lvls > 1:
      cell = grid.getCell(randint(0, grid.rows - 1), randint(0, grid.cols - 1),
                          lvl)
      cell.link(cell.neighbors['up'])
  return grid


'''
Wilson's: draws multiple paths from unvisited cells to a visited one until
there are no more unvisited cells.
'''


def wilsons(grid):
  unvisited = list(grid.each_cell())
  shuffle(unvisited)
  unvisited.pop()  # set first goal cell
  while unvisited:
    path = unvisited[0:1]
    cell = path[0]
    while cell in unvisited:  # create path
      cell = choice(cell.getNeighbors())
      if cell in path:  # remove loops
        path = path[:path.index(cell) + 1]
      else:
        path.append(cell)
    for index, cell in enumerate(path):
      if index < len(path) - 1:
        cell.link(path[index + 1])  # link the cells in path
        unvisited.remove(cell)  # set path as visited
    path.clear()  # clear path
  return grid
