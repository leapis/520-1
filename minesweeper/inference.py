class Fact:

    def __init__(self, value, unknowns):
        self.value = value
        self.unknowns = set(unknowns)
        self.operator = '='
    
    def add_unknown(self, unknown):
        self.unknowns.add(unknown)
    
    def get_unknowns(self):
        """Return set of unknowns"""
        return self.unknowns

    def get_value(self):
        return self.value

    def merge_subset(self, otherFact):
        otherFactUnknowns = otherFact.get_unknowns()
        otherFactValue = otherFact.get_value()
        if not otherFactUnknowns.issubset(self.unknowns): return False, (None)
        elif len(self.unknowns) == len(otherFactUnknowns): return False, (None)
        else:
            return True, Fact(self.value - otherFactValue, self.unknowns.difference(otherFactUnknowns))

    def is_solved_zero(self):
        if self.value == 0: return True #if the value is zero, then everything in unknowns must be safe
        return False

    def is_solved_atomic(self):
        if len(self.unknowns) == 1: return True #if there's one unknown left, then we know it's solved
        return False

    def is_equal_to(self, newFact):
        if len(self.unknowns) == len(newFact.unknowns) and self.unknowns.difference(newFact.unknowns) == set():
            assert (newFact.value == self.value), """INCONSISTENT FACTS: {val1}: {set1}, {val2}: {set2}""".format(val1=self.value, set1=str(self.unknowns), val2=newFact.value, set2 = str(newFact.unknowns))
            return True
        return False