
from .bp2DPlot import *
from .bpUtil import *




class Bin:

    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.area = w*h        # box, i.e. rectangle, to be packed
        self.pnts_open =  None
        self.init_pnts_open()  # list of rectangles still to be placed
        self.boxes_stored = []
        self.bounding_box = Box(w,h, Point(0,0))

    def init_pnts_open(self):
        # self.pnts_open = {Point(i, j) for i in range(self.w) for j in range(self.h)}
        self.pnts_open = [Point(i, j) for i in range(self.w) for j in range(self.h)]

    def place_box_at_pnt(self, box: Box, pnt: Point) -> bool:
        if pnt not in self.pnts_open:
            return False
        if box.get_a() > len(self.pnts_open):
            return False

        old_position = box.bl.copy()
        box.set_bl(pnt)

        if not self.bounding_box.contains_rectangle(box):
            box.set_bl(old_position)
            return False
        for bs in self.boxes_stored:
            if bs.overlap(box) > 0:
                box.set_bl(old_position)
                return False
        self.boxes_stored.append(box)
        self.remove_open_pnts(box)
        return True

    def get_pnts_open(self):
        return self.pnts_open

    def remove_box(self, box):
        assert box in self.boxes_stored
        self.add_open_pnts(box)
        self.boxes_stored.remove(box)

    def add_open_pnts(self, box: Box):
        self.pnts_open.extend(box.get_interior_points())

    def remove_open_pnts(self, box: Box):
        for bp in box.get_interior_points():
            self.pnts_open.remove(bp)

    def capacity_available(self):
        return len(self.pnts_open)

    def get_corner(self, c: str):
        return self.bounding_box.get_corner(c)

if __name__ == '__main__':
    pass
