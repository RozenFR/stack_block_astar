from Predicate import Predicate
from PutDownOp import PutdownOp


# Predicate OnTable defining block X is on the table
# NOTE : OnTable is not compatible with On
# Example : On(X, Y), X can't be on the table
class OnTable(Predicate):
    def __init__(self, X):
        self.X = X

    def __str__(self):
        return "OnTable({X})".format(X=self.X)

    def __repr__(self):
        return self.__str__()

    def __lt__(self, other):
        if isinstance(other, self.__class__):
            return other.X is not None and self.X <= other.X

        from Clear import Clear
        if isinstance(other, Clear.__class__):
            return True

        from Holding import Holding
        from ArmEmpty import ArmEmpty
        from On import On
        if isinstance(other, Holding.__class__) or isinstance(other, ArmEmpty.__class__) \
                or isinstance(other, On.__class__):
            return False

    def __eq__(self, other):
        return self.__dict__ == other.__dict__ and self.__class__ == other.__class__

    def __hash__(self):
        return hash(str(self))
