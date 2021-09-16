from Base.bp2DBox import Box
from Base.bp2DPnt import Point


class Bin:

    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.area = w * h  # box, i.e. rectangle, to be packed
        self.pnts_open = None
        self.init_pnts_open()  # list of rectangles still to be placed
        self.boxes_stored = []
        self.bounding_box = Box(w, h, Point(0, 0))

    def init_pnts_open(self):
        # self.pnts_open = {Point(i, j) for i in range(self.w) for j in range(self.h)}
        self.pnts_open = [Point(i, j) for i in range(self.w) for j in range(self.h)]

    def can_place_box_at_pnt(self, box: Box, pnt: Point) -> bool:
        '''Check if Box box can be placed at Point pnt.'''
        if pnt not in self.pnts_open:
            return False
        if box.get_a() > len(self.pnts_open):
            return False

        old_position = box.bl.copy()
        box.move(pnt)

        if not self.bounding_box.contains_rectangle(box):
            box.move(old_position)
            return False
        for bs in self.boxes_stored:
            if bs.overlap(box) > 0:
                box.move(old_position)
                return False
        box.move(old_position)
        return True

    def place_box_at_pnt(self, box: Box, pnt: Point) -> bool:
        '''Place Box box at Point pnt. 
        If the operation is feasible, the function modifies the set of open points and the list of stored boxes and returns True. Otherwise it does nothing and returns False.
        '''
        if self.can_place_box_at_pnt(box, pnt):
            box.move(pnt)
            self.boxes_stored.append(box)
            self.remove_open_pnts(box)
            return True
        else:
            return False

    def get_pnts_open(self):
        return self.pnts_open

    def remove_box(self, box):
        assert box in self.boxes_stored
        self.add_open_pnts(box)
        self.boxes_stored.remove(box)

    def add_open_pnts(self, box: Box):  # TODO shuffles the order of open points if a box is added and then removed
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
