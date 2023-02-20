from Predicate import Predicate


class Clear(Predicate):
    def __init__(self, X):
        self.X = X

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

    def get_action(self, world_state):
        for predicate in world_state:
            # If Block is on another block, unstack
            from On import On
            if isinstance(predicate, On) and predicate.Y == self.X:
                from PutDownOnTop import PutDownOnTop
                return PutDownOnTop(X=predicate.X, Y=predicate.Y)
        return None