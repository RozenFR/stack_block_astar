from Operation import Operation


# Operation pick up on top defining relation which define
# robot's arm is picking block
class PickUpOnTopOp(Operation):
    def __init__(self, X, Y):
        self.X = X
        self.Y = Y

    def __str__(self):
        return "PickUpOnTop({X},{Y})".format(X=self.X, Y=self.Y)

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return self.__dict__ == other.__dict__ and self.__class__ == other.__class__
