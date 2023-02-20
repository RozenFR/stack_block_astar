from Predicate import Predicate
from Holding import Holding
from PutdownOp import PutdownOp


class ArmEmpty(Predicate):

    def __init__(self):
        self.X = None

    def __str__(self):
        return "ArmEmpty"

    def __repr__(self):
        return self.__str__()

    def __lt__(self, other):
        return True

    def __eq__(self, other):
        return self.__dict__ == other.__dict__ and self.__class__ == other.__class__

    def __hash__(self):
        return hash(str(self))

    def get_action(self, world_state=[]):
        for predicate in world_state:
            if isinstance(predicate, Holding):
                return PutdownOp(predicate.X)
        return None