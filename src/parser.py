import re
from typing import List

from src.definition import Variable, Statement, Assignment, Print, SourceCode, Procedure, Param, Type, Direction
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
    lin_num = lexer.next_token_is(TokenType.TOKEN_PROCEDURE).line_num
    parse_ignored(lexer)
    variable = parse_variable2(lexer)
    parse_ignored(lexer)
    lexer.next_token_is(TokenType.TOKEN_LEFT_PAREN)
    params = parse_params(lexer)
    lexer.next_token_is(TokenType.TOKEN_RIGHT_PAREN)
    lexer.next_token_is(TokenType.TOKEN_COLON)
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


def parse_statement(lexer: Lexer) -> Statement:
    if lexer.look_ahead() == TokenType.TOKEN_PRINT:
        return parse_print(lexer)
    if lexer.look_ahead() == TokenType.TOKEN_VAR_PREFIX:
        return parse_assignment(lexer)
    if lexer.look_ahead() == TokenType.TOKEN_PROCEDURE:
        return parse_procedure(lexer)
    raise ParseException('parse_statement(): unexpected token {}'.format(lexer.look_ahead()))


def parse(lexer: Lexer) -> SourceCode:
    statements = []
    line_num = lexer.line_num
    while lexer.look_ahead() != TokenType.TOKEN_EOF:
        statements.append(parse_statement(lexer))
    procedure = statements[0]
    print(procedure)
    return SourceCode(line_num, statements)
