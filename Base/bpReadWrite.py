import random

from typing import Tuple

from Base.bp2DState import State
from Base.bp2DPnt import Point
from Base.bp2DBin import Bin
from Base.bp2DBox import Box


class ReadWrite:

    @staticmethod
    def read_state(path: str):
        """
        Read a state of bins, boxes in the bins and unused boxes from some file
        @param path: path to the file
        """
        state = State(0, (0, 0), [])
        n = 0
        with open(path, "r") as file:
            first_line = True
            line_counter = 0
            bin_width = 0
            bin_height = 0
            lines = file.readlines()
            for line in lines:
                line_counter += 1
                values = line.strip().split(' ')
                # Ignore comments in the file
                if values[0] != "%":
                    # bin size is in the first line
                    if first_line:
                        if len(values) == 2:
                            bin_width, bin_height = values
                            try:
                                bin_width = int(bin_width)
                            except ValueError:
                                print(f'File is not valid, in line {line_counter} {width} cannot be converted to int!')
                            try:
                                bin_height = int(bin_height)
                            except ValueError:
                                print(f'File is not valid, in line {line_counter} {height} cannot be converted to int!')
                            state.bin_size = (bin_width, bin_height)
                            state.open_new_bin()
                        else:
                            raise IOError(f'Wrong format of first line: \n\t {line} should be of format: \n\t bin_width'
                                          f'bin_height')
                        first_line = False
                    else:
                        if len(values) == 2:
                            width, height = values
                            try:
                                width = int(width)
                            except ValueError:
                                print(f'File is not valid, in line {line_counter} {width} cannot be converted to int!')
                            try:
                                height = int(height)
                            except ValueError:
                                print(f'File is not valid, in line {line_counter} {height} cannot be converted to int!')
                            state.boxes_open.append(Box(width, height, n=n))
                            n += 1
                        elif len(values) == 5:
                            width, height, box_x, box_y, bin_id = values
                            while len(state.bins) < int(bin_id) + 1:
                                state.bins.append(Bin(bin_width, bin_height))
                            validation = state.bins[int(bin_id)].place_box_at_pnt(
                                Box(int(width), int(height), n=n), Point(int(box_x), int(box_y)))
                            n += 1
                            if not validation:
                                raise IOError(
                                    f'File contains no valid configuration, in line {line_counter} the box in bin {bin_id} with size {(width, height)} and position {(box_x, box_y)} is overlapping with some other box.')
                        else:
                            raise IOError(f'Wrong format of line {line_counter} should be of format: \n\t box_width '
                                          f'box_height box_x box_y bin_width bin_height bin_id \n\t or \n\t box_width '
                                          f'box_height')
        return state

    @staticmethod
    def write_state(path: str, state: State, comments: dict = None):
        """
        Write some state of bins, boxes in the bins and unused boxes to some file
        @param path: target path for the file
        @param state: input state
        @param comments: dictionary of description, value pairs to comment the file
        """
        with open(path, "w") as file:
            # Write some comments about state and bins
            if type(comments) == dict:
                pass
            else:
                comments = default_comments(state)
            file.write(f'% State of a bin packing problem:\n%\n')
            for key, values in comments.items():
                file.write(f'% {key}: {values}\n')
            file.write(f'%\n% Bin size:\n')
            file.write(f'{state.bin_size[0]} {state.bin_size[1]}\n')
            file.write(f'%\n% Boxes (width, height) not in some bins:\n')
            for box in state.boxes_open:
                file.write(f'{box.get_w()} {box.get_h()}\n')
            file.write(f'%\n% Boxes (width, height, x_position, y_position, bin_id) in bins:\n')
            for i, bin in enumerate(state.bins):
                for box in bin.boxes_stored:
                    file.write(
                        f'{box.get_w()} {box.get_h()} {box.get_corner("bl").get_x()} {box.get_corner("bl").get_y()} {i}\n')


def default_comments(state: State):
    uncovered_points = 0
    covered_points = 0
    box_num = len(state.boxes_open)
    for bin in state.bins:
        uncovered_points += bin.capacity_available()
        covered_points += bin.area - bin.capacity_available()
        box_num += len(bin.boxes_stored)
    return {"Bin number": len(state.bins), "Total uncovered points": uncovered_points,
            "Total covered points": covered_points, "Number of boxes": box_num,
            "Unused boxes": len(state.boxes_open),
            "Runtime": state.solution_runtime}



