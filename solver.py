import grid
import sys

class Solver:
    def __init__(self, grid):
        '''grid is a Grid object representing the initial configuration'''
        self.grid = grid
        self.moves = []
        self.index_next_move = 0

    def moveIterator(self):
        for r in range(self.grid.HEIGHT):
            for c in range(self.grid.WIDTH):
                for d in "NSEW":
                    yield Move(r,c,d)

    def solve(self):
        '''launch computation of moves if not already done'''
        if self.moves == []:
            print("Computing a solution...")
            #found_move = True
            #while self.grid.score() < 100 and found_move:
            #    found_move = False
            #    for m in self.moveIterator():
            #        found_move = True:
            #        move_copy()
            moves_done = []
            result_done = []
            # try all moves on this grid and store the ones which are legal
            for m in self.moveIterator():
                r = self.grid.move_copy(m)
                if r != False:
                    moves_done.append(m)
                    result_done.append(r)
            if len(moves_done) > 0: # if this situation is not a dead end (because there is another possible move)
                # try next iteration
            else:
                # dead end
                # check score
                # if it's 100% -> that's a solution
                # else reverse last move and continue





            print("Done!")

    def next_move(self):
        '''Returns a Move object representing the next move according to this Solver
        or None if there is no possible move.
        '''
        if self.moves = []:
            self.solve()
        if self.index_next_move < len(self.moves):
            self.index_next_move += 1
            return self.moves[index_next_move-1]
        else:
            sys.stderr.write("No more moves to play. Sorry.\n")
            return None

    def score(self):
        '''Returns a float corresponding to the current completion percentage'''
        #TODO: move to Grid
        pass
