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
