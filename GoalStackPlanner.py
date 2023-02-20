from ArmEmpty import ArmEmpty
from Clear import Clear
from Holding import Holding
from On import On
from OnTable import OnTable
from PickupOp import PickupOp
from PutdownOp import PutdownOp
from StackOp import StackOp
from PutDownOnTop import PutDownOnTop


def isPredicate(obj):
    predicates = [On, OnTable, Clear, Holding, ArmEmpty]
    for predicate in predicates:
        if isinstance(obj, predicate):
            return True
    return False


def isOperation(obj):
    operations = [StackOp, PutDownOnTop, PickupOp, PutdownOp]
    for operation in operations:
        if isinstance(obj, operation):
            return True
    return False


def arm_status(world_state):
    for predicate in world_state:
        if isinstance(predicate, Holding):
            return predicate
    return ArmEmpty()


class GoalStackPlanner:

    def __init__(self, initial_state, goal_state):
        self.initial_state = initial_state
        self.goal_state = goal_state

    def get_steps(self):

        # Store Steps
        steps = []

        # Program Stack
        stack = []

        # World State/Knowledge Base
        world_state = self.initial_state.copy()

        # Initially push the goal_state as compound goal onto the stack
        stack.append(self.goal_state.copy())
        print(stack)

        # Repeat until the stack is empty
        while len(stack) != 0:

            # Get the top of the stack
            stack_top = stack[-1]

            # If Stack Top is Compound Goal, push its unsatisfied goals onto stack
            if type(stack_top) is list:
                compound_goal = stack.pop()
                for goal in compound_goal:
                    if goal not in world_state:
                        stack.append(goal)

            # If Stack Top is an action
            elif isOperation(stack_top):
                # Peek the operation
                operation = stack[-1]

                all_preconditions_satisfied = True

                # Check if any precondition is unsatisfied and push it onto program stack
                for predicate in operation.delete():
                    if predicate not in world_state:
                        all_preconditions_satisfied = False
                        stack.append(predicate)

                # If all preconditions are satisfied, pop operation from stack and execute it
                if all_preconditions_satisfied:

                    stack.pop()
                    steps.append(operation)

                    for predicate in operation.delete():
                        world_state.remove(predicate)
                    for predicate in operation.add():
                        world_state.append(predicate)


            # If Stack Top is a single satisfied goal
            elif stack_top in world_state:
                stack.pop()

            # If Stack Top is a single unsatisfied goal
            else:
                unsatisfied_goal = stack.pop()

                # Replace Unsatisfied Goal with an action that can complete it
                action = unsatisfied_goal.get_action(world_state)

                stack.append(action)
                # Push Precondition on the stack
                for predicate in action.precondition():
                    if predicate not in world_state:
                        stack.append(predicate)

        return steps
