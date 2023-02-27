from Predicate import Predicate
from PutDownOnTopOp import PutDownOnTopOp


# Predicate Clear defining X block which is clear
# NOTE : On(X,Y), Y can't be Clear(Y) because X is on top of X so contradiction
class Clear(Predicate):
    def __init__(self, X):
        self.X = X # Block X

    def __str__(self):
        return "Clear({X})".format(X=self.X)

    def __repr__(self):
        return self.__str__()

    def __lt__(self, other):
        if isinstance(other, self.__class__):
            return other.X is not None and self.X <= other.X
        else:
            return False

    def __eq__(self, other):
        return self.__dict__ == other.__dict__ and self.__class__ == other.__class__

    def __hash__(self):
        return hash(str(self))