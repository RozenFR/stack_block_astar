from ArmEmpty import ArmEmpty
from Clear import Clear
from Holding import Holding
from On import On
from OnTable import OnTable
from PickUpOnTopOp import PickUpOnTopOp
from PickupOp import PickupOp
from PutDownOnTopOp import PutDownOnTopOp
from PutDownOp import PutdownOp

# NodeSearch is a class representing a node for A*
class NodeSearch:
    def __init__(self, data=None, opera=None, gscore=0, fscore=0, prevNode=None, links=None):
        if opera is None:
            opera = []
        if data is None:
            data = []
        if links is None:
            links = []
        self.data = data  # contains a list of all predicate on state
        self.opera = opera  # Contains operation applied on node
        self.gscore = gscore  # total cost of node
        self.fscore = fscore  # heuristic
        self.previousNode = prevNode
        self.links = links  # List of neighbors of node

    def __eq__(self, other):
        return contains_in_list(self.data, other.data)

    def __str__(self):
        return "NodeSearch({data}, {g}, {h})".format(data=str(self.data), g=self.gscore, h=self.fscore)

    def __lt__(self, other):
        return self.fscore <= other.fscore


# Method to know if l1 is contained in l2
def contains_in_list(l1, l2):
    for i in l1:
        if i not in l2:
            return False
    return True


# Method to know if l1 is not contained in l2
def not_contains_in_list(l1, l2):
    for i in l1:
        if i in l2:
            return False
    return True


# Method defining A* heuristic
def heuristic(node1: list, node2: list):
    count = 0
    for i in node1:
        if i in node2:
            count += 1
    return len(node2) - count


# Method defining A* cost between 2 node
def cost(node1: NodeSearch = None, node2: NodeSearch = None):
    return 1


# Method to verify if goal is attained
def is_goal_reached(current, goal):
    return current == goal


# Main class to solve stacking problem
def heuristic2(node1, node2):
    count = 0
    for i in node1:
        if i in node2:
            count += 1
    return len(node2) + len(node1) - 2 * count


class StackSolver:
    # Class defining A*
    class AStar:
        def __init__(self, goal=None, elements=None):
            if goal is None:
                goal = list()
            if elements is None:
                elements = None
            self.goal = goal # Goal State
            self.open = list() # Open Node
            self.close = list() # Close Node
            self.elements = elements # Necessary to search for neighbors

        # Method returning a list of neighbors (i + 1) of node i
        def neighbors(self, node: NodeSearch):
            neighbors = []
            gscore = node.gscore
            # For each element verify if operation is available and if available add to
            for i in self.elements:
                # PickUpOnTable
                # Case where : EmptyArm and Clear(X) and OnTable(X) -> Holding(X)
                if contains_in_list([ArmEmpty(), Clear(i), OnTable(i)], node.data):
                    tempData1 = node.data.copy()
                    tempData1.remove(ArmEmpty())
                    tempData1.remove(Clear(i))
                    tempData1.remove(OnTable(i))
                    tempData1.append(Holding(i))
                    node1 = NodeSearch(data=tempData1, opera=PickupOp(i), gscore=(gscore + cost()),
                                      fscore=heuristic(tempData1, self.goal), prevNode=node)
                    neighbors.append(node1)

                # PutDownOnTable
                # Case where : Holding(X) -> AmrEmpty() and OnTable(i) and Clear(i)
                if contains_in_list([Holding(i)], node.data):
                    tempData2 = node.data.copy()
                    tempData2.remove(Holding(i))
                    tempData2.append(ArmEmpty())
                    tempData2.append(Clear(i))
                    tempData2.append(OnTable(i))
                    node2 = NodeSearch(data=tempData2, opera=PutdownOp(i), gscore=(gscore + cost()),
                                      fscore=heuristic(tempData2, self.goal), prevNode=node)
                    neighbors.append(node2)

                # Managing every operation with 2 variables
                for j in self.elements:
                    if i != j:
                        # PickUpOnTopOp
                        # Case Where : On(X,Y) and Clear(X) and ArmEmpty() -> Holding(X) and Clear(Y)
                        if contains_in_list([ArmEmpty(), On(i, j), Clear(i)], node.data):
                            tempData3 = node.data.copy()
                            tempData3.remove(ArmEmpty())
                            tempData3.remove(On(i, j))
                            tempData3.remove(Clear(i))
                            tempData3.append(Holding(i))
                            tempData3.append(Clear(j))
                            node3 = NodeSearch(data=tempData3, opera=PickUpOnTopOp(i, j), gscore=(gscore + cost()),
                                               fscore=heuristic(tempData3, self.goal), prevNode=node)
                            neighbors.append(node3)

                        # PutDownOnTopOp
                        # Case Where : Holding(X) and Clear(Y) -> On(X,Y) and Clear(X) and ArmEmpty()
                        if contains_in_list([Holding(i), Clear(j)], node.data):
                            tempData4 = node.data.copy()
                            tempData4.remove(Holding(i))
                            tempData4.remove(Clear(j))
                            tempData4.append(ArmEmpty())
                            tempData4.append(On(i, j))
                            tempData4.append(Clear(i))
                            node4 = NodeSearch(data=tempData4, opera=PutDownOnTopOp(i, j), gscore=(gscore + cost()),
                                              fscore=heuristic(tempData4, self.goal), prevNode=node)
                            neighbors.append(node4)
            return neighbors

        # Main method to solve stacking problem
        def get_path_operation(self, start: list, goal: list):

            # We setup the first node
            startNode = NodeSearch(data=start, gscore=0, fscore=heuristic(start, goal))
            self.open.append(startNode)

            # Infinit loop and only when there is nothing in open then we return an error
            while True:
                # Loop to verify if solution is in close
                for cnode in self.close:
                    if cnode.fscore == 0:
                        finalNode = cnode
                        operator = []
                        # Get previous node to get path of solution
                        while finalNode.previousNode is not None:
                            # We insert first because we go back through the node
                            operator.insert(0, finalNode.opera)
                            finalNode = finalNode.previousNode
                        return operator

                # Exception to A*
                if not self.open:
                    raise InterruptedError
                else:
                    # Getting 1st node of open
                    closeNode = self.open[0]
                    # Removing from open and add to close
                    self.open.pop(0)
                    self.close.append(closeNode)
                    # Get neighbors of node
                    closeNode.links = self.neighbors(closeNode)
                    # Loop through all neighbors
                    for np in closeNode.links:
                        # If node is not known then add to open
                        if np not in self.open and np not in self.close:
                            self.open.append(np)
                        else:
                            # if node is in open or close
                            if np in self.open or np in self.close:
                                inOpen = True if np in self.open else False
                                index = self.open.index(np) if inOpen else self.close.index(np)
                                cnode = self.open[index] if inOpen else self.close[index]
                                # if the cost of the new node is < to the one known
                                if cnode.gscore > np.gscore:
                                    # Replace with the new node
                                    if inOpen:
                                        self.open.remove(cnode)
                                        self.open.append(np)
                                    # remove from close and add to open
                                    else:
                                        self.close.remove(cnode)
                                        self.open.append(cnode)
                        # Sort open list by heuristic
                        self.open.sort()

    class AStar2:
        def __init__(self, goal=None, elements=None):
            if goal is None:
                goal = list()
            if elements is None:
                elements = None
            self.goal = goal # Goal State
            self.open = list() # Open Node
            self.close = list() # Close Node
            self.elements = elements # Necessary to search for neighbors

        # Method returning a list of neighbors (i + 1) of node i
        def neighbors(self, node: NodeSearch):
            neighbors = []
            gscore = node.gscore
            # For each element verify if operation is available and if available add to
            for i in self.elements:
                # PickUpOnTable
                # Case where : EmptyArm and Clear(X) and OnTable(X) -> Holding(X)
                if contains_in_list([ArmEmpty(), Clear(i), OnTable(i)], node.data):
                    tempData1 = node.data.copy()
                    tempData1.remove(ArmEmpty())
                    tempData1.remove(Clear(i))
                    tempData1.remove(OnTable(i))
                    tempData1.append(Holding(i))
                    node1 = NodeSearch(data=tempData1, opera=PickupOp(i), gscore=gscore + 4, prevNode=node)
                    node1.fscore = heuristic2(tempData1, self.goal)
                    neighbors.append(node1)

                # PutDownOnTable
                # Case where : Holding(X) -> AmrEmpty() and OnTable(i) and Clear(i)
                if contains_in_list([Holding(i)], node.data):
                    tempData2 = node.data.copy()
                    tempData2.remove(Holding(i))
                    tempData2.append(ArmEmpty())
                    tempData2.append(Clear(i))
                    tempData2.append(OnTable(i))
                    node2 = NodeSearch(data=tempData2, opera=PutdownOp(i), gscore=gscore + 4, prevNode=node)
                    node2.fscore = heuristic2(tempData2, self.goal)
                    neighbors.append(node2)

                # Managing every operation with 2 variables
                for j in self.elements:
                    if i != j:
                        # PickUpOnTopOp
                        # Case Where : On(X,Y) and Clear(X) and ArmEmpty() -> Holding(X) and Clear(Y)
                        if contains_in_list([ArmEmpty(), On(i, j), Clear(i)], node.data):
                            tempData3 = node.data.copy()
                            tempData3.remove(ArmEmpty())
                            tempData3.remove(On(i, j))
                            tempData3.remove(Clear(i))
                            tempData3.append(Holding(i))
                            tempData3.append(Clear(j))
                            node3 = NodeSearch(data=tempData3, opera=PickUpOnTopOp(i, j), gscore=gscore + 5, prevNode=node)
                            node3.fscore = heuristic2(tempData3, self.goal)
                            neighbors.append(node3)

                        # PutDownOnTopOp
                        # Case Where : Holding(X) and Clear(Y) -> On(X,Y) and Clear(X) and ArmEmpty()
                        if contains_in_list([Holding(i), Clear(j)], node.data):
                            tempData4 = node.data.copy()
                            tempData4.remove(Holding(i))
                            tempData4.remove(Clear(j))
                            tempData4.append(ArmEmpty())
                            tempData4.append(On(i, j))
                            tempData4.append(Clear(i))
                            node4 = NodeSearch(data=tempData4, opera=PutDownOnTopOp(i, j), gscore=gscore + 5, prevNode=node)
                            node4.fscore = heuristic2(tempData4, self.goal)
                            neighbors.append(node4)
            return neighbors

        # Main method to solve stacking problem
        def get_path_operation(self, start: list, goal: list):

            # We setup the first node
            startNode = NodeSearch(data=start, gscore=0, fscore=heuristic(start, goal))
            self.open.append(startNode)

            # Infinit loop and only when there is nothing in open then we return an error
            while True:
                # Loop to verify if solution is in close
                for cnode in self.close:
                    if cnode.fscore == 0:
                        finalNode = cnode
                        operator = []
                        # Get previous node to get path of solution
                        while finalNode.previousNode is not None:
                            # We insert first because we go back through the node
                            operator.insert(0, finalNode.opera)
                            finalNode = finalNode.previousNode
                        return operator

                # Exception to A*
                if not self.open:
                    raise InterruptedError
                else:
                    # Getting 1st node of open
                    closeNode = self.open[0]
                    # Removing from open and add to close
                    self.open.pop(0)
                    self.close.append(closeNode)
                    # Get neighbors of node
                    closeNode.links = self.neighbors(closeNode)
                    # Loop through all neighbors
                    for np in closeNode.links:
                        # If node is not known then add to open
                        if np not in self.open and np not in self.close:
                            self.open.append(np)
                        else:
                            # if node is in open or close
                            if np in self.open or np in self.close:
                                inOpen = True if np in self.open else False
                                index = self.open.index(np) if inOpen else self.close.index(np)
                                cnode = self.open[index] if inOpen else self.close[index]
                                # if the cost of the new node is < to the one known
                                if cnode.gscore > np.gscore:
                                    # Replace with the new node
                                    if inOpen:
                                        self.open.remove(cnode)
                                        self.open.append(np)
                                    # remove from close and add to open
                                    else:
                                        self.close.remove(cnode)
                                        self.open.append(cnode)
                        # Sort open list by heuristic
                        self.open.sort()