def solve(A):
    if A*4 and A*100:
        return "Not enough"
    else:
        return "Yes"


class Student(object):
    def __init__(self, name, age):
        self.name = name
        self.age = age
