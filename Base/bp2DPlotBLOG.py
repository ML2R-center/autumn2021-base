import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as clr
from matplotlib.patches import Rectangle
from matplotlib.collections import PatchCollection

from .bp2DRct import *



blu = '#0059ff' # hsv(219., 1., 1. ) = Web color blue 
ora = '#ffa500' # hsv( 39., 1., 1. ) = Web color orange

ml2r_bg_dark = (1/255)*np.array([37, 37, 34]) # '#252222' # machinelearning-blog box background hsv(0,8,15) rgb(37, 34, 34)
ml2r_bg_light = (1/255)*np.array([216, 216, 216]) # '#d8d8d8' # some light gray color hsv(0,0,85) rgb(216, 216, 216)
ml2r_or = (1/255)*np.array([250, 184, 48]) # '#fab830' # ml2r bonn orange hsv(40,81,98) rgb(250, 184, 48)
ml2r_bl = (1/255)*np.array([4, 69, 115]) # '#044573' # ml2r bonn blue hsv(205,97,45) rgb(4, 69, 115)
ml2r_gr = (1/255)*np.array([128, 181, 44]) # '#80b52c' # ml2r dortmund green hsv(83,76,71) rgb(128, 181, 44)
ml2r_darkcyan = (1/255)*np.array([0, 147, 145]) # '#009391' # ml2r fraunhofer darkcyan(?) hsv(179,100,58) rgb(0, 147, 145)

ml2r_bg = {'light': ml2r_bg_light, 'dark':ml2r_bg_dark}
ml2r_cols = {'orange': ml2r_or,
             'blue': ml2r_bl,
             'green': ml2r_gr,
             'darkcyan': ml2r_darkcyan}
ml2r_cols_list = [ml2r_or, ml2r_bl, ml2r_gr, ml2r_darkcyan]

def compute_colors(k, hue1=40):
    '''
    compute a list of 'k' matplotlib colors
    '''
    if k == 0:
        k=1
    dlt  = int(360/k)
    hues = (np.linspace(hue1, hue1+dlt*(k-1), k).astype('int') % 360) / 360.
    return [clr.hsv_to_rgb(np.dstack((hues[i], 1.,1.))).flatten()
            for i in range(k)]

def sample_ml2r_colors(k):
    cols = list(ml2r_cols.keys())
    return [ml2r_cols[cols[i % len(cols)]] for i in range(k)]

def write_figure(fig, fname):
    '''
    write a mtplotlib figure to disk
    '''
    fmt = fname.split('.')[-1]
    if fmt == 'png':
        fig.savefig(fname, facecolor=fig.get_facecolor(), edgecolor='w',
                    papertype='letter', format=fmt, transparent=False,
                    bbox_inches='tight', pad_inches=0.05, dpi=240)
    else:
        fig.savefig(fname, facecolor=fig.get_facecolor(), edgecolor='w',
                    papertype='letter', format=fmt, transparent=False,
                    bbox_inches='tight', pad_inches=0.0)

def color_rct(rct):
    return ml2r_cols_list[rct.get_n() % len(ml2r_cols_list)]
    
def plot_packed_box(box,            # Rectangle2D (required)
                    rcts,           # list of Rectangle2D (can be empty [])
                    pnts=None,      # list of Point2D
                    cols=None,      # list of matplotlib colors
                    showBox=True,   # flag parameter
                    showGrid=False, # flag parameter
                    delta=0.1,      # figure size extension
                    bgcol='w',      # figure background color
                    fname=None,     # figure file name (when writing to disk)
                    alpha=0.25):    # default alpha val
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
        for x in range(1,xmax  ): axs.plot((x,x), (ymin,ymax), 'k:', alpha=alpha)
        for y in range(1,ymax+1): axs.plot((xmin,xmax), (y,y), 'k:', alpha=alpha)

            
    # plot rectangles 
    rectangles = []
    for i, rct in enumerate(rcts):
        x, y = rct.get_corner('bl').get_coord()
        w, h = rct.get_w_and_h()
        n    = rct.get_n()
        rectangles.append(Rectangle((x,y), w, h, color=color_rct(rct), alpha=alpha))
        #rectangles.append(Rectangle((x,y), w, h, color=blu, alpha=alpha))
        
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
                            fname=None,
                            alpha=0.25):
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
        rectangles.append(Rectangle((x,0), w, h, color=color_rct(rct), alpha=alpha))
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
        fname=None,
        alpha=0.25):
    fig = plt.figure(); fig.patch.set_facecolor(bgcol)
    axs = fig.add_subplot('111', aspect='equal', facecolor=bgcol)

    axs.set_axis_off()
    axs.get_xaxis().set_visible(False)
    axs.get_yaxis().set_visible(False)

    
    # if necessary, compute a list of matplotlib colors
    # if cols is None:
    #     cols = [blu] * (len(rcts_clsd) + len(rcts_open))


    # determine extesions of box to be plotted
    xmin, ymin = box.get_corner('bl').get_coord()
    xmax, ymax = box.get_corner('tr').get_coord()

    
    # if desired, plot a grid within the box
    if showGrid and box is not None:
        for x in range(1,xmax  ): axs.plot((x,x), (ymin,ymax), 'k:', alpha=alpha)
        for y in range(1,ymax+1): axs.plot((xmin,xmax), (y,y), 'k:', alpha=alpha)

            
    # plot rectangles inside of box
    rectangles = []
    for i, rct in enumerate(rcts_clsd):
        x, y = rct.get_corner('bl').get_coord()
        w, h = rct.get_w_and_h()
        n    = rct.get_n()
        rectangles.append(Rectangle((x,y), w, h, color=color_rct(rct), alpha=alpha))
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
            rectangles.append(Rectangle((x,0), w, h, color=color_rct(rct), alpha=alpha))
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
