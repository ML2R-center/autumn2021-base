import random
from typing import Tuple, List

import numpy.random

from Base.bp2DState import State
from Base.bp2DBox import Box
from Base.bpReadWrite import ReadWrite
from Base.bp2DPnt import Point


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

'''
Generates a random dataset by recursively dividing boxes. The returned state contains already packed boxes. 
A peeling process removes margins of randomly selected boxes to leave a little wiggle room. 
Example call >>> sliced_box_state_generator((10,10), bin_num=8, box_num=100, peel_area=100)
'''
def sliced_box_state_generator(bin_size: Tuple[int, int], bin_num: int=1, box_num: int = 100, 
                                peel_area: int = 0, peel_margin: int = 1,
                                box_width_min: int = 1, box_width_max: int = 4, 
                                box_height_min: int = 1, box_height_max: int = 4, 
                                path: str = None, seed: int = 0):
    state = State(0, bin_size, [])
    random.seed(seed)

    boxes = []
    for i in range(bin_num): 
        box = Box(bin_size[0], bin_size[1])
        emb = (i,(0,0))
        sdir = random.randint(0,1) # slice direction
        boxes.append((box, emb, sdir))
        state.open_new_bin()
    
    while len(boxes) < box_num:
        box, emb, sdir = boxes.pop(0)
        # cut direction = width
        if sdir == 0:
            if box.w < box_width_min*2: boxes.append((box, emb, sdir))
            else:
                cut_pos = random.randint(box_width_min, box.w-box_width_min)
                boxes.append((Box(cut_pos, box.h), (emb[0], (emb[1][0], emb[1][1])), (sdir+1)%2))
                boxes.append((Box(box.w-cut_pos, box.h), (emb[0], (emb[1][0]+cut_pos, emb[1][1])), (sdir+1)%2))
        # cut direction = height
        else:
            if box.h < box_height_min*2: boxes.append((box, emb, sdir))
            else:
                cut_pos = random.randint(box_height_min, box.h-box_height_min)
                boxes.append((Box(box.w, cut_pos), (emb[0], (emb[1][0], emb[1][1])), (sdir+1)%2))
                boxes.append((Box(box.w, box.h-cut_pos), (emb[0], (emb[1][0], emb[1][1]+cut_pos)), (sdir+1)%2))
    
    # peel margins of boxes
    peeled = 0
    while peeled < peel_area:
        box, emb, sdir = random.choice(boxes)
        if random.randint(0, 1) == 0:
            if box.w >= peel_margin+1:
                box.w -= peel_margin
                peeled += box.h
        else:
            if box.h >= peel_margin+1:
                box.h -= peel_margin
                peeled += box.w

    # enumerate and assign boxes
    for i,(box,emb,sdir) in enumerate(boxes):
        box.n = i
        bin = emb[0]
        pos = Point(emb[1][0], emb[1][1])
        state.place_box_in_bin_at_pnt(box, bin, pos)
    
    if path is not None:
        ReadWrite.write_state(path, state)
    return state
