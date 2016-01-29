class Cell:
    def __init__(self, r, c, colour, group_id):
        self.r = r
        self.c = c
        self.colour = colour
        self.group_id = group_id

    def __repr__(self):
        return "({},{})-{}".format(self.r,self.c, self.colour)

class Group:
    def __init__(self, group_id):
        self.group_id = group_id
        self.cells = []

    def add(self, c):
        self.cells.append(c)


class Grid:
    HEIGHT = 9
    WIDTH = 6
    NB_COLORS = 6

    def __init__(self, array=None):
        if array:
            self.array = array
        else:
            self.array = Grid.rand_grid()
        for r in range(Grid.HEIGHT):
            for c in range(Grid.WIDTH):
                self.array[r][c] = Cell(r, c, self.array[r][c], -1)
        self.update_groups()

    def print_grid(self):
        print("-----------")
        for l in self.array:
            print(l)

    @staticmethod
    def test_ready(g):
        '''g must be a 2-D list, containing numbers
        Returns true if and only if any two adjacent cells have different colour
        ''' 
        for i in range(Grid.HEIGHT):
            for j in range(Grid.WIDTH):
                for vi, vj in [(i+1,j), (i,j+1)]:
                    if (0 <= vi and vi < Grid.HEIGHT and 0 <= vj 
                            and vj < Grid.WIDTH and g[vi][vj] == g[i][j]):
                        return False
        return True

    @staticmethod
    def rand_grid():
        '''Returns a 2-D self.HEIGHT*self.WIDTH list containing integers in [0, NB_COLORS[
        such as any two adjacent cells have different colours
        '''
        from random import shuffle
        g = [[j for j in range(Grid.WIDTH)] for i in range(Grid.HEIGHT)]
        while not Grid.test_ready(g):
            for i in range(Grid.HEIGHT):
                shuffle(g[i])
            #Grid.print_grid(g)
            if Grid.test_ready(g):
                return g
            for j in range(Grid.WIDTH):
                c = [g[i][j] for i in range(Grid.HEIGHT)]
                shuffle(c)
                for i in range(Grid.HEIGHT):
                    g[i][j] = c[i]
            #Grid.print_grid(g)
        return g

    # @staticmethod
    # def neighbours_of_colour(array, r, c, colour):
    #     '''Returns a list of neighbours (r2, c2) of cell (r,c) such as
    #     array[r2][c2] == colour
    #     '''  
    #     res = []
    #     if r-1 >= 0 and array[r-1][c] == colour: 
    #         res.append((r-1, c))
    #     if r+1 < len(array) and array[r+1][c] == colour: 
    #         res.append((r+1, c))
    #     if c-1 >= 0 and array[r][c-1] == colour: 
    #         res.append((r,c-1))
    #     if c+1 < len(array[0]) and array[r][c+1] == colour: 
    #         res.append((r,c+1))
    #     return res

    def update_groups(self):
        '''Analyses the grid to compute the groups of cells
        Note that cells are stored in groups in a certain order thanks to 
        a custom flooding order : from top to bottom and left to right
        '''
        self.groups = []
        copy = [[self.array[r][c].colour for c in range(Grid.WIDTH)] 
                for r in range(Grid.HEIGHT)]
        flood_val = -1
        group_id = 0
        for row in range(Grid.HEIGHT):
            for col in range(Grid.WIDTH):
                colour = copy[row][col]
                if colour >= 0:
                    # Computes the group_id-th group of cells, by
                    # flooding cells of colour 'colour' starting from 
                    # (row,col) with value flood_val
                    g = Group(group_id)
                    queue = [(row, col)]
                    while len(queue) > 0:
                        r, c = queue.pop()
                        g.add(self.array[r][c])
                        self.array[r][c].group_id = group_id
                        copy[r][c] = flood_val
                        if r+1 < Grid.HEIGHT and copy[r+1][c] == colour: 
                            queue.insert(0, (r+1, c))
                        if c+1 < Grid.WIDTH and copy[r][c+1] == colour: 
                            queue.append((r,c+1))

                    self.groups.append(g)
                    flood_val -= 1
                    group_id += 1

    def group_cells(self, r, c):
        '''Returns a list of cells in the group containing the cell
        self.array[r][c]
        '''
        return self.groups[self.array[r][c].group_id].cells
        
    @staticmethod
    def deltas(dir):
        dr, dc = 0, 0
        if dir == 'N': dr = -1
        if dir == 'S': dr = 1
        if dir == 'E': dc = 1
        if dir == 'W': dc = -1
        return dr, dc

    def shift(self, r, c, dir, dist):
        '''dir in {'N', 'S', 'E', 'W'}
        Shifts cell self.array[r][c] of dist cells, in direction dir
        '''
        dr, dc = Grid.deltas(dir)

        mem = self.array[r][c]
        r2, c2 = r, c
        while r2 != (r + dist*dr) or c2 != (c + dist*dc):
            self.array[r2][c2] = self.array[r2+dr][c2+dc]
            self.array[r2][c2].r = r2
            self.array[r2][c2].c = c2
            r2 += dr
            c2 += dc
        self.array[r2][c2] = mem
        self.array[r2][c2].r = r2
        self.array[r2][c2].c = c2 

    def raw_move(self, r, c, dir, dist):
        '''dir in {'N', 'S', 'E', 'W'}
        Shifts the whole group of the cell self.array[r][c] of dist cells,
        in direction dir
        '''
        # cells are stored from left to right, and up to bottom in groups
        # depending on the dir, the list must be browsed in a different way
        # for instance, if the move is toward South, the cells of each 
        # column must be considered from south to north, so the list must 
        # be browsed in reverse
        if dir in ['N', 'W']:
            cells = self.group_cells(r, c)
        else:
            cells = reversed(self.group_cells(r, c)) 


        for cell in cells:
            # Make sure the block won't get out the grid
            assert dir != 'N' or cell.r - dist < self.HEIGHT
            assert dir != 'S' or cell.r + dist >= 0
            assert dir != 'E' or cell.c + dc*dist < self.WIDTH
            assert dir != 'W' or cell.c - dc*dist >= 0
            self.shift(cell.r, cell.c, dir, dist)

if __name__ == '__main__':

    print("Random grid :")
    g = Grid([[3, 1, 4, 0, 2, 2],
              [1, 0, 2, 0, 2, 0],
              [5, 4, 3, 3, 5, 4],
              [3, 1, 3, 4, 2, 0],
              [5, 5, 3, 4, 2, 3],
              [4, 5, 5, 0, 1, 4],
              [2, 5, 4, 5, 5, 1],
              [1, 1, 2, 0, 0, 1],
              [3, 2, 1, 3, 0, 4]])
    g.print_grid()

    # print("Groups :")
    # for grp in g.groups:
    #     print("grp id {} : {}", grp.group_id, grp.cells)

    print("After moving (2,3) of 3 cells in direction South :")
    g.raw_move(2, 3, 'S', 3)
    g.print_grid()



