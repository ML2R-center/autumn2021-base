import Base.bp2DState
from Base.bp2DAction import State
from Base.bp2DSimpleHeuristics import first_fit, next_fit
from Base.bpReadWrite import ReadWrite
from Base.bp2DRct import Box
from Base.bpStateGenerators import random_state_generator, state_generator
from tut_heuristics import single_type_heuristic


def main():
    state = ReadWrite.read_state(path="test_instances/test_1_input")
    ReadWrite.write_state(path="test_instances/test_1_output", state=state)
    solution = single_type_heuristic(state, video=False)
    ReadWrite.write_state(path="test_instances/test_1_solution", state=solution)

    state = ReadWrite.read_state(path="test_instances/test_2_input")
    ReadWrite.write_state(path="test_instances/test_2_output", state=state)
    solution = single_type_heuristic(state, video=False)
    ReadWrite.write_state(path="test_instances/test_2_solution", state=solution)

    state = ReadWrite.read_state(path="test_instances/test_3_input")
    ReadWrite.write_state(path="test_instances/test_3_output", state=state)
    solution = single_type_heuristic(state, video=False)
    ReadWrite.write_state(path="test_instances/test_3_solution", state=solution)

    random_state = state_generator(path="test_instances/explicit_1_output", bin_size=(10, 10), box_list=[(1, (1, 10)), (1, (1, 9)), (1, (9, 1)), (1, (1, 8)), (1, (8, 1)), (1, (1, 7)), (1, (7, 1)), (1, (1, 6)), (1, (6, 6))], seed=10)
    heuristic_state = single_type_heuristic(random_state, video=True)
    ReadWrite.write_state(path="test_instances/explicit_1_solution", state=heuristic_state)

    random_state = random_state_generator(path="test_instances/random_1_output", bin_size=(10, 10))
    heuristic_state = single_type_heuristic(random_state, video=False)
    ReadWrite.write_state(path="test_instances/random_1_solution", state=heuristic_state)

    random_state = random_state_generator(path="test_instances/first_fit_1_output", bin_size=(10, 10), box_num=30000)
    heuristic_state = first_fit(random_state.boxes_open)
    ReadWrite.write_state(path="test_instances/first_fit_1_solution", state=heuristic_state)

    random_state = random_state_generator(path="test_instances/next_fit_1_output", bin_size=(10, 10), box_num=30000)
    heuristic_state = next_fit(random_state.boxes_open)
    ReadWrite.write_state(path="test_instances/next_fit_1_solution", state=heuristic_state)




if __name__ == '__main__':
    main()
