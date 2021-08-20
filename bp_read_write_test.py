import Base.bp2DState
from Base.bp2DAction import State
from Base.bpReadWrite import ReadWrite, random_state_generator
from Base.bp2DRct import Box


def main():
    state = ReadWrite.read_state(path="test_instances/test_boxes")
    ReadWrite.write_state(path="test_instances/test_write", state=state)
    state = ReadWrite.read_state(path="test_instances/test_write")

    state = ReadWrite.read_state(path="test_instances/test_boxes2")
    ReadWrite.write_state(path="test_instances/test_write2", state=state)
    state = ReadWrite.read_state(path="test_instances/test_write2")

    state = ReadWrite.read_state(path="test_instances/test_write2")
    ReadWrite.write_state(path="test_instances/test_write2", state=state)
    state = ReadWrite.read_state(path="test_instances/test_write2")

    state = ReadWrite.read_state(path="test_instances/test_boxes3")
    ReadWrite.write_state(path="test_instances/test_write3", state=state)
    state = ReadWrite.read_state(path="test_instances/test_write3")

    random_state_generator(path="test_instances/test_write4", bin_size=(10, 10))


if __name__ == '__main__':
    main()
