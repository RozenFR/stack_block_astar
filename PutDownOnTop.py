from Operation import Operation


class PutDownOnTop(Operation):

    def __init__(self, X, Y):
        self.X = X
        self.Y = Y

    def __str__(self):
        return "PutDownOnTop({X},{Y})".format(X=self.X, Y=self.Y)

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return self.__dict__ == other.__dict__ and self.__class__ == other.__class__

    def precondition(self):
        from ArmEmpty import ArmEmpty
        from On import On
        from Clear import Clear
        return {ArmEmpty(), On(X=self.X, Y=self.Y), Clear(X=self.X)}

    def delete(self):
        from ArmEmpty import ArmEmpty
        from On import On
        return [ArmEmpty(), On(X=self.X, Y=self.Y)]

    def add(self):
        from Clear import Clear
        from Holding import Holding
        return [Clear(X=self.Y), Holding(X=self.X)]