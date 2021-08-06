
#
# script demonstrates brute force search of possible packings
#
# NOTE: ths script will write 234 PNG images to disk
#

import sys

sys.path.append('./Base')

from bp2DBase import * 
from bp2DData import * 
from bp2DPlot import * 

from bp2DState import *
from bp2DAction import *



def initialize_state(rcts, BOX):
    rcts = Rectangle2D.place_rectangles_at_point(rcts, Point2D(-1, -1))
    rcts_clsd = []                   
    rcts_open = rcts                    
    pnts_open = [Point2D(0,0)]
    return State(rcts_clsd, rcts_open, pnts_open, BOX)



stateCounter = 0

def brute_force_search_all_feasible(S):
    global stateCounter
    stateCounter += 1
    
    actions = [Action(p,r) for p in S.pnts_open for r in S.rcts_open]

    for A in actions:
        if A.is_feasible(S):
            S_new = A.apply_to(S)
            
            fName = 'figXmpl05-trial-%d.png' % stateCounter

            S_new.plot(fname=fName)

            brute_force_search_all_feasible(S_new)




            
if __name__ == '__main__':
    BOX  = Rectangle2D(10, 10, Point2D(0, 0))
    rcts = example2()

    S = initialize_state(rcts, BOX)

    brute_force_search_all_feasible(S)
