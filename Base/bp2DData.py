
from bp2DBase import *


def example1():
    r1 = Rectangle2D(6, 3, Point2D(0, 0))
    r2 = Rectangle2D(2, 5, Point2D(6, 0))
    rs = [r1, r2]
    rs = Rectangle2D.sort_rectangles(rs)
    rs = Rectangle2D.name_rectangles(rs)
    return rs


def example2():
    r1 = Rectangle2D(6, 3, Point2D(0, 0))
    r2 = Rectangle2D(2, 5, Point2D(6, 0))
    r3 = Rectangle2D(1, 4, Point2D(8, 0))
    r4 = Rectangle2D(3, 3, Point2D(0, 3))
    rs = [r1, r2, r3, r4]
    rs = Rectangle2D.sort_rectangles(rs)
    rs = Rectangle2D.name_rectangles(rs)
    return rs


def example3():
    r1 = Rectangle2D(7, 3, Point2D(0, 0))
    r2 = Rectangle2D(3, 7, Point2D(7, 0))
    r3 = Rectangle2D(3, 7, Point2D(0, 3))
    r4 = Rectangle2D(7, 3, Point2D(3, 7))
    r5 = Rectangle2D(4, 4, Point2D(3, 3))
    rs = [r1, r2, r3, r4, r5]
    rs = Rectangle2D.sort_rectangles(rs)
    rs = Rectangle2D.name_rectangles(rs)
    return rs


def example4():
    r1 = Rectangle2D(6, 5, Point2D(0, 0))
    r2 = Rectangle2D(4, 1, Point2D(6, 0))
    r3 = Rectangle2D(2, 6, Point2D(6, 1))
    r4 = Rectangle2D(2, 9, Point2D(8, 1))
    r5 = Rectangle2D(3, 2, Point2D(0, 5))
    r6 = Rectangle2D(3, 2, Point2D(3, 5))
    r7 = Rectangle2D(8, 3, Point2D(0, 7))
    rs = [r1, r2, r3, r4, r5, r6, r7]
    rs = Rectangle2D.sort_rectangles(rs)
    rs = Rectangle2D.name_rectangles(rs)
    return rs


def example5():
    r1 = Rectangle2D(6, 5, Point2D(0, 0))
    r2 = Rectangle2D(4, 1, Point2D(6, 0))
    r3 = Rectangle2D(3, 2, Point2D(6, 1))
    r4 = Rectangle2D(1, 9, Point2D(9, 1))
    r5 = Rectangle2D(1, 2, Point2D(6, 3))
    r6 = Rectangle2D(2, 4, Point2D(7, 3))
    r7 = Rectangle2D(2, 2, Point2D(0, 5))
    r8 = Rectangle2D(5, 2, Point2D(2, 5))
    r9 = Rectangle2D(9, 3, Point2D(0, 7))
    rs = [r1, r2, r3, r4, r5, r6, r7, r8, r9]
    rs = Rectangle2D.sort_rectangles(rs)
    rs = Rectangle2D.name_rectangles(rs)
    return rs


def example6():
    r1 = Rectangle2D(6, 5, Point2D(0, 0))
    r2 = Rectangle2D(4, 1, Point2D(6, 0))
    r3 = Rectangle2D(3, 2, Point2D(6, 1))
    r4 = Rectangle2D(1, 9, Point2D(9, 1))
    r5 = Rectangle2D(1, 2, Point2D(6, 3))
    r6 = Rectangle2D(2, 4, Point2D(7, 3))
    r7 = Rectangle2D(2, 5, Point2D(0, 5))
    r8 = Rectangle2D(5, 2, Point2D(2, 5))
    r9 = Rectangle2D(7, 3, Point2D(2, 7))
    rs = [r1, r2, r3, r4, r5, r6, r7, r8, r9]
    rs = Rectangle2D.sort_rectangles(rs)
    rs = Rectangle2D.name_rectangles(rs)
    return rs





if __name__ == '__main__':
    pass


