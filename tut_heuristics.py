from Base.bp2DPlot import plot_packing_state
from Base.bp2DPnt import Point
from Base.bp2DFce import Face2D
from Base.bp2DRct import Box
from Base.bp2DState import Bin
from Base.bp2DAction import State
from bp_blog_entry import example_blog

from Base.bpReadWrite import ReadWrite

import random
import os


def face_intersection(b1: Box, b2: Box) -> Face2D:
    '''Check how much overlap the faces of two rectangles have. 
    Return the overlap, as a face, or return None, if there is no face intersection.'''
    max = 0
    for f1 in b1.get_face_list():
        for f2 in b2.get_face_list():
            intersection = f1.intersect(f2)
            if intersection is not None:
                max += intersection.length()
    return max


def most_enclosed_position_in_bin(bin: Bin, box: Box) -> Point:
    '''Finds the most enclosed feasible position for box in bin.
    it returns the first open point with this property, i.e. 
    it also tries to place as bottom left as possible'''
    pmax = None
    max = -1
    for p in bin.get_pnts_open():
        if bin.can_place_box_at_pnt(box, p):
            box.set_bl(p)
            enclosure = face_intersection(box,
                                          bin.bounding_box)  # check for edge overlap with bounding box, ie if box is placed on side or in corner of bin
            # TODO extremely slow and assumes that remove_box does not fiddle with box.lr and keeps the place position
            for box_stored in bin.boxes_stored:
                enclosure += face_intersection(box, box_stored)
            if enclosure > max:
                max = enclosure
                pmax = p
    return (max, pmax)


def most_enclosed_position_assignment(state: State, box: Box) -> int:
    '''A placement heuristic that puts the next rectangle in the position where the longest part of its
        circumference touches other boxes or the bin. '''

    most_enclosed_positions = [(most_enclosed_position_in_bin(bin, box), i) for i, bin in enumerate(state.bins)]
    bin_idx = sorted(most_enclosed_positions, key=lambda x: (x[0][0], len(state.bins) - x[1]), reverse=True)[0]
    if bin_idx[0][0] != -1:
        placement_success = state.place_box_in_bin_at_pnt(box, bin_idx[1], bin_idx[0][1])
        return bin_idx[1]
    else:
        state.open_new_bin()
        state.place_box_in_bin(box, -1)
        return len(state.bins) - 1



def single_type_heuristic(state: State, heuristic_step=most_enclosed_position_assignment, video=False):
    '''A generic heuristic that applies the same assignment step for each box'''

    counter = 0

    while state.has_open_boxes():
        box = state.get_next_open_box()

        bin_id = heuristic_step(state, box)

        if video:
            bin = state.bins[bin_id]
            plot_packing_state(bin, bin.boxes_stored,
                                   pnts_open=bin.pnts_open,
                                   fname=f"./vis/_box_{counter}_bin_{bin_id}.png", alpha=1.)
            counter += 1

    return state


if __name__ == "__main__":

    # random.seed(666)
    # squares_only = False
    # r1, r2, cont_size = example_blog(squares_only=squares_only)
    # rcts = r1+r2
    # state = State(1, (10, 10), rcts)

    state = ReadWrite.read_state(path="test_instances/test_boxes")
    state.open_new_bin()

    if not os.path.exists("./vis"):
        os.mkdir("./vis")

    heuristics = [most_enclosed_position_assignment]
    names = ['most_enclosed']

    for h, n in zip(heuristics, names):
        print(f"running {n}")
        s = single_type_heuristic(state, heuristic_step=h, video=True)
        for i, bin in enumerate(s.bins):
            plot_packing_state(bin, bin.boxes_stored,
                               pnts_open=bin.pnts_open,
                               fname=f"./vis/{n}_{i}.png", alpha=1.)
