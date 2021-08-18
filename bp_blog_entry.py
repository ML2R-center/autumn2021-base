import sys


import random

from Base.bp2DBase import *
from Base.bp2DData import *
from Base.bp2DPlot import *
from Base.bp2DState import Bin
from Base.bp2DAction import Action

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


def next_fit(rcts, cont_size=10):

    containers = []  # will be a list of states, each state contain the rectangles placed in its container
    rcts_open = rcts
    rcts_placed = []
    current_state = Bin([], [], [], make_new_container(cont_size))
    current_state.update_pnts_open()  # see what points are left
    i = 0
    while(i < len(rcts_open)):
        r = rcts_open[i]

        current_state.rcts_open.append(r) # put new r into queue
        placement_success, current_state = place_in_container(r, current_state)
        i += placement_success  # hacky :)

        if not placement_success:
            current_state.rcts_open.remove(r) # dont queue rect for current container
            containers.append(current_state) # store container
            current_state = Bin([], [], [], make_new_container(cont_size))

        current_state.update_pnts_open()  # see what points are left

    containers.append(current_state)

    return containers

def place_in_container(r, c):
    placement_success = False
    if c.capacity_available() >= r.get_a():
        for p in c.pnts_open:
            a = Action(p, r)
            if a.is_feasible(c):
                c = a.apply_to(c)
                placement_success = True
                break
            else:
                if r.w != r.h:
                    a.rot_rct()
                    if a.is_feasible(c):
                        c = a.apply_to(c)
                        placement_success = True
                        break
                    a.rot_rct()  # undo rotation

    return placement_success, c

def get_placement(r, c):
    # returns either the first feasible action or 'None'
    for p in c.pnts_open:
        a = Action(p, r)
        if a.is_feasible(c):
            return a
    return None

def first_fit(rcts, cont_size=10, video=False):
    containers = []  # will be a list of states, each state contain the rectangles placed in its container
    rcts_open = rcts
    rcts_placed = []
    for _ in range(3):
        current_state = Bin([], [], [], make_new_container(cont_size))
        current_state.update_pnts_open()  # see what points are left
        containers.append(current_state)

    i = 0
    bad_placement = 0
    while i < len(rcts):
        placement_success = False
        r = rcts[i]
        last_c = -1
        for c in range(len(containers)):
            cont = containers[c]
            cont.rcts_open.append(r)
            cont.update_pnts_open()
            placement_success, new_cont = place_in_container(r, cont)
            if placement_success:
                new_cont.update_pnts_open()
                containers[c] = new_cont
                rcts_placed.append(r)
                last_c = c
                break
            else:
                bad_placement += 1 # we didnt place it in this container
                cont.rcts_open.remove(r)
        if not placement_success:
            new_cont = Bin([], [r], [], make_new_container(cont_size))
            new_cont.update_pnts_open()
            _, new_cont = place_in_container(r, new_cont)
            new_cont.update_pnts_open()
            containers.append(new_cont)
        if video:
            for j in range(3):
                containers[j].plot(alpha=1., fname=f'./ff_vis/{i}_{j}.png')
        i = i + 1

    return containers, bad_placement


def max_rest(rcts, cont_size=10, video=False):
    # place objet in the container with most space available
    containers = []  # will be a list of states, each state contain the rectangles placed in its container
    rcts_open = rcts
    rcts_placed = []
    current_state = Bin([], [], [], make_new_container(cont_size))
    current_state.update_pnts_open()  # see what points are left
    containers.append(current_state)
    i = 0
    bad_placements = 0
    while i < len(rcts_open):
        r = rcts_open[i]
        max_cont_idx = np.argmax([cont.capacity_available() for cont in containers])
        max_cont = containers[max_cont_idx]
        max_cont.rcts_open.append(r)
        max_cont.update_pnts_open()
        placement_success, new_cont = place_in_container(r, max_cont)
        if placement_success:
            new_cont.update_pnts_open()
            containers[max_cont_idx] = new_cont
            rcts_placed.append(r)
        else:
            bad_placements += 1
            max_cont.rcts_open.remove(r)
            new_cont = Bin([], [r], [], make_new_container(cont_size))
            new_cont.update_pnts_open()
            _, new_cont = place_in_container(r, new_cont)
            new_cont.update_pnts_open()
            containers.append(new_cont)
        if video:
            idx = max_cont_idx if placement_success  else len(containers)-1
            containers[idx].plot(alpha=1., fname=f'./mr_vis/{i}_{idx}.png')
        i = i + 1

    return containers, bad_placements

def best_fit(rcts, cont_size=10):
    containers = []  # will be a list of states, each state contain the rectangles placed in its container
    rcts_open = rcts
    rcts_placed = []
    current_state = Bin([], [], [], make_new_container(cont_size))
    current_state.update_pnts_open()  # see what points are left
    containers.append(current_state)
    i = 0
    while i < len(rcts_open):
        r = rcts_open[i]

        remaining_capacities = [cont.capacity_available()-r.get_a() for cont in containers]
        placements = [get_placement(r, cont) for cont in containers]
        first_fit_idx = -1
        for j, p in enumerate(placements):
            if p is not None:
                first_fit_idx = j
                break

        if first_fit_idx == -1: # r didn't fit anywhere
            new_cont = Bin([], [r], [], make_new_container(cont_size))
            new_cont.update_pnts_open()
            _, new_cont = place_in_container(r, new_cont)
            new_cont.update_pnts_open()
            containers.append(new_cont)
        else:
            best_fit_idx = first_fit_idx
            best_fit_capacity = remaining_capacities[best_fit_idx]
            for j, (cap, p) in enumerate(zip(remaining_capacities[first_fit_idx+1:],
                                             placements[first_fit_idx+1:]),
                                         start=first_fit_idx+1):
                if p is not None:
                    if cap < best_fit_capacity:
                        best_fit_idx = j
                        best_fit_capacity = cap
            best_cont = containers[best_fit_idx]
            best_cont.rcts_open.append(r)
            _, best_cont = place_in_container(r, best_cont)
            best_cont.update_pnts_open()
            containers[best_fit_idx] = best_cont
        i = i + 1

    return containers

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
    containers = []  # will be a list of states, each state contain the rectangles placed in its container
    rcts_open = rcts
    rcts_placed = []
    for _ in range(n_cont):
        current_state = Bin([], [], [], make_new_container(cont_size))
        current_state.update_pnts_open()  # see what points are left
        random.shuffle(current_state.pnts_open) # give the indices a good shake
        containers.append(current_state)

    i = 0
    bad_placements = 0
    i_mem = []
    while i < len(rcts_open):
        if len(i_mem) == n_cont:
            return -1, bad_placements
        r = rcts_open[i]
        idx = random.randint(0, n_cont-1)
        cont = containers[idx]
        cont.rcts_open.append(r)
        random.shuffle(cont.pnts_open)
        placement_success, cont = place_in_container(r, cont)
        cont.update_pnts_open()
        if placement_success:
            i = i + 1
            i_mem.clear()
            containers[idx] = cont
        else:
            bad_placements += 1
            cont.rcts_open.remove(r)
            if not cont in i_mem:
                i_mem.append(cont)
        containers[idx] = cont
    return containers, bad_placements

if __name__ == '__main__':

    random.seed(666)
    squares_only = False
    r1, r2, cont_size = example_blog(squares_only=squares_only)
    b1, b2 = Box(cont_size, cont_size, Point(0, 0)), \
             Box(cont_size, cont_size, Point(0, 0))
    c1, c2 = sample_ml2r_colors(len(r1)), sample_ml2r_colors(len(r2))

    for r, c in zip(r1, c1):
        r.set_color(c)
    for r, c in zip(r2, c2):
        r.set_color(c)

    state1 = Bin(r1, [], [], b1)
    state2 = Bin(r2, [], [], b2)

    plt_args = {'alpha': 1., 'bgcol': ml2r_bg_light}

    rcts = r1+r2 # concat rectangle lists
    name_rectangles(rcts) # names in r1, r2 overlap

    state1.plot(fname="./test/state1.png", **plt_args)
    state2.plot(fname="./test/state2.png", **plt_args)

    plot_packed_box(b1, rcts[:len(r1)], fname='./test/figR1packed.png', **plt_args)
    plot_packed_box(b2, rcts[len(r1):], fname='./test/figR2packed.png', **plt_args)
    plot_box_and_rectangles(b1, rcts[:len(r1)], fname='./test/figR1.png', **plt_args)
    plot_box_and_rectangles(b2, rcts[len(r1):], fname='./test/figR2.png', **plt_args)

    if not squares_only:
        for r in rcts[len(r1):]:
            if random.randint(0,1):
                r.rotate90()
    rcts = [r.place_at(Point(0, 0)) for r in rcts]

    rcts_sorted = sort_rectangles(rcts)
    plot_box_and_rectangles(None, rcts_sorted, fname='./test/Rsorted.png', **plt_args)



    rcts_shuffled = rcts_sorted.copy()
    random.shuffle(rcts_shuffled)
    plot_box_and_rectangles(None , rcts_shuffled, fname='./test/shuffled.png', **plt_args)

    # containers = next_fit(rcts_shuffled, cont_size)
    # for i, c in enumerate(containers):
    #     c.plot(fname=f'./test/nf_shuffled{i}.png', **plt_args)
    #
    # containers = next_fit(rcts_sorted, cont_size)
    # for i, c in enumerate(containers):
    #     c.plot(fname=f'./test/nfd{i}.png', **plt_args)


    # containers = best_fit_decreasing(rcts_shuffled, cont_size)
    # for i, c in enumerate(containers):
    #     c.plot(fname=f'./test/bfd_shuffled{i}.png', **plt_args)

    def eval_space_left(conts):
        # given a list of containers, count number of open coordinates across all of them
        space_left = []
        for c in conts:
            c.update_pnts_open()
            space_left.append(len(c.pnts_open))
        return space_left

    containers, bad_placements_mr = max_rest(rcts_shuffled.copy(), cont_size, video=True)
    space_left_mr = eval_space_left(containers)
    for i, c in enumerate(containers):
        c.plot(fname=f'./test/mr_{i}.png', **plt_args)

    containers, bad_placements_ff = first_fit(rcts_shuffled.copy(), cont_size, video=True)
    space_left_ff = eval_space_left(containers)
    for i, c in enumerate(containers):
        c.plot( fname=f'./test/ff_shuffled{i}.png', **plt_args)

    containers, bad_placements_ffd = first_fit(rcts_sorted.copy(), cont_size)
    space_left_ffd = eval_space_left(containers)
    for i, c in enumerate(containers):
        c.plot(fname=f'./test/ffd_shuffled{i}.png', **plt_args)

    containers, bad_placements_mrs = max_rest(rcts_sorted.copy(), cont_size)
    space_left_mrs = eval_space_left(containers)
    for i, c in enumerate(containers):
        c.plot(fname=f'./test/mr_sorted_{i}.png', **plt_args)

    containers, bad_placements_rnd = random_fit(rcts_shuffled.copy(), n_cont=4)
    space_left_rnd = eval_space_left(containers)
    for i, c in enumerate(containers):
        c.plot(fname=f'./test/rnd_shuffled{i}.png', **plt_args)

    ## count how often random_fit fails to fit boxes into [cont_sizes] bins
    # cont_sizes = [3, 4, 5]
    # fails = {k:0 for k in cont_sizes}
    # import time
    # ntimes = 1000
    # for cs in cont_sizes:
    #     for i in range(ntimes):
    #         random.seed(time.time_ns())
    #         conts, _ = random_fit(rcts_shuffled, n_cont=cs)
    #         if conts == -1:
    #             fails[cs] = fails[cs] + 1
    # print(fails)

    print(
        "Space left\n",
        f"rnd: {space_left_rnd}, sum={sum(space_left_rnd)}\n",
        f"mr:  {space_left_mr}\n",
        f"ff:  {space_left_ff}\n",
        f"mrs:  {space_left_mrs}\n",
        f"ffd: {space_left_ffd}\n"
    )
    print(
        "Bad placements\n",
        f"rnd: {bad_placements_rnd}\n",
        f"mr:  {bad_placements_mr}\n",
        f"ff:  {bad_placements_ff}\n",
        f"mrs:  {bad_placements_mrs}\n",
        f"ffd: {bad_placements_ffd}\n"
    )

    ## plot for max rest
    # plot empty containers:
    # current_state = State([], [], [], make_new_container(cont_size))
    # current_state.rcts_open.append(rcts_sorted[0]) # else error when plotting
    # current_state.update_pnts_open()  # see what points are left
    # ranges = [(0, 10, 1), (0, 22, 2)]
    # for (_,b,i) in ranges:
    #     for j in range(b):
    #         current_state.plot(alpha=1., fname=f'./mr_vis/{j}_{i}.png')

    pass