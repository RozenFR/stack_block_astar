from PickUpOnTopOp import PickUpOnTopOp
from Predicate import Predicate

# Predicate On defining bloc X is on top of Y
class On(Predicate):
    def __init__(self, X, Y):
        self.X = X
        self.Y = Y

    def __str__(self):
        return "On({X},{Y})".format(X=self.X, Y=self.Y)

    def __repr__(self):
        return self.__str__()

    def __lt__(self, other):

        if isinstance(other, self.__class__):
            return other.X is not None and self.X <= other.X

        from OnTable import OnTable
        from Clear import Clear
        if isinstance(other, OnTable.__class__) or isinstance(other, Clear.__class__):
            return True

        from Holding import Holding
        from ArmEmpty import ArmEmpty
        if isinstance(other, Holding.__class__) or isinstance(other, ArmEmpty.__class__):
            return False

    def __eq__(self, other):
        return self.__dict__ == other.__dict__ and self.__class__ == other.__class__

    def __hash__(self):
        return hash(str(self))
