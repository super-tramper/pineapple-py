import sys

from src.definition import Variable, Statement, Assignment, Print, SourceCode, Procedure
from src.lexer import Lexer
from src.parser import parse


class Interpreter:

    def __init__(self, source_code: str):
        self.lexer = Lexer(source_code)
        self.ast = parse(self.lexer)
        self.variables = {}
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

    def parse(self, statement: Statement):
        if isinstance(statement, Procedure):
            return self.parse_procedure(statement)

    def parse_procedure(self, procedure: Procedure):
        params = [i.variable.name for i in procedure.params if i.direction.direction == 'in']
        return 'def {}({}):\n'.format(procedure.variable.name, ' ,'.join(params))

    def resolve_source_code(self, ast: SourceCode) -> None:
        with open('./out.py', 'w') as f:
            for statement in ast.statements:
                self.resolve_statement(statement)
                f.write(self.parse(statement))

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
