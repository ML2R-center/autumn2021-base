import os
import random

from Base.bp2DData import *
from Base.bp2DPlot import *
from Base.bp2DState import Bin
from Base.bp2DAction import Action, State

from Base.bpUtil import *

import numpy as np

def example_blog(squares_only=True):
    # [w, (br)]\


    cont_size = 10
    make_rects = lambda l: [Box(r[0], r[0], bl=Point(r[1], r[2])) for r in l]
    rects1 = make_rects([
        [5, 0, 0], [2, 5, 0], [2, 7, 0], [1, 9, 0],
        [1, 9, 1], [1, 5, 2], [1, 6, 2], [3, 7, 2],
        [2, 5, 3], [4, 0, 5], [3, 4, 7], [3, 7, 7],
        [1, 0, 9], [1, 1, 9], [1, 2, 9], [1, 3, 9],
        [2, 4, 5], [2, 6, 5], [2, 8, 5]
    ])
    rects1 = sort_rectangles(rects1)
    rs1 = name_rectangles(rects1)
    if squares_only:
        rects2 = make_rects([
            [5, 0, 0], [2, 5, 0], [1, 9, 0], [1, 9, 1], [2, 7, 0],
            [5, 5, 2], [3, 0, 5], [2, 3, 5], [1, 3, 7],
            [2, 0, 8], [2, 2, 8], [3, 4, 7], [3, 7, 7]
        ])
        rects2 = sort_rectangles(rects2)
        rs2 = name_rectangles(rects2)
    else:
        rs2 = example5()
    return rs1, rs2, cont_size


def make_new_container(cont_size):
    return Box(cont_size, cont_size)


def next_fit(rcts, cont_size=10) -> State:

    s = State(nbins=1, bin_size=(cont_size, cont_size), boxes_open=rcts)

    while s.has_open_boxes():
        r = s.get_next_open_box()
        placement_success = s.place_box_in_bin(r, -1)

        if not placement_success:
            s.open_new_bin()
            s.place_box_in_bin_at_pnt(r, -1, Point(0, 0))

    return s


def first_fit(rcts, cont_size=10, video=False):

    state = State(nbins=1, bin_size=(cont_size, cont_size), boxes_open=rcts)

    while state.has_open_boxes():
        b = state.get_next_open_box()
        placement_success = False
        for i in range(len(state.bins)):
            placement_success = state.place_box_in_bin(b, i)
            if placement_success:
                break

        if not placement_success:
            state.open_new_bin()
            state.place_box_in_bin_at_pnt(b, -1, Point(0, 0))

    return state


def max_rest(rcts, cont_size=10, video=False):

    state = State(nbins=1, bin_size=(cont_size, cont_size), boxes_open=rcts)

    while state.has_open_boxes():
        b = state.get_next_open_box()

        capacities = [bin.capacity_available() for bin in state.bins]
        bin_idx = np.argsort(capacities)[-1]
        placement_success = state.place_box_in_bin(b, bin_idx)

        if not placement_success:
            state.open_new_bin()
            state.place_box_in_bin(b, -1)

    return state

def best_fit(rcts, cont_size=10):

    state = State(nbins=1, bin_size=(cont_size, cont_size), boxes_open=rcts)

    while state.has_open_boxes():
        b = state.get_next_open_box()
        capacities = [state.get_bin_i(i).capacity_available()
                      if state.check_if_fits_somewhere_in_box(b, i)
                      else np.inf
                      for i in range(len(state.bins))
                      ]
        best_idx = np.argmin(capacities)
        if capacities[best_idx] == np.inf:
            state.open_new_bin()
            state.place_box_in_bin(b, -1)
        else:
            state.place_box_in_bin(b, best_idx)

    return state

def best_fit_decreasing(rcts, cont_size=10):
    rcts = sort_rectangles(rcts)
    return best_fit(rcts, cont_size)

def next_fit_decreasing(rcts, cont_size=10):
    rcts = sort_rectangles(rcts)
    return next_fit(rcts, cont_size)

def first_fit_decreasing(rcts, cont_size=10):
    rcts = sort_rectangles(rcts)
    return first_fit(rcts, cont_size)

def random_fit(rcts, cont_size=10, n_cont=5):

    state = State(nbins=6, bin_size=(cont_size, cont_size), boxes_open=rcts)

    while state.has_open_boxes():
        b = state.get_next_open_box()

        bin_idx = np.random.choice(len(state.bins))
        pnt = np.random.choice(state.get_bin_i(bin_idx).get_pnts_open())

        if not state.place_box_in_bin_at_pnt(b, bin_idx, pnt):
            state.append_open_box(b)

    return state

if __name__ == '__main__':

    random.seed(666)
    squares_only = False
    r1, r2, cont_size = example_blog(squares_only=squares_only)
    rcts = r1+r2
    np.random.shuffle(rcts)

    heuristics = [random_fit, first_fit, first_fit_decreasing,
                  next_fit, next_fit_decreasing,
                  best_fit, best_fit_decreasing,
                  max_rest
                  ]
    names = ["rand", "ff", "ffd", "nf", "nfd", "bf", "bfd", "mr"]

    if not os.path.exists("./vis"):
        os.mkdir("./vis")

    for h, n in zip(heuristics, names):
        print(f"running {n}")
        s = h(rcts.copy())
        for i, bin in enumerate(s.bins):
            plot_packing_state(bin, bin.boxes_stored,
                               pnts_open=bin.pnts_open,
                               fname=f"./vis/{n}_{i}.png", alpha=1.)