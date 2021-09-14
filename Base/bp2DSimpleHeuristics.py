
from Base.bp2DState import Bin
from Base.bp2DAction import Action, State
from Base.bpUtil import *

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
    rcts = sort_boxes(rcts)
    return best_fit(rcts, cont_size)

def next_fit_decreasing(rcts, cont_size=10):
    rcts = sort_boxes(rcts)
    return next_fit(rcts, cont_size)

def first_fit_decreasing(rcts, cont_size=10):
    rcts = sort_boxes(rcts)
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