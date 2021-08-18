
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as clr
from matplotlib.patches import Rectangle
from matplotlib.collections import PatchCollection

from .bp2DRct import *



blu = '#0059ff' # hsv(219., 1., 1. ) = Web color blue 
ora = '#ffa500' # hsv( 39., 1., 1. ) = Web color orange

def compute_colors(k, hue1=40):
    '''
    compute a list of 'k' matplotlib colors
    '''
    dlt  = int(360/k)
    hues = (np.linspace(hue1, hue1+dlt*(k-1), k).astype('int') % 360) / 360.
    return [clr.hsv_to_rgb(np.dstack((hues[i], 1.,1.))).flatten()
            for i in range(k)]



def write_figure(fig, fname):
    '''
    write a mtplotlib figure to disk
    '''
    fmt = fname.split('.')[-1]
    fig.savefig(fname, facecolor=fig.get_facecolor(), edgecolor='w',
                papertype='letter', format=fmt, transparent=False,
                bbox_inches='tight', pad_inches=0.0)




    
def plot_packed_box(box,            # Rectangle2D (required)
                    rcts,           # list of Rectangle2D (can be empty [])
                    pnts=None,      # list of Point2D
                    cols=None,      # list of matplotlib colors
                    showBox=True,   # flag parameter
                    showGrid=False, # flag parameter
                    delta=0.1,      # figure size extension
                    bgcol='w',      # figure background color
                    fname=None):    # figure file name (when writing to disk)
    fig = plt.figure(); fig.patch.set_facecolor(bgcol)
    axs = fig.add_subplot('111', aspect='equal', facecolor=bgcol)

    axs.set_axis_off()
    axs.get_xaxis().set_visible(False)
    axs.get_yaxis().set_visible(False)

    
    # if necessary, compute a list of matplotlib colors
    if cols is None:
        cols = [blu] * len(rcts)


    # determine extesions of box to be plotted
    xmin, ymin = box.get_corner('bl').get_coord()
    xmax, ymax = box.get_corner('tr').get_coord()

    
    # if desired, plot a grid within the box
    if showGrid and box is not None:
        for x in range(1,xmax  ): axs.plot((x,x), (ymin,ymax), 'k:', alpha=0.25)
        for y in range(1,ymax+1): axs.plot((xmin,xmax), (y,y), 'k:', alpha=0.25)

            
    # plot rectangles 
    rectangles = []
    for i, rct in enumerate(rcts):
        x, y = rct.get_corner('bl').get_coord()
        w, h = rct.get_w_and_h()
        n    = rct.get_n()
        rectangles.append(Rectangle((x,y), w, h, color=cols[n], alpha=0.25))
        #rectangles.append(Rectangle((x,y), w, h, color=blu, alpha=0.25))
        
    if rectangles:
        collection = PatchCollection(rectangles, edgecolor='k',
                                     match_original=True)
        axs.add_collection(collection)


    # if desired, plot insertion points in list 'pnts'
    if pnts is not None:
        axs.plot([pnt.get_x()+0.5 for pnt in pnts],
                 [pnt.get_y()+0.5 for pnt in pnts],
                 'o', color='k', ms=8, mew=0, alpha=1.0)

        
    # if desired, plot box
    if showBox:
        axs.plot([xmin,       xmin, xmax, xmax      ],
                 [ymax+delta, ymin, ymin, ymax+delta], '-k', linewidth=3)


    axs.set_xlim(xmin-2*delta, xmax+2*delta)
    axs.set_ylim(ymin-2*delta, ymax+2*delta)


    if fname is None:
        plt.show()
    else:
        write_figure(fig, fname)
    plt.close()









    
def plot_box_and_rectangles(box,
                            rcts,
                            cols=None,  
                            delta=0.1,  
                            bgcol='w',  
                            fname=None):
    fig = plt.figure(); fig.patch.set_facecolor(bgcol)
    axs = fig.add_subplot('211', aspect='equal', facecolor=bgcol)

    axs.set_axis_off()
    axs.get_xaxis().set_visible(False)
    axs.get_yaxis().set_visible(False)

    
    # if necessary, compute a list of matplotlib colors
    if cols is None:
        cols = [blu] * len(rcts)

        
    x, xmax, ymax = 0, 0, 0

    # if desired, plot box
    if box is not None:
        xmin, ymin = box.get_corner('bl').get_coord()
        xmax, ymax = box.get_corner('tr').get_coord()
        ymax      += delta
        axs.plot([xmin, xmin, xmax, xmax],
                 [ymax, ymin, ymin, ymax],
                 color='k', linewidth=3)
        xmax += 10*delta
        x     = xmax
        
    rectangles = []
    for i, rct in enumerate(rcts):
        w, h = rct.get_w_and_h()
        rectangles.append(Rectangle((x,0), w, h, color=cols[i], alpha=0.25))
        x    += w + 5*delta
        xmax  = x 
        ymax  = max(ymax, h+delta)
        
    if rectangles:
        collection = PatchCollection(rectangles, edgecolor='k', 
                                     match_original=True)
        axs.add_collection(collection)

        
    


    axs.set_xlim(-delta, xmax+delta)
    axs.set_ylim(-delta, ymax+delta)

    
    if fname is None:
        plt.show()
    else:
        write_figure(fig, fname)
    plt.close()









    
def plot_packing_state(
        box,
        rcts_clsd,
        rcts_open=[],
        pnts_open=[],
        cols=None, 
        showBox=True,
        showGrid=False,
        delta=0.1,
        bgcol='w',
        fname=None):
    fig = plt.figure(); fig.patch.set_facecolor(bgcol)
    axs = fig.add_subplot('111', aspect='equal', facecolor=bgcol)

    axs.set_axis_off()
    axs.get_xaxis().set_visible(False)
    axs.get_yaxis().set_visible(False)

    
    # if necessary, compute a list of matplotlib colors
    if cols is None:
        cols = [blu] * (len(rcts_clsd) + len(rcts_open))


    # determine extesions of box to be plotted
    xmin, ymin = box.get_corner('bl').get_coord()
    xmax, ymax = box.get_corner('tr').get_coord()

    
    # if desired, plot a grid within the box
    if showGrid and box is not None:
        for x in range(1,xmax  ): axs.plot((x,x), (ymin,ymax), 'k:', alpha=0.25)
        for y in range(1,ymax+1): axs.plot((xmin,xmax), (y,y), 'k:', alpha=0.25)

            
    # plot rectangles inside of box
    rectangles = []
    for i, rct in enumerate(rcts_clsd):
        x, y = rct.get_corner('bl').get_coord()
        w, h = rct.get_w_and_h()
        n    = rct.get_n()
        rectangles.append(Rectangle((x,y), w, h, color=cols[n], alpha=0.25))
    if rectangles:
        collection = PatchCollection(rectangles, edgecolor='k',
                                     match_original=True)
        axs.add_collection(collection)


    # if desired, plot insertion points
    if pnts_open:
        axs.plot([pnt.get_x()+0.5 for pnt in pnts_open],
                 [pnt.get_y()+0.5 for pnt in pnts_open],
                 'o', color='k', ms=8, mew=0, alpha=1.0)

        
    # if desired, plot box
    if showBox:
        axs.plot([xmin,       xmin, xmax, xmax      ],
                 [ymax+delta, ymin, ymin, ymax+delta], '-k', linewidth=3)

        
    # plot rectangles outside of box
    if rcts_open:
        xmax += 10*delta
        x     = xmax

        rectangles = []
        for i, rct in enumerate(rcts_open):
            w, h = rct.get_w_and_h()
            n    = rct.get_n()
            rectangles.append(Rectangle((x,0), w, h, color=cols[n], alpha=0.25))
            x    += w + 5*delta
            xmax  = x 
            ymax  = max(ymax, h+delta)
        
        if rectangles:
            collection = PatchCollection(rectangles, edgecolor='k', 
                                         match_original=True)
            axs.add_collection(collection)

    
    axs.set_xlim(xmin-2*delta, xmax+2*delta)
    axs.set_ylim(ymin-2*delta, ymax+2*delta)


    if fname is None:
        plt.show()
    else:
        write_figure(fig, fname)
    plt.close()




    
if __name__ == '__main__':
    pass
