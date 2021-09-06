from Base.bp2DPlot import plot_packing_state
from Base.bp2DPnt import Point
from Base.bp2DFce import Face2D
from Base.bp2DRct import Box
from Base.bp2DState import Bin
from Base.bp2DAction import State
from bp_blog_entry import example_blog
from Base.bpUtil import sort_boxes

from Base.bpReadWrite import ReadWrite
from tut_heuristics import *

import random
import os



if __name__ == "__main__":

    random.seed(666)
    squares_only = False
    r1, r2, cont_size = example_blog(squares_only=squares_only)
    rcts = r1+r2
    state = State(1, (10, 10), rcts)

    # state = ReadWrite.read_state(path="test_instances/test_boxes")
    # state.open_new_bin()

    if not os.path.exists("./vis"):
        os.mkdir("./vis")

    # choose some placement heuristic(s)
    heuristic = [most_enclosed_position_assignment]
    heur_name = ['most_enclosed']

    # create different sorted copies of the list of open boxes
    # sort_boxes sorts from largest to smallest according to keys computed by keyfkt
    sorted_boxes_area = sort_boxes(state.boxes_open) # sort by area
    sorted_boxes_wh = sort_boxes(state.boxes_open, keyfkt=lambda x: (x.w, x.h)) # sort by width of boxes, break ties by height
    sorted_boxes_hw = sort_boxes(state.boxes_open, keyfkt=lambda x: (x.h, x.w)) # sort by height of boxes, break ties by width

    sorting_strategies = [sorted_boxes_area, sorted_boxes_wh, sorted_boxes_hw]    
    sorting_names = ['area', 'wh', 'hw']

    # loop through different sorting strategies
    for sorting_name, sorting_strategy in zip(sorting_names, sorting_strategies):
        
        # create new set of bins to put boxes into
        new_state = State(bins=1, bin_size=state.bin_size, boxes_open=sorting_strategy)

        # run heuristic for a particular orting strategy
        print(f"running {heur_name}")
        s = single_type_heuristic(new_state, heuristic_step=heuristic, video=False)

        # plot results
        for i, bin in enumerate(s.bins):
            plot_packing_state(bin, bin.boxes_stored,
                        pnts_open=bin.pnts_open,
                        fname=f"./vis/{sorting_name}_{heur_name}_{i}.png", alpha=1.)
