import numpy

from .bp2DFce import Face2D
from .bp2DPnt import Point


class Box:

    def __init__(self, w, h, bl=Point(0, 0), n=None):
        self.bl = bl  # bottom left corner
        self.tr = bl + Point(w, h)  # top right corner
        self.w = int(w)  # width
        self.h = int(h)  # height
        self.a = w * h  # area
        self.n = n  # number / name
        self.color = None

    def __eq__(self, other):
        return self.bl == other.bl and self.tr == other.tr

    def __ne__(self, other):
        return not self.__eq__(other)

    def move(self, new_bl: Point):
        self.bl = new_bl
        self.tr = self.bl + Point(self.w, self.h)

    def get_a(self):
        return self.a

    def get_n(self):
        return self.n

    def get_w(self):
        return self.w

    def get_h(self):
        return self.h

    def get_w_and_h(self):
        return (self.w, self.h)

    def get_interior_points(self):
        return [Point(i, j) for i in range(self.bl.get_x(), self.bl.get_x() + self.get_w())
                for j in range(self.bl.get_y(), self.bl.get_y() + self.get_h())]

    def contains_point(self, pnt):
        x, y = pnt.get_coord()
        xmin, ymin = self.bl.get_coord()
        xmax, ymax = self.tr.get_coord()
        return xmin <= x <= xmax and ymin <= y <= ymax

    def contains_rectangle(self, other):
        xmins, ymins = self.bl.get_coord()
        xmaxs, ymaxs = self.tr.get_coord()
        xmino, ymino = other.bl.get_coord()
        xmaxo, ymaxo = other.tr.get_coord()
        return xmins <= xmino and \
               xmaxs >= xmaxo and \
               ymins <= ymino and \
               ymaxs >= ymaxo

    def touches_rectangle(self, other):  # TODO Bug: does not cover all cases.
        for corner in other.get_corner_list():
            if self.contains_point(corner):
                return True
        return False

    ####
    def get_corner(self, cname):
        if cname == 'bl': return self.bl
        if cname == 'tr': return self.tr
        if cname == 'br': return self.bl + Point(self.w, 0)
        if cname == 'tl': return self.bl + Point(0, self.h)

    def get_corner_list(self):
        return [self.get_corner(cname) for cname in ['bl', 'br', 'tr', 'tl']]

    def get_face(self, fname):
        if fname == 't': return Face2D(self.get_corner('tl'),
                                       self.get_corner('tr'))
        if fname == 'b': return Face2D(self.get_corner('bl'),
                                       self.get_corner('br'))
        if fname == 'l': return Face2D(self.get_corner('bl'),
                                       self.get_corner('tl'))
        if fname == 'r': return Face2D(self.get_corner('br'),
                                       self.get_corner('tr'))

    def get_face_list(self):
        return [self.get_face(fname) for fname in ['b', 'r', 't', 'l']]

    def place_at(self, pnt):
        return Box(self.w, self.h, pnt, self.n)

    def shift_by(self, vec):
        return self.place_at(self.bl + Point(*vec))

    def overlap(self, other):
        bl_max = numpy.maximum(self.bl.get_coord(), other.bl.get_coord())
        tr_min = numpy.minimum(self.tr.get_coord(), other.tr.get_coord())

        if bl_max[0] <= tr_min[0] and bl_max[1] <= tr_min[1]:
            return (tr_min[0] - bl_max[0]) * (tr_min[1] - bl_max[1])
        else:
            return 0

    def interior_contains_point(self, pn):
        # same as contains_point but < instead of <= in n <= max check
        # does not look right, but when implementing the simple heuristics and plotting the results
        # some bins were plotted out of bounds, with this changes results were consistently good
        # need to find out why
        x, y = pn.get_coord()
        xmin, ymin = self.bl.get_coord()
        xmax, ymax = self.tr.get_coord()
        return xmin <= x < xmax and ymin <= y < ymax  # this should be wrong

    def rotate90(self):
        # bl stays the same
        self.w, self.h = self.h, self.w

    def set_color(self, c):
        self.color = c

    def get_color(self):
        return self.color

    # @staticmethod
    # def area_of_rectangles(rcts):
    #     return np.sum([rct.a for rct in rcts]) if rcts else 0
    #
    # @staticmethod
    # def x_extension_of_rectangles(rcts):
    #     return np.max([rct.tr.get_x() for rct in rcts]) if rcts else 0
    #
    # @staticmethod
    # def y_extension_of_rectangles(rcts):
    #     return np.max([rct.tr.get_y() for rct in rcts]) if rcts else 0
    #
    # @staticmethod
    # def bounding_box_of_rectangles(rcts):
    #     if not rcts:
    #         return Box(0, 0)
    #     xbl = np.min([rct.bl.get_x() for rct in rcts])
    #     ybl = np.min([rct.bl.get_y() for rct in rcts])
    #     xtr = np.max([rct.tr.get_x() for rct in rcts])
    #     ytr = np.max([rct.tr.get_y() for rct in rcts])
    #     return Box(xtr - xbl, ytr - ybl, Point(xbl, ybl))

    # @staticmethod
    # def sort_rectangles(rcts):
    #     def get_a(rct):
    #         return rct.a
    #     return (sorted(rcts, key=get_a)[::-1])

    @staticmethod
    def place_rectangles_at_point(rcts, pnt):
        return [rct.place_at(pnt) for rct in rcts]

    @staticmethod
    def place_rectangles_at_points(rcts, pnts):
        return [rcts[i].place_at(pnts[i]) for i in range(len(rcts))]


if __name__ == '__main__':
    pass
