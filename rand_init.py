HEIGHT = 9
WIDTH = 6
NB_COLORS = 6

def test_ready(g):
    for i in range(HEIGHT):
        for j in range(WIDTH):
            for vi, vj in [(i-1,j), (i+1,j), (i,j-1), (i,j+1)]:
                if vi >= 0 and vj >= 0 and vi < HEIGHT and vj < WIDTH and g[vi][vj] == g[i][j]:
                    return False
    return True

def print_grid(g):
    print("-----------")
    for l in g:
        print(l)

def rand_grid():
    from random import shuffle
    g = [[j for j in range(WIDTH)] for i in range(HEIGHT)]
    while not test_ready(g):
        for i in range(HEIGHT):
            shuffle(g[i])
        print_grid(g)
        if(test_ready(g)):
            return g
        for j in range(WIDTH):
            c = [g[i][j] for i in range(HEIGHT)]
            shuffle(c)
            for i in range(HEIGHT):
                g[i][j] = c[i]
        print_grid(g)
        if(test_ready(g)):
            return g
    return g

if __name__ == "__main__":
    print("Niak niak niak...")
    g = rand_grid()
    for l in g:
        print(l)
