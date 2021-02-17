from abc import ABC
from collections import namedtuple
from typing import List


class Variable:

    def __init__(self, line_num: int, name: str):
        self.line_num = line_num
        self.name = name

    def __repr__(self) -> str:
        return 'Variable({}, {})'.format(self.line_num, self.name)


class Statement(ABC):
    pass


class Assignment(Statement):

    def __init__(self, line_num: int, variable: Variable, string: str):
        self.line_num = line_num
        self.variable = variable
        self.string = string

    def __repr__(self) -> str:
        return 'Assignment({}, {}, {})'.format(self.line_num, self.variable, self.string)


class Print(Statement):

    def __init__(self, line_num: int, variable: Variable):
        self.line_num = line_num
        self.variable = variable

    def __repr__(self) -> str:
        return 'Print({}, {})'.format(self.line_num, self.variable)


class SourceCode:

    def __init__(self, line_num: int, statements: List[Statement]):
        self.line_num = line_num
        self.statements = statements

    def __repr__(self) -> str:
        return 'SourceCode({}, {})'.format(self.line_num, self.statements)


class Direction:
    direction_list = ('in', 'out')

    def __init__(self, direction):
        if direction.lower() not in self.direction_list:
            raise ValueError
        self.direction = direction

    def __repr__(self):
        return str(self.direction)

    def __eq__(self, other):
        return self.direction.lower() == other


class Type(Statement):
    type_list = ('integer', 'char')

    def __init__(self, type):
        if type.lower() not in self.type_list:
            raise ValueError
        self.type = type

    def __repr__(self):
        return 'Type {}'.format(self.type)


class Param(Statement):

    def __init__(self, lin_num: int, variable: Variable, type: Type, direction: Direction):
        self.lin_num = lin_num
        self.variable = variable
        self.type = type
        self.direction = direction

    def __repr__(self) -> str:
        return '{} {} {}'.format(self.variable, self.type, self.direction)


class Procedure(Statement):
    def __init__(self, lin_num: int, variable: Variable, params: List[Param]):
        self.lin_num = lin_num
        self.variable = variable
        self.params = params

    def __repr__(self) -> str:
        return 'Procedure {}({})'.format(self.variable, ','.join(str(self.params)))