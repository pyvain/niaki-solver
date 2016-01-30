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

class Move:
    NORTH = 'N';
    EAST = 'E';
    SOUTH = 'S';
    WEST = 'W';

    def __init__(self, r, c, dir):
        '''(r,c) is the origin of the swipe
        dir is its direction (in {NORTH, SOUTH, EAST, WEST})
        '''
        self.r = r
        self.c = c
        self.dir = dir

class Grid:
    HEIGHT = 9
    WIDTH = 6
    NB_COLORS = 6

    def __init__(self, array=None):
        if array:
            self.array = array
        else:
            self.array = Grid.__rand_grid()
        for r in range(Grid.HEIGHT):
            for c in range(Grid.WIDTH):
                self.array[r][c] = Cell(r, c, self.array[r][c], -1)
        self.__update_groups()

    def print_grid(self):
        print("-----------")
        for l in self.array:
            print(l)

    def group_cells(self, r, c):
        '''Returns a list of cells in the group containing the cell
        self.array[r][c]
        '''
        return self.groups[self.array[r][c].group_id].cells

    @staticmethod
    def __has_no_block(g):
        '''g must be a 2-D list, containing numbers
        Returns true if and only if any two adjacent cells have different colour
        ''' 
        for r in range(Grid.HEIGHT):
            for c in range(Grid.WIDTH):
                for vr, vc in [(r+1,c), (r,c+1)]:
                    if (0 <= vr and vr < Grid.HEIGHT and 0 <= vc 
                            and vc < Grid.WIDTH and g[vr][vc] == g[r][c]):
                        return False
        return True

    @staticmethod
    def __rand_grid():
        '''Returns a 2-D self.HEIGHT*self.WIDTH list containing integers in [0, NB_COLORS[
        such as any two adjacent cells have different colours
        '''
        from random import shuffle
        g = [[c for c in range(Grid.WIDTH)] for r in range(Grid.HEIGHT)]
        while not Grid.__has_no_block(g):
            for r in range(Grid.HEIGHT):
                shuffle(g[r])
            #Grid.print_grid(g)
            if Grid.__has_no_block(g):
                return g
            for c in range(Grid.WIDTH):
                col = [g[r][c] for r in range(Grid.HEIGHT)]
                shuffle(col)
                for r in range(Grid.HEIGHT):
                    g[r][c] = c[r]
            #Grid.print_grid(g)
        return g


    def __update_groups(self):
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

        
    @staticmethod
    def __deltas(dir):
        dr, dc = 0, 0
        if dir == 'N': dr = -1
        if dir == 'S': dr = 1
        if dir == 'E': dc = 1
        if dir == 'W': dc = -1
        return dr, dc

    def __set_cell(self, r, c, cell):
        '''Replaces self.array[r][c] by cell and
        Returns a tuple t such as self.__set_cell(*t) reverses this action.'''
        prev = self.array[r][c]
        self.array[r][c] = cell
        self.array[r][c].r = r
        self.array[r][c].c = c
        return (r, c, prev)

    def __set_cells(self, l):
        '''l must be a list of tuples (r, c, cell)
        Calls __set_cell() on the elements of each tuple, from first 
        to last, and returns a list l2 such as __set_cell(l2) reverses
        this action.
        '''
        rev = []
        for r, c, cell in l:
            rev.add(0, self.__set_cell(r, c, cell))

    def __cell_shift(self, r, c, dir, d):
        '''Computes the operations needed to shift cell self.array[r][c]
        of given distance d, in given direction dir
        Returns them in a list l such as __set_cells(l) performs the shift
        '''
        dr, dc = Grid.__deltas(dir)
        mem = self.array[r][c]
        res = []        
        for i in range(dist) :
            cell = self.array[r+(i+1)*dr][c+(i+1)*dc]
            res.append((r+i*dr, c+i*dc, cell))
        res.append((r+dist*dr, r+dist*dc, mem))
        return rev


    def __block_shift(self, r, c, dir, d):
        '''Computes the operations needed to shift cell self.array[r][c]
        of given distance d, in given direction dir, along with its block
        Returns them in a list l such as __set_cells(l) performs the shift

        Note that, shifting a block can be done by shifting its cells one 
        by one, in a good order.
        For example, if the direction of the shift is SOUTH, a cell of the 
        block can be shifted only if cells of the same line that were south
        of it have already been shifted.

        And because cells of a group are stored up to bottom, left to right
        This can be done by browsing the list in one way or the other
        '''
        res = []
        cells = self.group_cells(r, c)
        if dir in ['S', 'E']:
            cells = reversed(cells)

        for cell in cells:
            # Make sure the block won't get out the grid
            assert dir != 'N' or cell.r - d < self.HEIGHT
            assert dir != 'S' or cell.r + d >= 0
            assert dir != 'E' or cell.c + dc*d < self.WIDTH
            assert dir != 'W' or cell.c - dc*d >= 0
            res.extend(self.__cell_shift(cell.r, cell.c, dir, d))
        return res

    def __size_of_block_formed(self, r, c, dir, d):
        '''Returns the size of the block that would be formed if 
        self.__block_shift(r, c, dir, d) was performed

        Note that if it is equal to len(self.group_cells(r, c)), then 
        the move is illegal, as it doesn't extend the block containing 
        self.array[r][c]
        '''
        colour = self.array[r][c].colour
        res = len(self.group_cells(r, c))
        groups_considered = [self.array[r][c].group_id]
        
        dr, dc = Grid.__deltas(dir)
        r += dist * dr
        c += dist * dc
        for vr, vc in [(r+1, c), (r, c+1), (r-1, c), (r, c-1)]:
            cell = self.array[vr][vc]
            if (cell.colour == colour and 
                    cell.group_id not in groups_considered):
                groups_considered.append(cell.group_id)
                res += len(self.group_cells(vr, vc))
        return res


    @staticmethod
    def intern_move(grid, m):
        pass

    def move(self, m):
        '''dir in {'N', 'S', 'E', 'W'}
        Returns true if the move is legal and does it
        Else, returns false
        '''
        pass

    def move_copy(self, m):
        '''dir in {'N', 'S', 'E', 'W'}
        If the move is legal, does it on a copy and returns it
        Else, returns false
        '''
        pass




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



