from ArmEmpty import ArmEmpty
from Clear import Clear
from On import On
from OnTable import OnTable
from StackSolver import StackSolver

if __name__ == '__main__':
    elements = ['A', 'B', 'C']

    initial_state = [
        On('C', 'A'),
        OnTable('A'), OnTable('B'),
        Clear('B'), Clear('C'),
        ArmEmpty()
    ]

    goal_state = [
        On('A', 'B'), On('B', 'C'),
        OnTable('C'),
        Clear('A'),
        ArmEmpty()
    ]

    print("============= Algorithme A* =============")
    elements.sort()
    initial_state.sort()
    goal_state.sort()
    stackSolver = StackSolver.AStar(goal=goal_state, elements=elements)
    operatorPath = stackSolver.get_path_operation(initial_state, goal_state)
    output = "Chemin Algorithme A* : "
    for i in operatorPath:
        print(str(i))
