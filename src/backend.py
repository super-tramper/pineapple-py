import sys

from src.definition import Variable, Statement, Assignment, Print, SourceCode, Procedure
from src.lexer import Lexer
from src.parser import parse


class Interpreter:

    def __init__(self, source_code: str):
        print('l1')
        self.lexer = Lexer(source_code)
        print('l2')
        self.ast = parse(self.lexer)
        print('l3')
        self.variables = {}
        print('l4')
        self.procedure = None

    def resolve_print(self, print_statement: Print) -> None:
        print(self.variables[print_statement.variable.name])

    def resolve_assignment(self, assignment: Assignment) -> None:
        self.variables[assignment.variable.name] = assignment.string

    def resolve_procedure(self, procedure_statement: Procedure) -> None:
        self.procedure = procedure_statement

    def resolve_statement(self, statement: Statement) -> None:
        if isinstance(statement, Print):
            self.resolve_print(statement)
        elif isinstance(statement, Assignment):
            self.resolve_assignment(statement)
        elif isinstance(statement, Procedure):
            self.resolve_procedure(statement)
        else:
            raise RuntimeError(
                'resolve_statement(): unexpected statement type: {}'.format(statement))

    def resolve_source_code(self, ast: SourceCode) -> None:
        for statement in ast.statements:
            self.resolve_statement(statement)

    def execute(self) -> None:
        self.resolve_source_code(self.ast)


def main():
    source_file = './test.sql'
    with open(source_file) as f:
        source_code = f.read()
    interpreter = Interpreter(source_code)
    interpreter.execute()


if __name__ == '__main__':
    main()
