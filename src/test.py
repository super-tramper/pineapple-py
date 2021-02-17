class Human():
    pass


class Person(Human):
    pass


a = Person()
print(isinstance(a, Human))

class test:
    def __init__(self, directoin):
        self.direction = directoin

    def __repr__(self):
        return 'in'

    def __eq__(self, other):
        return self.direction == other

t = test('out')
print(t=='out')