
#
# script demonstrares plotting options for packed boxes using
# hand coded examples of sets of recatngles in 'Base/bp2DData.py'
#

import sys

sys.path.append('./Base')

from Base.bp2DBase import * # basic data types (classes)
from Base.bp2DData import * # examples of listes of rectangles
from Base.bp2DPlot import * # functions for plotting / graphical output





if __name__ == '__main__':
    # define a box (width 10, height 10) to be packed
    # data type 'Rectangle2D' is defined in './Base/bp2DRct.py'
    BOX = Box(10, 10, Point(0, 0))

    
    # get a list of (manually packed) rectangles
    # function 'example2' is defined in './Base/bp2DData.py'
    rcts = example2()

    
    # plot the current box and (already packed) rectangles
    # and write the result into a .PDF file
    # function 'plot_packed_box' is defined in './Base/bp2DPlot.py'
    fName = 'figXmpl01-1.pdf'
    plot_packed_box(BOX, rcts, fname=fName)


    # alternatively, plot the current box and (already packed) rectangles
    # and write the result into a .PNG file
    fName = 'figXmpl01-2.png'
    plot_packed_box(BOX, rcts, fname=fName)


    # to create a colored plot, compute a list of matplotlib colors
    # function 'computeColors' is defined in './Base/bp2DPlot.py'
    cols = compute_colors(len(rcts))
    fName = 'figXmpl01-3.pdf'
    plot_packed_box(BOX, rcts, cols=cols, fname=fName)


    # if we would want to, we could also superimopose a grid over the
    # box to better (?) illustrate the setting
    fName = 'figXmpl01-4.pdf'
    plot_packed_box(BOX, rcts, cols=cols, showGrid=True, fname=fName)


    # finally, we may also create a plot with all rectangles outside of
    # the box (mainly to illustrate the "initial state" of the packing
    # problem
    # function 'plot_box_and_rectangles' is in './Base/bp2DPlot.py'
    fName = 'figXmpl01-5.pdf'
    plot_box_and_rectangles(BOX, rcts, cols=cols, fname=fName)

