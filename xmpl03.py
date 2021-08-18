
#
# script demonstrates the concepts of states and actions in bin packing
#


from Base.bp2DBase import *
from Base.bp2DData import *
from Base.bp2DPlot import *

from Base.bp2DState import *
from Base.bp2DAction import *
from Base.bp2DRct import *
from Base.bp2DPnt import *



def xmpl1():
    r1 = Box(2, 2, Point(-1, -1))
    r2 = Box(2, 2, Point(-1, -1))
    r3 = Box(2, 2, Point(-1, -1))
    r4 = Box(2, 1, Point(-1, -1))
    r5 = Box(8, 1, Point(-1, -1))
    r6 = Box(1, 8, Point(-1, -1))
    r7 = Box(2, 1, Point(-1, -1))
    rs = [r1, r2, r3, r4, r5, r6, r7]
    rs = Box.name_rectangles(rs)
    return rs



            
if __name__ == '__main__':
    # define a 10 x 10 box to be packed
    BOX = Box(10, 10, Point(0, 0))

    
    # function xmpls1() contains hand crafted rectangles to work with
    rcts = xmpl1()

    
    # a state in a bin packing process consists of
    #   a closed-list of rectangle already placed in the box
    #   an open-list of rectangles still outside of the boc
    #   an open-list of insertion points where rectanlge could be placed
    rcts_clsd = []                   
    rcts_open = rcts                
    pnts_open = [Point(0., 0.)]
    S = Bin(rcts_clsd, rcts_open, pnts_open, BOX)
    S.plot(showGrid=True, fname='figXmpl03-1.png')

    # the following is "manual" bin packing ...
    # just to illustrate the idea of insertion points
    # it should not be taken seriously
    r1, r2, r3, r4, r5, r6, r7 = rcts
    A = Action(Point(0, 0), r1)
    S = A.apply_to(S)
    S.plot(showGrid=True, fname='figXmpl03-2.png')
    A = Action(Point(0, 2), r5)
    S = A.apply_to(S)
    S.plot(showGrid=True, fname='figXmpl03-3.png')
    A = Action(Point(2, 0), r4)
    S = A.apply_to(S)
    S.plot(showGrid=True, fname='figXmpl03-4.png')
    A = Action(Point(4, 0), r2)
    S = A.apply_to(S)
    S.plot(showGrid=True, fname='figXmpl03-5.png')
    A = Action(Point(2, 1), r7)
    S = A.apply_to(S)
    S.plot(showGrid=True, fname='figXmpl03-6.png')
