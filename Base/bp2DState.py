
import itertools

from bp2DBase import *
from bp2DPlot import *




class State:

    def __init__(self, rcts_clsd, rcts_open, pnts_open, box):
        self.rcts_clsd = rcts_clsd  # list of rectangles already placed
        self.rcts_open = rcts_open  # list of rectangles still to be placed
        self.pnts_open = pnts_open  # list of rectangle placing points
        self.box       = box        # box, i.e. rectangle, to be packed 

        
    def copy(self):
        return State(list(self.rcts_clsd),
                     list(self.rcts_open),
                     list(self.pnts_open),
                     self.box)

    
    
    def plot(self, showOpen=False, showPoints=True,
             showBox=True, showGrid=False,
             cols=None, delta=0.1, bgcol='w', fname=None):

        rcts_inside  = self.rcts_clsd
        rcts_outside = self.rcts_open if showOpen else []
        pnts         = self.pnts_open if showPoints else []
        
        cols = compute_colors(len(self.rcts_clsd) + len(self.rcts_open))

        plot_packing_state(self.box, rcts_inside, rcts_outside, pnts, cols,
                           showBox, showGrid, delta, bgcol, fname)
        #plot_packed_box(self.box, self.rcts_clsd, pnts,
        #                 cols, showBox, showGrid, delta, bgcol, fname)




        
if __name__ == '__main__':
    pass
