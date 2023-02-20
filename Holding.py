from Predicate import Predicate
from PutDownOnTop import PutDownOnTop
from PickupOp import PickupOp


class Holding(Predicate):

    def __init__(self, X):
        self.X = X

    def __str__(self):
        return "Holding({X})".format(X=self.X)

    def __repr__(self):
        return self.__str__()

    def __lt__(self, other):
        if isinstance(other, self.__class__):
            return other.X is not None and self.X <= other.X

        from On import On
        from OnTable import OnTable
        from Clear import Clear
        if isinstance(other, On.__class__) or isinstance(other, OnTable.__class__) and isinstance(other, Clear.__class__):
            return True

        from ArmEmpty import ArmEmpty
        if isinstance(other, ArmEmpty.__class__):
            return False

    def __eq__(self, other):
        return self.__dict__ == other.__dict__ and self.__class__ == other.__class__

    def __hash__(self):
        return hash(str(self))

    def get_action(self, world_state):
        X = self.X
        # If block is on table, pick up
        from OnTable import OnTable
        if OnTable(X) in world_state:
            return PickupOp(X)
        # If block is on another block, unstack
        else:
            for predicate in world_state:
                from On import On
                if isinstance(predicate, On) and predicate.X == X:
                    return PutDownOnTop(X, predicate.Y)