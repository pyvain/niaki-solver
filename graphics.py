
try:
    import Tkinter
except ImportError:
    raise ImportError, "The python-tk package is required to run this app" # python-imaging-tk
from PIL import Image, ImageTk

from rand_init import rand_grid

HEIGHT = 9
WIDTH = 6
NB_COLORS = 6

class NiakiView(Tkinter.Tk):
    def __init__(self, g):
        Tkinter.Tk.__init__(self, None)
        self.parent = None
        self.title("Niak niak niak...")
        self.g = g
        self.initialize()
        self.draw()
        self.mainloop()

    def initialize(self):
        self.tiles = [ImageTk.PhotoImage(Image.open("img/"+str(i)+".png").resize((64,64),Image.ANTIALIAS)) for i in range(NB_COLORS)]
        self.grid()
        self.cells = [[Tkinter.Label(self, anchor="w", bg="white") for j in range(WIDTH)] for i in range(HEIGHT)]
        for i in range(HEIGHT):
            for j in range(WIDTH):
                self.cells[i][j].grid(column=j,row=i,columnspan=1,sticky='EWNS')

    def draw(self):
        for i in range(HEIGHT):
            for j in range(WIDTH):
                self.cells[i][j].configure(image=self.tiles[self.g[i][j]])



if __name__ == "__main__":
    g = rand_grid()
    #g = [[j for j in range(WIDTH)] for i in range(HEIGHT)]
    NiakiView(g)
    NiakiView(g)
