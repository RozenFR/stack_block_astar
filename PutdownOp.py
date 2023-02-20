from Operation import Operation


class PutdownOp(Operation):

    def __init__(self, X):
        self.X = X

    def __str__(self):
        return "PutDownOnTable({X})".format(X=self.X)

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return self.__dict__ == other.__dict__ and self.__class__ == other.__class__

    def precondition(self):
        from Holding import Holding
        return [Holding(self.X)]

    def delete(self):
        from Holding import Holding
        return [Holding(self.X)]

    def add(self):
        from ArmEmpty import ArmEmpty
        from OnTable import OnTable
        from Clear import Clear
        return [ArmEmpty(), OnTable(self.X), Clear(self.X)]
