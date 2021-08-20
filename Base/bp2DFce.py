from Base.bp2DPnt import Point

class Face2D:
    def __init__(self, p: Point, q: Point):
        self.p = p  # 1st end point of a rectanlge face, type=Point2D
        self.q = q  # 2nd end point of a rectangle face, type=Point2D


    def __eq__(self, other):
        return self.p == other.p and self.q == other.q

    def __ne__(self, other):
        return not self.__eq__(other)


    def interior_contains_point(self, pnt: Point):
        x, y = pnt.get_coord()
        px, py = self.p.get_coord()
        qx, qy = self.q.get_coord()

        if px == x and qx == x:
            if py < y < qy or qy < y < py:
                return True

        if py == y and qy == y:
            if px < x < qx or qx < x < px:
                return True

        return False

    def _intersect_dim(self, sp: int, sq: int, op: int, oq: int):
        if sp > sq:
            tmp = sq
            sq = sp
            sp = tmp
        if op > oq:
            tmp = oq
            oq = op
            op = tmp

        return max(sp, op), min(sq, oq)

    def intersect(self, other):
        '''Return the face that represents the intersection of two faces. If self and other don't intersect, return None.'''
        spx, spy = self.p.get_coord()
        sqx, sqy = self.q.get_coord()

        opx, opy = other.p.get_coord()
        oqx, oqy = other.q.get_coord()

        lx, hx = self._intersect_dim(spx, sqx, opx, oqx)
        ly, hy = self._intersect_dim(spy, sqy, opy, oqy)

        if lx > hx or ly > hy:
            return None
        else:
            return Face2D(Point(lx, ly), Point(hx, hy))


    def length(self):
        '''Return the length of the face, in units.'''
        px, py = self.p.get_coord()
        qx, qy = self.q.get_coord()

        return abs(px - qx) + abs(py - qy) # rectangles are axis parallel. hence one of the two differences must always be zero



    
if __name__ == '__main__':
    pass


