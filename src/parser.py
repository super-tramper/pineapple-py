import re
from typing import List

from src.definition import Variable, Statement, Assignment, Print, \
    SourceCode, Procedure, Param, Type, Direction, VariableStatement, \
    Begin, Execute, End, Ignored
from src.lexer import TokenType, Lexer, DIRECTION, TYPE


class ParseException(Exception):
    pass


def parse_ignored(lexer: Lexer) -> None:
    if lexer.look_ahead() == TokenType.TOKEN_IGNORED:
        lexer.next_token_is(TokenType.TOKEN_IGNORED)


def parse_comma(lexer: Lexer) -> None:
    if lexer.look_ahead() == TokenType.TOKEN_COMMA:
        lexer.next_token_is(TokenType.TOKEN_COMMA)


def parse_variable(lexer: Lexer) -> Variable:
    line_num = lexer.next_token_is(TokenType.TOKEN_VAR_PREFIX).line_num
    name = lexer.next_token_is(TokenType.TOKEN_NAME).token
    parse_ignored(lexer)
    return Variable(line_num, name)


def parse_variable2(lexer: Lexer) -> Variable:
    if lexer.look_ahead() == TokenType.TOKEN_NAME:
        token_info = lexer.next_token_is(TokenType.TOKEN_NAME)
        parse_ignored(lexer)
        return Variable(token_info.line_num, token_info.token)
    else:
        raise ParseException('parse_variable2(): unexpected direction {}'.format(lexer.look_ahead()))


def parse_string(lexer: Lexer) -> str:
    if lexer.look_ahead() == TokenType.TOKEN_DUOQUOTE:
        lexer.next_token_is(TokenType.TOKEN_DUOQUOTE)
        return ''
    if lexer.look_ahead() == TokenType.TOKEN_DUOSINGLEQUOTE:
        lexer.next_token_is(TokenType.TOKEN_DUOSINGLEQUOTE)
        return ''
    if lexer.look_ahead() == TokenType.TOKEN_SINGLEQUOTE:
        lexer.next_token_is(TokenType.TOKEN_SINGLEQUOTE)
        string = lexer.scan_before_token("'")
        lexer.next_token_is(TokenType.TOKEN_SINGLEQUOTE)
        return string
    lexer.next_token_is(TokenType.TOKEN_QUOTE)
    string = lexer.scan_before_token('"')
    lexer.next_token_is(TokenType.TOKEN_QUOTE)
    return string


def parse_assignment(lexer: Lexer) -> Assignment:
    var = parse_variable(lexer)
    parse_ignored(lexer)
    lexer.next_token_is(TokenType.TOKEN_EQUAL)
    parse_ignored(lexer)
    string = parse_string(lexer)
    parse_ignored(lexer)
    return Assignment(var.line_num, var, string)


def parse_assignment2(lexer: Lexer) -> Assignment:
    var = parse_variable2(lexer)
    parse_ignored(lexer)
    lexer.next_token_is(TokenType.TOKEN_COLON)
    lexer.next_token_is(TokenType.TOKEN_EQUAL)
    parse_ignored(lexer)
    string = parse_string(lexer)
    parse_ignored(lexer)
    return Assignment(var.line_num, var, string)


def parse_statement2(lexer: Lexer) -> Statement:
    """解析声明变量语句/变量赋值语句"""
    var = parse_variable2(lexer)
    parse_ignored(lexer)
    if lexer.look_ahead() in TYPE:
        type = parse_type(lexer)
        lexer.next_token_is(TokenType.TOKEN_SEMICOLON)
        parse_ignored(lexer)
        return VariableStatement(var.line_num, var, type)
    if lexer.look_ahead() == TokenType.TOKEN_COLON:
        lexer.next_token_is(TokenType.TOKEN_COLON)
        lexer.next_token_is(TokenType.TOKEN_EQUAL)
        string = parse_string(lexer)
        lexer.next_token_is(TokenType.TOKEN_SEMICOLON)
        parse_ignored(lexer)
        return Assignment(var.line_num, var, string)


def parse_print(lexer: Lexer) -> Print:
    line_num = lexer.next_token_is(TokenType.TOKEN_PRINT).line_num
    lexer.next_token_is(TokenType.TOKEN_LEFT_PAREN)
    parse_ignored(lexer)
    variable = parse_variable(lexer)
    parse_ignored(lexer)
    lexer.next_token_is(TokenType.TOKEN_RIGHT_PAREN)
    parse_ignored(lexer)
    return Print(line_num, variable)


def parse_procedure(lexer: Lexer) -> Procedure:
    lexer.next_token_is(TokenType.TOKEN_CREATE)
    parse_ignored(lexer)
    lexer.next_token_is(TokenType.TOKEN_OR)
    parse_ignored(lexer)
    lexer.next_token_is(TokenType.TOKEN_REPLACE)
    parse_ignored(lexer)
    lin_num = lexer.next_token_is(TokenType.TOKEN_PROCEDURE).line_num
    parse_ignored(lexer)
    variable = parse_variable2(lexer)
    parse_ignored(lexer)
    lexer.next_token_is(TokenType.TOKEN_LEFT_PAREN)
    params = parse_params(lexer)
    lexer.next_token_is(TokenType.TOKEN_RIGHT_PAREN)
    parse_ignored(lexer)
    # lexer.next_token_is(TokenType.TOKEN_COLON)
    lexer.next_token_is(TokenType.TOKEN_IS)
    parse_ignored(lexer)
    return Procedure(lin_num, variable, params)


def parse_params(lexer: Lexer) -> List[Param]:
    params = [parse_param(lexer)]
    while not lexer.next_source_code_is(')'):
        parse_comma(lexer)
        parse_ignored(lexer)
        params.append(parse_param(lexer))
    return params


# name type in/out
def parse_param(lexer: Lexer) -> Param:
    variable = parse_variable2(lexer)
    parse_ignored(lexer)
    type = parse_type(lexer)
    parse_ignored(lexer)
    directon = parse_direction(lexer)
    return Param(variable.line_num, variable, type, directon)


def parse_type(lexer: Lexer) -> Type:
    if lexer.look_ahead() == TokenType.TOKEN_INTEGER:
        type = lexer.next_token_is(TokenType.TOKEN_INTEGER).token
    elif lexer.look_ahead() == TokenType.TOKEN_CHAR:
        type = lexer.next_token_is(TokenType.TOKEN_CHAR).token
    else:
        raise ParseException('parse_direction(): unexpected type {}'.format(lexer.look_ahead()))
    return Type(type)


def parse_direction(lexer: Lexer) -> Direction:
    if lexer.look_ahead() == TokenType.TOKEN_IN:
        direction = lexer.next_token_is(TokenType.TOKEN_IN).token
    elif lexer.look_ahead() == TokenType.TOKEN_OUT:
        direction = lexer.next_token_is(TokenType.TOKEN_OUT).token
    else:
        raise ParseException('parse_direction(): unexpected direction {}'.format(lexer.look_ahead()))
    return Direction(direction)


def parse_begin(lexer: Lexer) -> Begin:
    line_num = lexer.next_token_is(TokenType.TOKEN_BEGIN).line_num
    return Begin(line_num)


def parse_execute(lexer: Lexer) -> Execute:
    line_num = lexer.next_token_is(TokenType.TOKEN_EXECUTE).line_num
    parse_ignored(lexer)
    lexer.next_token_is(TokenType.TOKEN_IMMEDIATE)
    parse_ignored(lexer)
    sql = parse_variable2(lexer)
    lexer.next_token_is(TokenType.TOKEN_SEMICOLON)
    parse_ignored(lexer)
    return Execute(line_num, sql)


def parse_end(lexer: Lexer) -> End:
    line_num = lexer.next_token_is(TokenType.TOKEN_END).line_num
    lexer.scan_before_token(';')
    lexer.next_token_is(TokenType.TOKEN_SEMICOLON)
    parse_ignored(lexer)
    return End(line_num)


def parse_statement(lexer: Lexer) -> Statement:
    if lexer.look_ahead() == TokenType.TOKEN_PRINT:
        return parse_print(lexer)
    if lexer.look_ahead() == TokenType.TOKEN_VAR_PREFIX:
        return parse_assignment(lexer)
    if lexer.look_ahead() == TokenType.TOKEN_CREATE:
        return parse_procedure(lexer)
    if lexer.look_ahead() == TokenType.TOKEN_NAME:
        return parse_statement2(lexer)
    if lexer.look_ahead() == TokenType.TOKEN_BEGIN:
        return parse_begin(lexer)
    if lexer.look_ahead() == TokenType.TOKEN_IGNORED:
        parse_ignored(lexer)
        return Ignored(lexer.line_num)
    if lexer.look_ahead() == TokenType.TOKEN_EXECUTE:
        return parse_execute(lexer)
    if lexer.look_ahead() == TokenType.TOKEN_END:
        return parse_end(lexer)
    raise ParseException('parse_statement(): unexpected token {}'.format(lexer.look_ahead()))


def parse(lexer: Lexer) -> SourceCode:
    statements = []
    line_num = lexer.line_num
    while lexer.look_ahead() != TokenType.TOKEN_EOF:
        statements.append(parse_statement(lexer))
    for i in statements:
        print(i)
    return SourceCode(line_num, statements)
