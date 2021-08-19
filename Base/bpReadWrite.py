import Base.bp2DRct
from Base.bp2DPnt import Point
from Base.bp2DState import Bin
from Base.bp2DRct import Box

#TODO needs correct State class

class ReadWrite:

    @staticmethod
    def read_state(path: str):
        state = State([], [], [], None)
        with open(path, "r") as file:
            lines = file.readlines()
            for line in lines:
                values = line.strip().split(' ')
                if len(values) == 2:
                    width, height = values
                    state.unused.append(Box(int(width), int(height)))
                elif len(values) == 7:
                    width, height, box_x, box_y, bin_w, bin_h, bin_id = values
                    while len(state.bins) < bin_id + 1:
                        state.bins.append(Bin([], [], [], Box(bin_w, bin_h)))
                    state.bins[bin_id].rcts_clsd.append(Box(int(width), int(height), Point(int(box_x), int(box_y))))
                else:
                    raise IOError(
                        f'Wrong format of line: \n\t {line} should be of format: \n\t box_width box_height box_x box_y bin_width bin_height bin_id \n\t or \n\t box_width box_height')
        # TODO check if file gives valid placement!
        for bin in state.bins:
            bin.update_pnts_open()

    @staticmethod
    def write_state(path: str, state: State):
        with open(path, "w") as file:
            for i, bin in enumerate(state.bins):
                for box in bin.rcts_clsd:
                    file.writelines(
                        f'{box.get_w()} {box.get_h()} {box.get_corner().get_x()} {box.get_corner().get_y()} {bin.box.get_w()} {bin.box.get_h()} {i}\n')
            for box in state.unused:
                file.writelines(f'{box.get_w()} {box.get_h()}')
