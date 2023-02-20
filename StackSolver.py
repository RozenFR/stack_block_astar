from ArmEmpty import ArmEmpty
from Clear import Clear
from Holding import Holding
from On import On
from OnTable import OnTable
from PickupOp import PickupOp
from PutdownOp import PutdownOp
from PutDownOnTop import PutDownOnTop


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
        self.fscore = fscore  # total cost + heuristic
        self.previousNode = prevNode
        self.links = links  # List of neighbors of node

    def __eq__(self, other):
        return contains_in_list(self.data, other.data)

    def __str__(self):
        return "NodeSearch({data}, {g}, {h})".format(data=str(self.data), g=self.gscore, h=self.fscore)

    def __lt__(self, other):
        return self.fscore <= other.fscore


def contains_in_list(l1, l2):
    for i in l1:
        if i not in l2:
            return False
    return True


def not_contains_in_list(l1, l2):
    for i in l1:
        if i in l2:
            return False
    return True


def heuristic(node1: list, node2: list):
    count = 0
    for i in node1:
        if i in node2:
            count += 1
    return len(node2) - count


def cost(node1: NodeSearch = None, node2: NodeSearch = None):
    return 1


def is_goal_reached(current, goal):
    return current == goal


def select_min_h(open: [NodeSearch]):
    hlist = []
    fscore = open[0].fscore
    for i in open:
        if i.fscore == fscore:
            hlist.append(i)
    return hlist


class StackSolver:
    class AStar:
        def __init__(self, goal=None, elements=None):
            if goal is None:
                goal = list()
            if elements is None:
                elements = None
            self.goal = goal
            self.open = list()
            self.close = list()
            self.elements = elements # Necessary to search for neighbors

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

                for j in self.elements:
                    if i != j:
                        # PickOnTop
                        # Case Where : On(X,Y) and Clear(X) and ArmEmpty() -> Holding(X) and Clear(Y)
                        if contains_in_list([ArmEmpty(), On(i, j), Clear(i)], node.data):
                            tempData3 = node.data.copy()
                            tempData3.remove(ArmEmpty())
                            tempData3.remove(On(i, j))
                            tempData3.remove(Clear(i))
                            tempData3.append(Holding(i))
                            tempData3.append(Clear(j))
                            node3 = NodeSearch(data=tempData3, opera=PutDownOnTop(i, j), gscore=(gscore + cost()),
                                              fscore=heuristic(tempData3, self.goal), prevNode=node)
                            neighbors.append(node3)

                        # PutDownOnTop
                        # Case Where : Holding(X) and Clear(Y) -> On(X,Y) and Clear(X) and ArmEmpty()
                        if contains_in_list([Holding(i), Clear(j)], node.data):
                            tempData4 = node.data.copy()
                            tempData4.remove(Holding(i))
                            tempData4.remove(Clear(j))
                            tempData4.append(ArmEmpty())
                            tempData4.append(On(i, j))
                            tempData4.append(Clear(i))
                            node4 = NodeSearch(data=tempData4, opera=PutDownOnTop(i, j), gscore=(gscore + cost()),
                                              fscore=heuristic(tempData4, self.goal), prevNode=node)
                            neighbors.append(node4)
            return neighbors

        def get_path_operation(self, start: list, goal: list):

            # We setup the first node
            startNode = NodeSearch(data=start, gscore=0, fscore=heuristic(start, goal))
            self.open.append(startNode)

            while True:
                for cnode in self.close:
                    if cnode.fscore == 0:
                        finalNode = cnode
                        operator = []
                        while finalNode.previousNode is not None:
                            operator.insert(0, finalNode.opera)
                            finalNode = finalNode.previousNode
                        return operator

                if not self.open:
                    raise InterruptedError
                else:
                    closeNode = self.open[0]
                    self.open.pop(0)
                    self.close.append(closeNode)
                    closeNode.links = self.neighbors(closeNode)
                    for np in closeNode.links:
                        if np not in self.open and np not in self.close:
                            self.open.append(np)
                        else:
                            if np in self.open or np in self.close:
                                inOpen = True if np in self.open else False
                                index = self.open.index(np) if inOpen else self.close.index(np)
                                cnode = self.open[index] if inOpen else self.close[index]
                                if cnode.gscore > np.gscore:
                                    if inOpen:
                                        self.open.remove(cnode)
                                        self.open.append(np)
                                    else:
                                        self.close.remove(cnode)
                                        self.open.append(cnode)
                        self.open.sort()