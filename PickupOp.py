from Operation import Operation


# Class representing
class PickupOp(Operation):
    def __init__(self, X):
        self.X = X

    def __str__(self):
        return "PickUp({X})".format(X=self.X)

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return self.__dict__ == other.__dict__ and self.__class__ == other.__class__

    def precondition(self):
        from Clear import Clear
        from OnTable import OnTable
        from ArmEmpty import ArmEmpty
        return [Clear(self.X), OnTable(self.X), ArmEmpty()]

    def delete(self):
        from ArmEmpty import ArmEmpty
        from OnTable import OnTable
        return [ArmEmpty(), OnTable(self.X)]

    def add(self):
        from Holding import Holding
        return [Holding(self.X)]
