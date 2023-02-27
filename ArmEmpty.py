from Predicate import Predicate
from Holding import Holding
from PutDownOp import PutdownOp


# Predicate ArmEmpty defining when robot's arm is empty
# NOTE : ArmEmpty can't be in encoding if Holding(X) because contradiction
class ArmEmpty(Predicate):

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