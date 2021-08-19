import Base.bp2DState
from Base.bpReadWrite import ReadWrite
from Base.bp2DRct import Box

#TODO needs correct State class

def main():
    state = ReadWrite.read_state("data/test_boxes")
    ReadWrite.write_state(path="out/test_write", state=state)
    state = State([Box(1, 1), Box(2, 2), Box(3, 2)])
    ReadWrite.write_state(path="out/test_write", state=state)

if __name__ == '__main__':
    main()
