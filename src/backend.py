import sys

from src.definition import Variable, Statement, Assignment, Print, SourceCode, \
    Procedure, VariableStatement, Ignored, Begin, Execute, End
from src.lexer import Lexer
from src.parser import parse


class Interpreter:

    def __init__(self, source_code: str):
        self.lexer = Lexer(source_code)
        self.ast = parse(self.lexer)
        self.variables = {}
        self.procedure = None
        self.begin = None
        self.assignment = []

    def resolve_print(self, print_statement: Print) -> None:
        print(self.variables[print_statement.variable.name])

    def resolve_assignment(self, assignment: Assignment) -> None:
        self.variables[assignment.variable.name] = assignment.string

    def resolve_procedure(self, procedure_statement: Procedure) -> None:
        self.procedure = procedure_statement

    def resolve_variableStatement(self, variableStatement: VariableStatement) -> None:
        pass

    def resolve_begin(self, begin: Begin) -> None:
        self.begin = begin.line_num

    def resolve_statement(self, statement: Statement) -> None:
        if isinstance(statement, Print):
            self.resolve_print(statement)
        elif isinstance(statement, Assignment):
            self.resolve_assignment(statement)
        elif isinstance(statement, Procedure):
            self.resolve_procedure(statement)
        elif isinstance(statement, VariableStatement):
            self.resolve_variableStatement(statement)
        elif isinstance(statement, Execute):
            pass
        elif isinstance(statement, End):
            pass
        elif isinstance(statement, Begin):
            self.resolve_begin(statement)
        elif isinstance(statement, Ignored):
            pass
        else:
            raise RuntimeError(
                'resolve_statement(): unexpected statement type: {}'.format(statement))

    def parse(self, statement: Statement):
        if isinstance(statement, Procedure):
            return self.parse_procedure(statement)
        if isinstance(statement, VariableStatement):
            return self.parse_ignored(-1)
        if isinstance(statement, Begin):
            return self.parse_begin(statement)
        if isinstance(statement, VariableStatement):
            return
        if isinstance(statement, Assignment):
            return self.parse_assignment(statement)
        if isinstance(statement, Execute):
            return self.parse_execute(statement)
        if isinstance(statement, End):
            return self.parse_end(statement)
        if isinstance(statement, Ignored):
            return self.parse_ignored(statement)

    def parse_procedure(self, procedure: Procedure):
        params = [i.variable.name for i in procedure.params if i.direction.direction == 'in']
        return 'def {}({}):\n'.format(procedure.variable.name, ' ,'.join(params))

    def parse_begin(self, begin: Begin):
        self.begin = begin.line_num
        return ' '*4+'try:\n'

    def parse_assignment(self, assignment: Assignment):
        self.assignment.append(assignment)
        return ' '*8 + '{} = "{}"\n'.format(assignment.variable.name, assignment.string)

    def parse_execute(self, execute: Execute):
        return ' '*8 + 'conn.execute({})\n'.format(execute.sql.name)

    def parse_end(self, end: End):
        return ' '*4 + 'except Exception as e:\n'+' '*8+'logger.info(str(e))\n'

    def parse_ignored(self, ignored: int):
        return ''

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
