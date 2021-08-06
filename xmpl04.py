
#
# script demonstrates the concepts of states and actions in bin packing
# it basically does the same as xmpl03.py but creates a different kind of plots
#

import sys

sys.path.append('./Base')

from bp2DBase import * 
from bp2DData import * 
from bp2DPlot import * 

from bp2DState import *
from bp2DAction import *




def xmpl1():
    r1 = Rectangle2D(2, 2, Point2D(-1, -1))
    r2 = Rectangle2D(2, 2, Point2D(-1, -1))
    r3 = Rectangle2D(2, 2, Point2D(-1, -1))
    r4 = Rectangle2D(2, 1, Point2D(-1, -1))
    r5 = Rectangle2D(8, 1, Point2D(-1, -1))
    r6 = Rectangle2D(1, 8, Point2D(-1, -1))
    r7 = Rectangle2D(2, 1, Point2D(-1, -1))
    rs = [r1, r2, r3, r4, r5, r6, r7]
    rs = Rectangle2D.name_rectangles(rs)
    return rs



            
if __name__ == '__main__':
    BOX = Rectangle2D(10, 10, Point2D(0, 0))

    rcts = xmpl1()

    rcts_clsd = []                   
    rcts_open = rcts                
    pnts_open = [Point2D(0.,0.)]

    S = State(rcts_clsd, rcts_open, pnts_open, BOX)
    S.plot(showOpen=True, fname='figXmpl04-1.pdf')

    r1, r2, r3, r4, r5, r6, r7 = rcts
    A = Action(Point2D(0, 0), r1)
    S = A.apply_to(S)
    S.plot(showOpen=True, fname='figXmpl04-2.pdf')
    A = Action(Point2D(0, 2), r5)
    S = A.apply_to(S)
    S.plot(showOpen=True, fname='figXmpl04-3.pdf')
    A = Action(Point2D(2, 0), r4)
    S = A.apply_to(S)
    S.plot(showOpen=True, fname='figXmpl04-4.pdf')
    A = Action(Point2D(4, 0), r2)
    S = A.apply_to(S)
    S.plot(showOpen=True, fname='figXmpl04-5.pdf')
    A = Action(Point2D(2, 1), r7)
    S = A.apply_to(S)
    S.plot(showOpen=True, fname='figXmpl04-6.pdf')
