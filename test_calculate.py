#! /usr/bin/env python3.7
# Author: Nathaniel Rudenberg

# After writing this many test cases, I realized there are likely to be many more
# extremely specific cases that I just don't have enough remaining time available
# to test for.

# Tests for calculate.py

from calculate import *

def test_parse():
    input = "2+2"
    assert parse(input) == ['2', '+', '2']

def test_parse_decimal():
    input = "7+2.0"
    assert parse(input) == ['7', '+', '2.0']

def test_parse_decimal_no_leading_zero():
    input = ".25 * 7"
    assert parse(input) == ['.25', '*', '7']
    input = "-.32          /.5"
    assert parse(input) == ['-', '.32', '/', '.5']

def test_parse_lone_decimal_point():
    input = "4 * . - 2"
    assert parse(input) == False

def test_parse_decimal_with_two_or_more_dots():
    input = "7.0.3 + 5"
    assert parse(input) == False

def test_parse_decimal_with_trailing_dot():
    input = "7. + 5"
    assert parse(input) == False

def test_parse_with_spaces():
    input = "1 + 2"
    assert parse(input) == ['1', '+', '2']
    input = "0.32          /0.5"
    assert parse(input) == ['0.32', '/', '0.5']

def test_parse_single_item():
    input = "3"
    assert parse(input) == ['3']
    input = "+"
    assert parse(input) == ['+']
    input = "-"
    assert parse(input) == ['-']
    input = "*"
    assert parse(input) == ['*']
    input = "/"
    assert parse(input) == ['/']

def test_parse_null():
    assert parse(None) == False

def test_parse_empty_input():
    input = ""
    assert parse(input) == False

def test_parse_invalid_input():
    input = "19 + cinnamon"
    assert parse(input) == False

def test_getNumber_single_digit():
    input = "2+2"
    number, pos, invalidSyntax = getNumber(input, 0)
    assert number == '2' and invalidSyntax == False
    input = "2 + 2"
    number, pos, invalidSyntax = getNumber(input, 4)
    assert number == '2' and invalidSyntax == False
    input = "12/4+2"
    number, pos, invalidSyntax = getNumber(input, 3)
    assert number == '4' and invalidSyntax == False

def test_getNumber_multi_digit():
    input = "42 + 58"
    number, pos, invalidSyntax = getNumber(input, 0)
    assert number == '42' and invalidSyntax == False

def test_getNumber_float_no_leading_zero():
    input = ".42"
    number, pos, invalidSyntax = getNumber(input, 0)
    assert number == '.42' and invalidSyntax == False
    input = "42 + .42"
    number, pos, invalidSyntax = getNumber(input, 5)
    assert number == '.42' and invalidSyntax == False

def test_getNumber_multiple_decimal_points():
    input = "0.4.2"
    number, pos, invalidSyntax = getNumber(input, 0)
    assert number == '0' and invalidSyntax == True

def test_convertToPostfix_order_of_operations():
    expression = ['32', '-', '5', '+', '7', '*', '2', '-', '3', '+', '32', '/', '4']
    assert convertToPostfix(expression) == ['32', '5', '-', '7', '2', '*', '+', '3', '-', '32', '4', '/', '+']

def test_convertToPostfix_flat_parens():
    expression = ['2', '*', '(', '7', '+', '7', ')']
    assert convertToPostfix(expression) == ['2', '7', '7', '+', '*']

def test_convertToPostfix_nested_parens():
    expression = ['2', '+', '(', '(', '7', '-', '4', ')', ')', '-', '5']
    assert convertToPostfix(expression) == ['2', '7', '4', '-', '+', '5', '-']
    expression = ['2', '+', '(', '7', '-', '(', '6', '+', '4', ')', ')', '-', '5']
    assert convertToPostfix(expression) == ['2', '7', '6', '4', '+', '-', '+', '5', '-']
    expression = ['2', '+', '(', '7', '-', '(', '6', '+', '4', ')', '-', '2', ')', '-', '5']
    assert convertToPostfix(expression) == ['2', '7', '6', '4', '+', '-', '2', '-', '+', '5', '-']

def test_validateSyntax_three_ops_in_series():
    expression = ['32', '-', '5', '+', '7', '*', '2', '-', '3', '+', '32', '/', '-', '*', '4']
    assert validateSyntax(expression) == False
    expression = ['-', '-', '-', '5']
    assert validateSyntax(expression) == False
    expression = ['2', '+', '-', '+', '-', '4']
    assert validateSyntax(expression) == False

def test_validateSyntax_second_op_not_minus():
    # Second operation is "/"
    expression = ['3', '+', '32', '/', '/', '4']
    assert validateSyntax(expression) == False
    expression = ['3', '+', '32', '*', '/', '4']
    assert validateSyntax(expression) == False
    expression = ['3', '+', '32', '+', '/', '4']
    assert validateSyntax(expression) == False
    expression = ['3', '+', '32', '-', '/', '4']
    assert validateSyntax(expression) == False

    # Second operation is "*"
    expression = ['3', '+', '32', '/', '*', '4']
    assert validateSyntax(expression) == False
    expression = ['3', '+', '32', '+', '*', '4']
    assert validateSyntax(expression) == False
    expression = ['3', '+', '32', '*', '*', '4']
    assert validateSyntax(expression) == False
    expression = ['3', '+', '32', '-', '*', '4']
    assert validateSyntax(expression) == False

    # Second operation is "+"
    expression = ['3', '+', '32', '/', '+', '4']
    assert validateSyntax(expression) == False
    expression = ['3', '+', '32', '*', '+', '4']
    assert validateSyntax(expression) == False
    expression = ['3', '+', '32', '+', '+', '4']
    assert validateSyntax(expression) == False
    expression = ['3', '+', '32', '-', '+', '4']
    assert validateSyntax(expression) == False

def test_validateSyntax_second_op_is_minus():
    expression = ['3', '+', '32', '/', '-', '4']
    assert validateSyntax(expression) == expression
    expression = ['3', '+', '32', '*', '-', '4']
    assert validateSyntax(expression) == expression
    expression = ['3', '+', '32', '+', '-', '4']
    assert validateSyntax(expression) == expression
    expression = ['3', '+', '32', '-', '-', '4']
    assert validateSyntax(expression) == expression

def test_validateSyntax_with_flat_parens():
    expression = ['2', '+', '(', '7', '-', '4', ')', '-', '2']
    assert validateSyntax(expression) == expression

def test_validateSyntax_with_nested_parens():
    expression = ['2', '+', '(', '(', '7', '-', '4', ')', ')', '-', '5']
    assert validateSyntax(expression) == expression
    expression = ['2', '+', '(', '7', '-', '(', '6', '+', '4', ')', ')', '-', '5']
    assert validateSyntax(expression) == expression
    expression = ['2', '+', '(', '7', '-', '(', '6', '+', '4', ')', '-', '2', ')', '-', '5']
    assert validateSyntax(expression) == expression

def test_validateSyntax_ops_at_end():
    expression = ['4', '+', '7', '*', '8', '/', '2', '-', '9', '+']
    assert validateSyntax(expression) == False
    expression = ['4', '+', '7', '*', '8', '/', '2', '-', '9', '-']
    assert validateSyntax(expression) == False
    expression = ['4', '+', '7', '*', '8', '/', '2', '-', '9', '*']
    assert validateSyntax(expression) == False
    expression = ['4', '+', '7', '*', '8', '/', '2', '-', '9', '/']
    assert validateSyntax(expression) == False

def test_validateSyntax_ops_before_close_paren():
    expression = ['(', '3', '-', ')']
    assert validateSyntax(expression) == False
    expression = ['(', '-', ')']
    assert validateSyntax(expression) == False
    expression = ['(', '-', '+', ')']
    assert validateSyntax(expression) == False

def test_validateSyntax_ops_at_beginning():
    # One leading operator
    expression = ['-', '5', '+', '-', '8']
    assert validateSyntax(expression) == ['~', '5', '+', '~', '8']
    expression = ['+', '5', '+', '-', '8']
    assert validateSyntax(expression) == False
    expression = ['*', '5', '+', '-', '8']
    assert validateSyntax(expression) == False
    expression = ['/', '5', '+', '-', '8']
    assert validateSyntax(expression) == False
    expression = ['/', '+', '5', '+', '-', '8']
    assert validateSyntax(expression) == False

    # Two leading operators
    # Second op is minus
    expression = ['-', '-', '5']
    assert validateSyntax(expression) == False
    expression = ['+', '-', '5']
    assert validateSyntax(expression) == False
    expression = ['*', '-', '5']
    assert validateSyntax(expression) == False
    expression = ['/', '-', '5']
    assert validateSyntax(expression) == False

    # Second op is plus
    expression = ['-', '+', '5']
    assert validateSyntax(expression) == False
    expression = ['+', '+', '5']
    assert validateSyntax(expression) == False
    expression = ['*', '+', '5']
    assert validateSyntax(expression) == False
    expression = ['/', '+', '5']
    assert validateSyntax(expression) == False

    # Second op is mult
    expression = ['-', '*', '5']
    assert validateSyntax(expression) == False
    expression = ['+', '*', '5']
    assert validateSyntax(expression) == False
    expression = ['*', '*', '5']
    assert validateSyntax(expression) == False
    expression = ['/', '*', '5']
    assert validateSyntax(expression) == False

    # Second op is div
    expression = ['-', '/', '5']
    assert validateSyntax(expression) == False
    expression = ['+', '/', '5']
    assert validateSyntax(expression) == False
    expression = ['*', '/', '5']
    assert validateSyntax(expression) == False
    expression = ['/', '/', '5']
    assert validateSyntax(expression) == False

def test_validateSyntax_unary_minus():
    expression = ['8', '-', '-', '11', '*', '2']
    assert validateSyntax(expression) == ['8', '-', '~', '11', '*', '2']
    expression = ['2', '+', '(', '-', '3', '*', '4', ')']
    assert validateSyntax(expression) == ['2', '+', '(', '~', '3', '*', '4', ')']
    expression = ['-','(', '3', ')', '*', '(', '4', ')']
    assert validateSyntax(expression) == ['~','(', '3', ')', '*', '(', '4', ')']

def test_validateSyntax_one_lone_op():
    expression = ['+']
    assert validateSyntax(expression) == False
    expression = ['-']
    assert validateSyntax(expression) == False
    expression = ['*']
    assert validateSyntax(expression) == False
    expression = ['/']
    assert validateSyntax(expression) == False

def test_validate_syntax_no_op_between_parens():
    expression = ['(', '3', ')', '(', '4', ')']
    assert validateSyntax(expression) == False
    expression = ['(', '3', ')', '7', '(', '4', ')']
    assert validateSyntax(expression) == False
    expression = ['(', '3', ')', '+', '7', '(', '4', ')']
    assert validateSyntax(expression) == False
    expression = ['(', '3', ')', '7', '+', '(', '4', ')']
    assert validateSyntax(expression) == False
    expression = ['(', ')']
    assert validateSyntax(expression) == False

def test_validateSyntax_multiple_ops_after_open_paren():
    expression = ['8', '-', '(', '-', '-', '11', ')', '*', '2']
    assert validateSyntax(expression) == False

def test_checkBalancedParens():
    expression = ['2', '+', '(', '2']
    assert checkBalancedParens(expression) == False
    expression = ['2', ')', '+', '2']
    assert checkBalancedParens(expression) == False
    expression = ['2', '+', '(', '4', '-', '(', '7', ')']
    assert checkBalancedParens(expression) == False
    expression = ['2', '+', '(', '4', '-', '7', ')', ')']
    assert checkBalancedParens(expression) == False
    expression = ['(', ')']
    assert checkBalancedParens(expression) == True
    expression = ['(', '3', ')', '(', '4', ')']
    assert checkBalancedParens(expression) == True
    expression = ['(']
    assert checkBalancedParens(expression) == False
    expression = [')']
    assert checkBalancedParens(expression) == False

def test_evaluatePostfix_empty_expression():
    expression = []
    assert evaluatePostfix(expression) == False

def test_evaluatePostfix_invalid_expression():
    expression = ['2', '+',]
    assert evaluatePostfix(expression) == False
    expression = ['8', '3', '~', '+', '-']
    assert evaluatePostfix(expression) == False
    expression = ['4', '2']
    assert evaluatePostfix(expression) == False

def test_precedence():
    op = "+"
    assert precedence(op) == 0
    op = "-"
    assert precedence(op) == 0
    op = "*"
    assert precedence(op) == 1
    op = "/"
    assert precedence(op) == 1
    op = "~"
    assert precedence(op) == 2