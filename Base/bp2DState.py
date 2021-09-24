from typing import List

import numpy

from Base.bp2DBin import Bin
from Base.bp2DBox import Box


class State:
    def __init__(self, nbins: int, bin_size: (int, int), boxes_open: List[Box]):
        self.bin_size = bin_size
        self.bins = [Bin(*self.bin_size) for _ in range(nbins)]
        self.boxes_open = boxes_open
        self.solution_runtime = None

    def has_open_boxes(self):
        return len(self.boxes_open) > 0

    def place_box_in_bin_at_pnt(self, box, i: int, pnt):
        # box says if object can be placed there
        # "logic" checks if path to point is reachable
        # TODO: here we can add constraints on the placement, eg check for "gravity" constraints
        return self.bins[i].place_box_at_pnt(box, pnt)

    def place_box_in_bin(self, box: Box, i: int):
        '''
        places box in bin i at the first feasible position
        '''
        pnts_open = self.get_open_pnts_of_bin_i(i)
        for pnt in pnts_open:
            if self.place_box_in_bin_at_pnt(box, i, pnt):
                return True  # placement successful

        return False  # box couldn't be placed

    def check_if_fits_somewhere_in_box(self, box: Box, i: int):
        box_old_bl = box.bl.copy()
        if self.place_box_in_bin(box, i):
            self.remove_box_from_bin(box, i)
            box.move(box_old_bl)
            return True

        return False

    def remove_box_from_bin(self, box: Box, i: int):
        return self.bins[i].remove_box(box)

    def open_new_bin(self):
        self.bins.append(Bin(*self.bin_size))

    def get_open_pnts_of_bin_i(self, i: int):
        return self.bins[i].pnts_open

    def get_next_open_box(self):
        return self.boxes_open.pop(0)

    def insert_open_box(self, box: Box, i=0):
        self.boxes_open.insert(i, box)

    def append_open_box(self, box: Box):
        self.boxes_open.append(box)

    def get_bin_i(self, i: int):
        return self.bins[i]

    def compare_with_unboxed(self, state) -> bool:
        checked = numpy.zeros(len(state.boxes_open), dtype=bool)
        for b in self.bins:
            for box in b.boxes_stored:
                found = False
                for i, unboxed in enumerate(state.boxes_open):
                    same_width = box.get_w() == unboxed.get_w()
                    same_height = box.get_h() == unboxed.get_h()
                    if not checked[i] and same_width and same_height:
                        checked[i] = True
                        found = True
                        break
                if not found:
                    return False

        return True

    def is_valid(self, state) -> bool:
        if len(self.boxes_open) > 0:
            return False
        for b in self.bins:
            for i, boxA in enumerate(b.boxes_stored):
                for j, boxB in enumerate(b.boxes_stored):
                    if i != j and boxA.overlap(boxB):
                        return False
        if not self.compare_with_unboxed(state):
            return False
        return True


class Action:

    def __init__(self, pnt, rct):
        self.rct = rct  # rectangle to be placed
        self.pnt = pnt  # point for rectangle to be placed at

    def __repr__(self):
        return 'action: r%d at (%f,%f)' % (self.rct.n, self.pnt[0], self.pnt[1])

    def complies_with_box(self, state):  # checks whether rct is in bounds
        test = self.rct.place_at(self.pnt)
        return state.area.contains_rectangle(test)

    def complies_with_box_content(self, state):  # checks that no rcts in box overlap
        test = self.rct.place_at(self.pnt)
        for rct in state.rcts_clsd:
            if test.overlap(rct) > 0: return False
        return True

    def is_feasible(self, state):
        return self.complies_with_box(state) and \
               self.complies_with_box_content(state)

    def apply_to(self, state):
        rcts_clsd = list(state.rcts_clsd)  # recall that list([...])
        rcts_open = list(state.rcts_open)  # creates a copy of [...]
        pnts_open = list(state.pnts_open)
        box = state.area

        rct = self.rct
        pnt = self.pnt

        rcts_open.remove(rct)  # works, because we overlaoded == in Rectangle2D
        pnts_open.remove(pnt)  # works, because we overlaoded == in Point2D

        rct_new = rct.place_at(pnt)

        pnts_open.extend(Action.new_placing_points(rct_new,
                                                   state))  # TODO: needed? not sure if blog entry code runs if this line is included
        rcts_clsd.append(rct_new)

        return Bin(rcts_clsd, rcts_open, pnts_open, box)

    def rot_rct(self):
        # forward method for 2DRct.rotate90()
        self.rct.rotate90()

    @staticmethod
    def new_placing_points(rct, state):
        box = state.area
        rcts_clsd = state.rcts_clsd

        pnt_br = rct.get_corner('br')
        pnt_tl = rct.get_corner('tl')

        pnts_new = []

        # test w.r.t. the 1st candidate point
        if pnt_br.get_x() < box.get_w():
            # test if bottom face of box contains candidate point
            if box.get_face('b').interior_contains_point(pnt_br):
                pnts_new.append(pnt_br)
            else:
                touches_tr = False
                touches_tl = False
                # iterate over all previously packed rectangles 
                for r in rcts_clsd:
                    # test if top face of rectangle contains candidate
                    if r.get_face('t').interior_contains_point(pnt_br):
                        pnts_new.append(pnt_br)
                        break

                    if r.get_corner('tr') == pnt_br:
                        touches_tr = True
                    if r.get_corner('tl') == pnt_br:
                        touches_tl = True
                if touches_tr and touches_tl:
                    pnts_new.append(pnt_br)

        # test w.r.t. the 2nd candidate point
        if pnt_tl.get_y() < box.get_h():
            # test if left face of box contains candidate point
            if box.get_face('l').interior_contains_point(pnt_tl):
                pnts_new.append(pnt_tl)
            else:
                touches_br = False
                touches_tr = False
                # iterate over all previously packed rectangles 
                for r in rcts_clsd:
                    # test if right face of rectangle contains candidate
                    if r.get_face('r').interior_contains_point(pnt_tl):
                        pnts_new.append(pnt_tl)
                        break

                    if r.get_corner('br') == pnt_tl:
                        touches_tr = True
                    if r.get_corner('tr') == pnt_tl:
                        touches_tl = True  ## TODO: bug? maybe this broke 2DRct.contains_point()?
                if touches_br and touches_tr:
                    pnts_new.append(pnt_tl)

        return pnts_new


if __name__ == '__main__':
    pass
