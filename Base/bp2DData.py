
from .bp2DBase import *

from .bpUtil import *

def example1():
    r1 = Box(6, 3, Point(0, 0))
    r2 = Box(2, 5, Point(6, 0))
    rs = [r1, r2]
    rs = sort_boxes(rs)
    rs = name_rectangles(rs)
    return rs


def example2():
    r1 = Box(6, 3, Point(0, 0))
    r2 = Box(2, 5, Point(6, 0))
    r3 = Box(1, 4, Point(8, 0))
    r4 = Box(3, 3, Point(0, 3))
    rs = [r1, r2, r3, r4]
    rs = sort_boxes(rs)
    rs = name_rectangles(rs)
    return rs


def example3():
    r1 = Box(7, 3, Point(0, 0))
    r2 = Box(3, 7, Point(7, 0))
    r3 = Box(3, 7, Point(0, 3))
    r4 = Box(7, 3, Point(3, 7))
    r5 = Box(4, 4, Point(3, 3))
    rs = [r1, r2, r3, r4, r5]
    rs = sort_boxes(rs)
    rs = name_rectangles(rs)
    return rs


def example4():
    r1 = Box(6, 5, Point(0, 0))
    r2 = Box(4, 1, Point(6, 0))
    r3 = Box(2, 6, Point(6, 1))
    r4 = Box(2, 9, Point(8, 1))
    r5 = Box(3, 2, Point(0, 5))
    r6 = Box(3, 2, Point(3, 5))
    r7 = Box(8, 3, Point(0, 7))
    rs = [r1, r2, r3, r4, r5, r6, r7]
    rs = sort_boxes(rs)
    rs = name_rectangles(rs)
    return rs


def example5():
    r1 = Box(6, 5, Point(0, 0))
    r2 = Box(4, 1, Point(6, 0))
    r3 = Box(3, 2, Point(6, 1))
    r4 = Box(1, 9, Point(9, 1))
    r5 = Box(1, 2, Point(6, 3))
    r6 = Box(2, 4, Point(7, 3))
    r7 = Box(2, 2, Point(0, 5))
    r8 = Box(5, 2, Point(2, 5))
    r9 = Box(9, 3, Point(0, 7))
    rs = [r1, r2, r3, r4, r5, r6, r7, r8, r9]
    rs = sort_boxes(rs)
    rs = name_rectangles(rs)
    return rs


def example6():
    r1 = Box(6, 5, Point(0, 0))
    r2 = Box(4, 1, Point(6, 0))
    r3 = Box(3, 2, Point(6, 1))
    r4 = Box(1, 9, Point(9, 1))
    r5 = Box(1, 2, Point(6, 3))
    r6 = Box(2, 4, Point(7, 3))
    r7 = Box(2, 5, Point(0, 5))
    r8 = Box(5, 2, Point(2, 5))
    r9 = Box(7, 3, Point(2, 7))
    rs = [r1, r2, r3, r4, r5, r6, r7, r8, r9]
    rs = sort_boxes(rs)
    rs = name_rectangles(rs)
    return rs





if __name__ == '__main__':
    pass


