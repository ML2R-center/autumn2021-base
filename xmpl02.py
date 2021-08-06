
#
# script plots all hand-coded examples of packed rectangles in
# './Base/bp2dData.py'
#

import sys

sys.path.append('./Base')

from bp2DBase import * 
from bp2DData import * 
from bp2DPlot import * 





if __name__ == '__main__':
    BOX = Rectangle2D(10, 10, Point2D(0, 0))
    
    examples = [example1(), example2(), example3(),
                example4(), example5(), example6()]

    for i, example in enumerate(examples):
        rcts = example
        cols = compute_colors(len(rcts))
        
        fName = 'figXmpl02-%d.png' % (i+1)
        plot_packed_box(BOX, rcts, cols=cols, fname=fName)
