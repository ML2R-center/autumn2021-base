import os

from Base.bp2DData import *
from Base.bp2DPlot import *

from Base.bp2DSimpleHeuristics import first_fit, first_fit_decreasing, next_fit, next_fit_decreasing, \
    best_fit, best_fit_decreasing, random_fit, max_rest

from Base.bpStateGenerators import *

from Base.bpUtil import *


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
    rects1 = sort_boxes(rects1)
    rs1 = name_rectangles(rects1)
    if squares_only:
        rects2 = make_rects([
            [5, 0, 0], [2, 5, 0], [1, 9, 0], [1, 9, 1], [2, 7, 0],
            [5, 5, 2], [3, 0, 5], [2, 3, 5], [1, 3, 7],
            [2, 0, 8], [2, 2, 8], [3, 4, 7], [3, 7, 7]
        ])
        rects2 = sort_boxes(rects2)
        rs2 = name_rectangles(rects2)
    else:
        rs2 = example5()
    return rs1, rs2, cont_size


def make_new_container(cont_size):
    return Box(cont_size, cont_size)


def get_random_set(n_items=500):
    random_state = random_state_generator(path="test_instances/random_1_output", bin_size=(10, 10), box_num=n_items)
    return random_state.boxes_open

if __name__ == '__main__':

    random.seed(666)

    # squares_only = False
    # r1, r2, cont_size = example_blog(squares_only=squares_only)
    # rcts = r1+r2#+r1.copy()+r1.copy()+r1.copy()+r1.copy()+r1.copy()+r1.copy()+r1.copy()+r1.copy()+r1.copy()+r1.copy()
    # name_rectangles(rcts)
    # np.random.shuffle(rcts)

    rcts = get_random_set(1000)
    print(f"n_items = {len(rcts)}")
    heuristics = [random_fit, first_fit, first_fit_decreasing,
                  next_fit, next_fit_decreasing,
                  best_fit, best_fit_decreasing,
                  max_rest
                  ]
    names = ["rand", "ff", "ffd", "nf", "nfd", "bf", "bfd", "mr"]

    if not os.path.exists("./vis"):
        os.mkdir("./vis")

    s = first_fit(rcts.copy())
    # plot_states_on_single_image(s.bins, alpha=1., ncols=5)
    plot_states(s.bins)

    # for h, n in zip(heuristics, names):
    #     print(f"running {n}")
    #     s = h(rcts.copy())
    #     plot_states(s)
    #     for i, bin in enumerate(s.bins):
    #         plot_packing_state(bin, bin.boxes_stored,
    #                            pnts_open=bin.pnts_open,
    #                            fname=f"./vis/{n}_{i}.png", alpha=1.)