


class Face2D:
    def __init__(self, p, q):
        self.p = p  # 1st end point of a rectanlge face, type=Point2D
        self.q = q  # 2nd end point of a rectangle face, type=Point2D


    def __eq__(self, other):
        return self.p == other.p and self.q == other.q

    def __ne__(self, other):
        return not self.__eq__(other)


    def interior_contains_point(self, pnt):
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


    
if __name__ == '__main__':
    pass


