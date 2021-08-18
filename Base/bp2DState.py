
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

    def update_pnts_open(self):
        self.pnts_open.clear()
        for i in range(self.box.get_w()):  # go over all poinst in box
            for j in range(self.box.get_h()):
                pnt = Point2D(i, j)
                pnt_free = True
                for r in self.rcts_clsd:  # check for each placed rect in box whether point is contained
                    if r.interior_contains_point(pnt):
                        pnt_free = False
                        break
                if pnt_free:
                    self.pnts_open.append(pnt)

        # def get_x(pnt):
        #     return min(pnt.get_x(), pnt.get_y())
        self.pnts_open = sorted(self.pnts_open, key=lambda x: (x.coord[0], x.coord[1]))
        return

    def capacity_available(self):
        filled_capacity = 0
        for r in self.rcts_clsd:
            filled_capacity += r.get_a()
        return self.box.get_a() - filled_capacity


if __name__ == '__main__':
    pass
