import os

import Base.bp2DState
from Base.bp2DSimpleHeuristics import single_type_heuristic, first_fit, next_fit, most_enclosed_position, max_rest, \
    best_fit, first_fit_decreasing, next_fit_decreasing, get_all_heuristics
from Base.bp2DState import State
from Base.bpReadWrite import ReadWrite
from Base.bp2DBox import Box
from Base.bpStateGenerators import random_state_generator, state_generator


def main():
    if not os.path.exists("./vis"):
        os.mkdir("./vis")

    # Simple examples for read and write
    state = ReadWrite.read_state(path="test_instances/test_1_input")
    ReadWrite.write_state(path="test_instances/test_1_output", state=state)
    single_type_heuristic(state, heuristic_step=first_fit_decreasing)
    ReadWrite.write_state(path="test_instances/test_1_solution", state=state)

    state = ReadWrite.read_state(path="test_instances/test_1_input")
    solution = ReadWrite.read_state(path="test_instances/test_1_solution")

    #
    # state = ReadWrite.read_state(path="test_instances/test_2_input")
    # ReadWrite.write_state(path="test_instances/test_2_output", state=state)
    # solution = single_type_heuristic(state, video=False)
    # ReadWrite.write_state(path="test_instances/test_2_solution", state=solution)
    #
    # state = ReadWrite.read_state(path="test_instances/test_3_input")
    # ReadWrite.write_state(path="test_instances/test_3_output", state=state)
    # solution = single_type_heuristic(state, video=False)
    # ReadWrite.write_state(path="test_instances/test_3_solution", state=solution)

    # Comparison of heuristics on small state with boxes explicitely given
    state_generator(path="test_instances/state_small", bin_size=(10, 10),
                    box_list=[(1, (1, 10)), (1, (1, 9)), (1, (9, 1)), (1, (1, 8)), (1, (8, 1)),
                              (1, (1, 7)), (1, (7, 1)), (1, (1, 6)), (1, (6, 6))], seed=10)
    for name, heuristic in get_all_heuristics():
        state = ReadWrite.read_state("test_instances/state_small")
        single_type_heuristic(state, heuristic, plot_result=True, plot_name=name)
        ReadWrite.write_state(path=f"test_instances/solution_small_{name}", state=state)

        state = ReadWrite.read_state("test_instances/state_random_big")
        solution = ReadWrite.read_state(path=f"test_instances/solution_big_{name}")
        print(f"Is solution of {name} valid? {solution.is_valid(state)}!")

    # Comparison of heuristics on random state
    random_state_generator(path="test_instances/state_random_big", bin_size=(10, 10), box_width_min=2,
                           box_num=1000)
    for name, heuristic in get_all_heuristics():
        state = ReadWrite.read_state("test_instances/state_random_big")
        single_type_heuristic(state, heuristic)
        ReadWrite.write_state(path=f"test_instances/solution_big_{name}", state=state)

        state = ReadWrite.read_state("test_instances/state_random_big")
        solution = ReadWrite.read_state(path=f"test_instances/solution_big_{name}")
        print(f"Is solution of {name} valid? {solution.is_valid(state)}!")

if __name__ == '__main__':
    main()
