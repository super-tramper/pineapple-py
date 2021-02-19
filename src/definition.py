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
        return 'Direction({})'.format(self.direction)

    def __eq__(self, other):
        return self.direction.lower() == other


class Type(Statement):
    type_list = ('integer', 'char')

    def __init__(self, type):
        if type.lower() not in self.type_list:
            raise ValueError
        self.type = type

    def __repr__(self):
        return 'Type({})'.format(self.type)


class Param(Statement):

    def __init__(self, line_num: int, variable: Variable, type: Type, direction: Direction):
        self.line_num = line_num
        self.variable = variable
        self.type = type
        self.direction = direction

    def __repr__(self) -> str:
        return 'Param({},{},{})'.format(self.variable.name, self.type.type, self.direction.direction)


class Procedure(Statement):
    def __init__(self, line_num: int, variable: Variable, params: List[Param]):
        self.line_num = line_num
        self.variable = variable
        self.params = params

    def __repr__(self) -> str:
        return 'Procedure {}({})'.format(self.variable.name, self.params)


class VariableStatement(Statement):
    def __init__(self, line_num: int, variable: Variable, type: Type):
        self.line_num = line_num
        self.variable = variable
        self.type = type

    def __repr__(self):
        return 'Statement {} {}'.format(self.variable.name, self.type.type)


class Begin(Statement):
    def __init__(self, line_num):
        self.line_num = line_num

    def __repr__(self):
        return '{} BEGIN'.format(self.line_num)


class Execute(Statement):
    def __init__(self, line_num, sql):
        self.line_num = line_num
        self.sql = sql

    def __repr__(self):
        return '{} Execute {}'.format(self.line_num, self.sql)


class End(Statement):
    def __init__(self, line_num):
        self.line_num = line_num

    def __repr__(self):
        return '{} End'.format(self.line_num)


class Ignored(Statement):
    def __init__(self, line_num):
        self.line_num = line_num

    def __repr__(self):
        return '{} Ignored'.format(self.line_num)