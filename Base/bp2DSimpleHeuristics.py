import time

from Base.bp2DPlot import plot_packing_state
from Base.bp2DSimpleHeuristicsFunctions import most_enclosed_position_in_bin
from Base.bp2DState import Bin
from Base.bp2DState import Action, State
from Base.bpUtil import *


def get_all_heuristics():
    return [("first_fit", first_fit), ("first_fit_dec", first_fit_decreasing), ("next_fit", next_fit),
            ("next_fit_dec", next_fit_decreasing), ("most_enclosed_position", most_enclosed_position),
            ("max_rest", max_rest), ("best_fit", best_fit)]


def most_enclosed_position(state: State, box: Box):
    '''A placement heuristic that puts the next rectangle in the position where the longest part of its
        circumference touches other boxes or the bin. '''

    most_enclosed_positions = [(most_enclosed_position_in_bin(bin, box), i) for i, bin in enumerate(state.bins)]
    bin_idx = sorted(most_enclosed_positions, key=lambda x: (x[0][0], len(state.bins) - x[1]), reverse=True)[0]
    if bin_idx[0][0] != -1:
        state.place_box_in_bin_at_pnt(box, bin_idx[1], bin_idx[0][1])
    else:
        state.open_new_bin()
        state.place_box_in_bin(box, -1)


def next_fit(state: State, box: Box):
    placement_success = state.place_box_in_bin(box, -1)

    if not placement_success:
        state.open_new_bin()
        state.place_box_in_bin_at_pnt(box, -1, Point(0, 0))


def first_fit(state: State, box: Box):
    placement_success = False
    for i in range(len(state.bins)):
        placement_success = state.place_box_in_bin(box, i)
        if placement_success:
            break

    if not placement_success:
        state.open_new_bin()
        state.place_box_in_bin_at_pnt(box, -1, Point(0, 0))


def max_rest(state: State, box: Box):
    capacities = [bin.capacity_available() for bin in state.bins]
    bin_idx = np.argsort(capacities)[-1]
    placement_success = state.place_box_in_bin(box, bin_idx)

    if not placement_success:
        state.open_new_bin()
        state.place_box_in_bin(box, -1)


def best_fit(state: State, box: Box):
    capacities = [state.get_bin_i(i).capacity_available()
                  if state.check_if_fits_somewhere_in_box(box, i)
                  else np.inf
                  for i in range(len(state.bins))
                  ]
    best_idx = np.argmin(capacities)
    if capacities[best_idx] == np.inf:
        state.open_new_bin()
        state.place_box_in_bin(box, -1)
    else:
        state.place_box_in_bin(box, best_idx)


def best_fit_decreasing(state: State, box: Box):
    sort_boxes_in_state(state)
    best_fit(state, box)


def next_fit_decreasing(state: State, box: Box):
    sort_boxes_in_state(state)
    next_fit(state, box)


def first_fit_decreasing(state: State, box: Box):
    sort_boxes_in_state(state)
    first_fit(state, box)


def random_fit(state: State, box: Box):
    bin_idx = np.random.choice(len(state.bins))
    pnt = np.random.choice(state.get_bin_i(bin_idx).get_pnts_open())

    if not state.place_box_in_bin_at_pnt(box, bin_idx, pnt):
        state.append_open_box(box)


def single_type_heuristic(state: State, heuristic_step=most_enclosed_position, plot_result=False, plot_steps=False, plot_name=None):
    '''A generic heuristic that applies the same assignment step for each box'''
    start = time.time()
    step = 0
    name = 'plot'
    if plot_name is not None:
        name = plot_name
    while state.has_open_boxes():
        box = state.get_next_open_box()
        heuristic_step(state, box)

        if plot_steps:
            plot_packing_state(state=state, step=step, fname=f"./vis/{name}_step")
            step += 1
    if plot_result:
        plot_packing_state(state, fname=f"./vis/{name}_result")
    state.solution_runtime = time.time() - start
