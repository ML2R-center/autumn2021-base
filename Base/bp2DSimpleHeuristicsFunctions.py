from typing import Any, Tuple

from Base.bp2DBin import Bin
from Base.bp2DBox import Box
from Base.bp2DPnt import Point


def face_intersection(b1: Box, b2: Box) -> int:
    '''Check how much overlap the faces of two rectangles have.
    Return the overlap, as a face, or return None, if there is no face intersection.'''
    max = 0
    for f1 in b1.get_face_list():
        for f2 in b2.get_face_list():
            intersection = f1.intersect(f2)
            if intersection is not None:
                max += intersection.length()
    return max


def most_enclosed_position_in_bin(bin: Bin, box: Box) -> Tuple[int, Any]:
    '''Finds the most enclosed feasible position for box in bin.
    it returns the first open point with this property, i.e.
    it also tries to place as bottom left as possible'''
    pmax = None
    max = -1
    for p in bin.get_pnts_open():
        if bin.can_place_box_at_pnt(box, p):
            box.move(p)
            enclosure = face_intersection(box,
                                          bin.bounding_box)  # check for edge overlap with bounding box, ie if box is placed on side or in corner of bin
            # TODO extremely slow and assumes that remove_box does not fiddle with box.lr and keeps the place position
            for box_stored in bin.boxes_stored:
                enclosure += face_intersection(box, box_stored)
            if enclosure > max:
                max = enclosure
                pmax = p
    return max, pmax
