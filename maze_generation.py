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
Binary Tree: destroys either a longitudinal or latitudinal wall in each cell,
using an equiprobable random selection
'''


def binaryTree(grid, skew=''):
  # randomized skew if input skew is unspecified or incorrect
  skews = {  # preferred directions to move for orthogonal maze
    'NW': ('north', 'west'),
    'NE': ('north', 'east'),
    'SW': ('south', 'west'),
    'SE': ('south', 'east')
  }
  if (skew := skew.upper()) not in skews:
    skew = choice(list(skews.keys()))
  for cell in grid.each_cell():
    neighbors = []
    neighbors.append(cell.neighbors.get(skews.get(skew)[0]))
    neighbors.append(cell.neighbors.get(skews.get(skew)[1]))
    neighbors = [n for n in neighbors if n is not None]
    if len(neighbors) == 2:  # select neighbor to link to
      index = randint(0, 1)
    elif len(neighbors) == 1:
      index = 0
    else:  # len(neighbors) == 0
      continue
    neighbor = neighbors[index]
    cell.link(neighbor)
  for lvl in range(grid.lvls):  # connects mazes on z-axis
    if lvl != grid.lvls - 1 and grid.lvls > 1:
      cell = grid.getCell(randint(0, grid.rows - 1), randint(0, grid.cols - 1),
                          lvl)
      cell.link(cell.neighbors['up'])
  return grid


'''
Eller's: links adjacent neighing cells for each set assigned per row. A
combination of sidewinder (descending per row) and Kruskal's (assigning sets)
'''


def ellers(grid):
  set_for_cell = {}  # maps cells to corresponding set identifiers
  cells_in_set = {}  # maps set identifiers to cells belonging to those sets
  next_set = 0  # starting set

  def record(cell):  # records a given set for the given cell
    nonlocal next_set
    set_for_cell[cell.coord[1]] = next_set
    if not cells_in_set.get(next_set):
      cells_in_set[next_set] = set()
    cells_in_set[next_set].add(cell)

  def set_for(cell):  # checks to see if cell belongs to a set and returns set
    if not set_for_cell.get(cell.coord[1]):
      nonlocal next_set
      record(cell)
      next_set += 1
    return set_for_cell[cell.coord[1]]

  def merge(winner, loser):  # moves all cells from loser set to winner set
    for cell in cells_in_set[loser]:
      set_for_cell[cell.coord[1]] = winner
    cells_in_set[winner] = cells_in_set[winner].union(cells_in_set[loser])
    cells_in_set.pop(loser)

  for r, row in enumerate(grid.each_row()):
    for cell in row:
      if not cell.neighbors['west']:
        continue  # skip most western cell in row
      prior_set = set_for(cell.neighbors['west'])
      cell_set = set_for(cell)  # assign cell to set
      should_link = cell_set != prior_set and \
          (cell.coord[0] == grid.rows-1 or random() < 1/3)
      if should_link:  # merge neighbors in row
        cell.link(cell.neighbors['west'])
        merge(set_for_cell[cell.coord[1] - 1], set_for_cell[cell.coord[1]])
    set_for_cell.clear()
    if (r + 1) % grid.rows:  # merge neighbors to next row
      for i, cells in cells_in_set.items():
        cell = cells.pop()
        cell.link(cell.neighbors['south'])
        cells_in_set[i] = {cell.neighbors['south']}
        set_for_cell[cell.coord[1]] = i
    else:
      cells_in_set.clear()

  for lvl in range(grid.lvls):  # connects mazes on z-axis
    if lvl != grid.lvls - 1 and grid.lvls > 1:
      cell = grid.getCell(randint(0, grid.rows - 1), randint(0, grid.cols - 1),
                          lvl)
      cell.link(cell.neighbors['up'])
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
Kruskal's: randomly (since no path cost assigned) merges a pair neighboring
cells as long as they are not already linked
'''


def kruskals(grid):
  # randomized skew if input skew is unspecified or incorrect
  neighbors = []  # track pairs of neighboring cells
  set_for_cell = {}  # maps cells to corresponding set identifiers
  cells_in_set = {}  # maps set identifiers to cells belonging to those sets
  can_merge = lambda l, r: set_for_cell[l] != set_for_cell[r]

  def merge(left, right):
    left.link(right)
    winner = set_for_cell[left]
    loser = set_for_cell[right]
    losers = cells_in_set[loser]
    for cell in losers:
      cells_in_set[winner].add(cell)
      set_for_cell[cell] = winner
    cells_in_set.pop(loser)

  for i, cell in enumerate(grid.each_cell()):
    set_for_cell[cell] = i  # assign each cell to own set
    cells_in_set[i] = {cell}
    if cell.neighbors.get('south'):
      neighbors.append([cell, cell.neighbors['south']])
    if cell.neighbors.get('east'):
      neighbors.append([cell, cell.neighbors['east']])

  shuffle(neighbors)
  while neighbors:
    left, right = neighbors.pop()  # chooses pair of neighboring cells
    if can_merge(left, right):  # if belong to different sets, merge
      merge(left, right)
  return grid


'''
Prim and Kill: Repeatedly starts a random walk from a visited region until
all unvisited cells are visited
'''


def prim_and_kill(grid):

  def random_walk(unvisited, visited, cell):
    isUnvisited = lambda n: True if n in unvisited else False
    visited.add(cell)
    unvisited.discard(cell)
    while (neighbors := list(filter(isUnvisited, cell.getNeighbors()))):
      next = choice(neighbors)
      cell.link(next)
      cell = next
      visited.add(cell)
      unvisited.remove(cell)
    return unvisited, visited

  unvisited = set(grid.each_cell())
  visited = set()
  cell = grid.getRandom()
  while unvisited:
    unvisited, visited = random_walk(unvisited, visited, cell)
    cell = choice(list(visited))
    for neighbor in cell.getNeighbors():
      if neighbor in unvisited:
        break
  return grid


'''
Prim's (simplified): Prim's algorithm if every path had equal weight, 
in which a random neighboring cell is added to the path one-by-one
'''


def prims_sim(grid):
  isAvailable = lambda n: True if not n.getLinks() else False
  active = []
  active.append(grid.getRandom())
  while active:
    cell = choice(active)
    neighbors = list(filter(isAvailable, cell.getNeighbors()))
    if neighbors:
      neighbor = choice(neighbors)
      cell.link(neighbor)
      active.append(neighbor)
    else:
      active.remove(cell)
  return grid


'''
Prim's (true): randomly assigns weights to cells and adds neighboring
cells according to those costs
'''


def prims_true(grid):
  isAvailable = lambda n: True if not n.getLinks() else False
  active = []
  active.append(grid.getRandom())
  costs = {}
  for cell in grid.each_cell():
    costs[cell] = randint(0, 100)
  while active:
    cell = min(active, key=costs.get)
    neighbors = list(filter(isAvailable, cell.getNeighbors()))
    if neighbors:
      neighbor = min(neighbors, key=costs.get)
      cell.link(neighbor)
      active.append(neighbor)
    else:
      active.remove(cell)
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
Sidewinder: decides to destroy the right wall or not for every cell based
on equiprobable random choice. If the wall is not destroyed, then any cell
preceding the current one within that row will destroy its northern wall.
'''


def sidewinder(grid):  # sidewinder algo
  for row in grid.each_row():
    run = []
    for cell in row:
      run.append(cell)
      at_eastern_boundary = True  # end of row
      if cell.neighbors.get('east'):
        at_eastern_boundary = False
      at_northern_boundary = True  # top of grid
      if cell.neighbors.get('north'):
        at_northern_boundary = False
      # decide to walk east or north
      should_close_out = at_eastern_boundary or \
          (not at_northern_boundary and randint(0, 1) == 0)
      if should_close_out:  # create dead end
        # select any preceding cell in row of current cell
        member = run[randint(0, len(run) - 1)]
        northerner = member.neighbors.get('north')
        if northerner:
          member.link(northerner)
        run.clear()
      else:
        easterner = cell.neighbors.get('east')
        cell.link(easterner)
  for lvl in range(grid.lvls):  # connects mazes on z-axis
    if lvl != grid.lvls - 1 and grid.lvls > 1:
      cell = grid.getCell(randint(0, grid.rows - 1), randint(0, grid.cols - 1),
                          lvl)
      cell.link(cell.neighbors['up'])
  return grid


'''
Twist and Merge: performs multiple biaised random walks to create paths where
straight walks are forbidden. The produced regions are then merged into a 
single connected component. This approach favorizes the turns and increases 
the number of non-significant walks.
'''


def twist_and_merge(grid):
  isUnvisited = lambda n: True if n in unvisited else False

  def twisty(neighbors, cell,
             previous):  # returns neighbors that are not aligned
    if (aligned := grid.getOpposite(cell, previous)):
      neighbors = neighbors.difference({aligned})
    return neighbors

  def biased_random_walk(unvisited, cell):  # create regions via random walk
    previous = cell
    region = {cell}
    while (neighbors := twisty(set(filter(isUnvisited, cell.getNeighbors())),
                               cell, previous)):
      next = neighbors.pop()
      cell.link(next)
      region.add(next)
      unvisited.remove(next)
      previous = cell
      cell = next
    return region

  regions = []
  unvisited = set(grid.each_cell())

  while unvisited:  # twist mode
    cell = unvisited.pop()
    regions.append(biased_random_walk(unvisited, cell))

  find_index = lambda n, i, l: i if n in l[i] else 0
  while len(regions) > 1:  # merge mode
    cell = regions[0].pop()
    for neighbor in cell.getNeighbors():
      if len(regions) == 1:
        break
      for i in range(1, len(regions)):
        i = find_index(neighbor, i, regions)
        if i:
          cell.link(neighbor)  # link cell to neighbor
          # absorb neighbor's region
          regions[0] = regions[0].union(regions.pop(i))
          break
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
