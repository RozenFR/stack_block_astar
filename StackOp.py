from Operation import Operation


class StackOp(Operation):
    def __init__(self, X, Y):
        self.X = X
        self.Y = Y

    def __str__(self):
        return "Stack({X},{Y})".format(X=self.X, Y=self.Y)

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return self.__dict__ == other.__dict__ and self.__class__ == other.__class__

    def precondition(self):
        from Clear import Clear
        from Holding import Holding
        return [Clear(X=self.Y), Holding(X=self.X)]

    def delete(self):
        from Clear import Clear
        from Holding import Holding
        return [Clear(X=self.Y), Holding(X=self.X)]

    def add(self):
        from ArmEmpty import ArmEmpty
        from On import On
        return [ArmEmpty(), On(X=self.X, Y=self.Y)]