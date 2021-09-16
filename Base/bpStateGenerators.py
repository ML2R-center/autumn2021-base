import random
from typing import Tuple, List

import numpy.random

from Base.bp2DState import State
from Base.bp2DBox import Box
from Base.bpReadWrite import ReadWrite


def state_generator(bin_size: Tuple[int, int], box_list: List[Tuple[int, Tuple[int, int]]], path: str = None, seed: int = 0):
    random.seed(seed)

    state = State(0, bin_size, [])
    state.open_new_bin()
    counter = 0
    for number, box_dims in box_list:
        for _ in range(number):
            state.boxes_open.append(Box(box_dims[0], box_dims[1], n=counter))
            counter += 1
    random.shuffle(state.boxes_open)

    if path is not None:
        ReadWrite.write_state(path, state)
    return state


def random_state_generator(bin_size: Tuple[int, int], box_num: int = 100, box_width_min: int = 1,
                           box_width_max: int = 4,
                           box_height_min: int = 1, box_height_max: int = 4, path: str = None, seed: int = 0):
    state = State(0, bin_size, [])
    state.open_new_bin()
    random.seed(seed)
    for i in range(box_num):
        width = random.randint(box_width_min, box_width_max)
        height = random.randint(box_height_min, box_height_max)
        state.boxes_open.append(Box(width, height, n=i))

    if path is not None:
        ReadWrite.write_state(path, state)
    return state
