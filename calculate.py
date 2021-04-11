#! /usr/bin/env python3.7
# Author: Nathaniel Rudenberg

from sys import argv
from sys import stderr

def add(l, r):
    """
    Adds two numbers together.
    Parameters: l - The left operand.
                r - The right operand.
    Returns: l + r
    """
    return l + r

def sub(l, r):
    """
    Subtracts the right operand from the left.
    Parameters: l - The left operand.
                r - The right operand.
    Returns: l - r
    """
    return l - r

def mult(l, r):
    """
    Multiplies two numbers together.
    Parameters: l - The left operand.
                r - The right operand.
    Returns: l * r
    """
    return l * r

def div(l, r):
    """
    Divides the left operand by the right.
    Parameters: l - The left operand.
                r - The right operand.
    Returns: l / r
    """
    return l / r

ops = {
    # Unary minus is represented by "~".
    "-": sub,
    "+": add,
    "/": div,
    "*": mult,
    "~": sub,
}

parens = "()"

def checkBalancedParens(expression):
    """
    Test whether the parentheses in the expression are balanced.
    Parameters: expression - The math expression to test.
    Returns: True if parentheses are balanced, otherwise returns False.
    """
    parenStack = []
    for item in expression:
        # Push open parens to stack
        if item == parens[0]:
            parenStack.append(item)
        # Check close parens against top of stack
        elif item == parens[1]:
            if len(parenStack) == 0:
                print("Syntax Error", file = stderr)
                return False
            else:
                parenStack.pop()
    
    if len(parenStack) > 0:
        print("Syntax Error", file = stderr)
        return False

    return True

def validateSyntax(expression):
    """
    Validates the syntax of the math expression.
    Parameters: expression - The math expression to validate.
    Returns: The validated math expression if all validations checks pass,
    otherwise returns False.
    """
    opsList = list(ops)

    # Empty expressions are invalid.
    if len(expression) == 0:
        return expression
    
    # Expressions with an operator as the final item are invalid.
    if expression[-1] in opsList:
        print("Syntax Error", file = stderr)
        return False

    # Check edge cases that apply for first item only
    if expression[0] in opsList:
        # Expressions with a non minus operator at the beginning are invalid.
        if expression[0] != "-":
            print("Syntax Error", file = stderr)
            return False
        # Expressions with two operators at the beginning are invalid.
        elif expression[1] in opsList:
            print("Syntax Error", file = stderr)
            return False
        # Expressions with a minus as the only operator at the beginning are accepted.
        else:
            expression[0] = "~"

    for i in range(1, len(expression)):
        if expression[i] in opsList:
            if expression[i - 1] == "(":
                if expression[i] == "-":
                    # Minus operators after left parens should be unary.
                    expression[i] = "~"
                if expression[i + 1] in opsList:
                    # There should not be two or more operators after an open
                    # parentheses.
                    print("Syntax Error", file = stderr)
                    return False
            elif expression[i - 1] in opsList:
                if expression[i + 1] in opsList:
                    # Return False if there are 3 or more expressions in series
                    print("Syntax Error", file = stderr)
                    return False
                if expression[i] == "-":
                    # The minus, being the second operator in series,
                    # should be a unary minus.
                    expression[i] = "~"
                else:
                    # Return False if there are two operators in series
                    # and the second is not minus.
                    print("Syntax Error", file = stderr)
                    return False
        elif expression[i] not in opsList and expression[i] not in parens:
            # If a number is not preceded by an operator or an open parentheses,
            # the syntax is invalid.
            if expression[i - 1] != "(" and expression[i - 1] not in opsList:
                print("Syntax Error", file = stderr)
                return False
        elif expression[i] == "(":
            # If the open parentheses is not the first item in the expression,
            # it must be preceded by an operator or another open parentheses.
            if expression[i - 1] not in opsList and expression[i - 1] != "(":
                print("Syntax Error", file = stderr)
                return False
        elif expression[i] == ")":
            # If the close parentheses is preceded by an operator or an
            # open parentheses, the syntax is invalid.
            if expression[i - 1] in opsList or expression[i - 1] == "(":
                print("Syntax Error", file = stderr)
                return False

    if checkBalancedParens(expression):
        return expression
    else:
        return False

def precedence(op):
    """
    Get the precedence of a given operator.
    Parameters: op - an arithmetic operator.
    Available operators are +, -, *, /, and ~ (unary minus).
    Returns: The precedence of the given operator.
    """
    if op in "+-":
        return 0
    elif op in "*/":
        return 1
    elif op is "~":
        return 2

def getNumber(input, pos):
    """
    Get a number from the math expression input.
    Parameters: input - The math expression input.
                pos - The position of the first character of the number in the input.
    Returns:    (number, pos, invalidSyntax)
                number - The number that was extracted from the input.
                pos - The current position in the input string.
                invalidSyntax - Syntax validation flag.
    """
    number = ""
    invalidSyntax = False
    # Loop through the string until a non-digit, non-decimal character is reached.
    while pos < len(input) and (input[pos].isdigit() or input[pos] is "."):
        currentChar = input[pos]
        if currentChar is "." and currentChar in number:
            print("Syntax Error: number has more than one decimal point.", file = stderr)
            invalidSyntax = True
            return ('0', -1, invalidSyntax)
        number += currentChar
        pos += 1
    
    if number[-1] == ".":
        print("Syntax Error: number has a trailing decimal point", file = stderr)
        invalidSyntax = True
        return ('0', -1, invalidSyntax)

    return (number, pos, invalidSyntax)

def parse(input):
    """
    Separates the components of the math expression input into separate parts.
    Parameters: input - The math expression string.
    Returns: A list containing the separate parts of the math expression.
    """
    currentPos = 0
    expression = []
    if not input:
        print("Invalid Input: empty.", file = stderr)
        return False

    while currentPos < len(input):
        currentChar = input[currentPos]
        if currentChar is not " ":
            # Operators and parentheses are single characters, so add them to
            # the list here.
            if currentChar in ops.keys() or currentChar in parens:
                expression.append(currentChar)
                currentPos += 1
            # A number might be more than one digit long. Pass starting
            # position of the number to a helper function to get the entire
            # number.
            elif currentChar.isdigit() or currentChar == ".":
                number, currentPos, error = getNumber(input, currentPos)
                if error:
                    return False
                expression.append(number)
            else:
                # Character is illegal and the input string is invalid
                print("Invalid Input: illegal character found.", file = stderr)
                return False
        else:
            # Skip empty spaces
            currentPos += 1

    return expression

def convertToPostfix(expression):
    """
    Converts an infix expression to postfix.
    Parameters: expression - The infix expression.
    Returns: The converted postfix expression.
    """
    opStack = []
    postfix = []
    opStack.append("#")
    for i in range(len(expression)):
        # Add number to the output list
        if expression[i] not in ops.keys() and expression[i] not in parens:
            postfix.append(expression[i])
        # Add top of operator stack to output list while the top of the stack
        # is an operator with precedence equal to or greater than that of the
        # current operator, then add the current operator to the stack.
        elif expression[i] in list(ops):
            while opStack[-1] in list(ops) and precedence(opStack[-1]) >= precedence(expression[i]):
                postfix.append(opStack.pop())
            opStack.append(expression[i])
        # Add left parentheses to the operator stack.
        elif expression[i] is "(":
            opStack.append(expression[i])
        # Add top of operator stack to output list while the top of the stack
        # is not a left parentheses.
        elif expression[i] is ")":
            while opStack[-1] != "#" and opStack[-1] != "(":
                postfix.append(opStack.pop())
            opStack.pop()
    
    # Add remaining items in the operator stack to the output list.
    while opStack[-1] != "#":
        postfix.append(opStack.pop())
    
    return postfix

def evaluatePostfix(expression):
    """
    Evaluates the result of a postfix expression.
    Parameters: expression - The postfix expression.
    Returns: The result of the calculation.
    """
    if len(expression) > 0:
        evalStack = []
        for item in expression:
            if item not in list(ops):
                num = 0
                if "." in item:
                    num = float(item)
                else:
                    num = int(item)
                evalStack.append(num)
            else:
                if len(evalStack) > 0:
                    r = evalStack.pop()
                else:
                    print("Syntax Error", file = stderr)
                    return False
                if len(evalStack) > 0:
                    l = evalStack.pop() if item != "~" else 0
                else:
                    print("Syntax Error", file = stderr)
                    return False
                evalStack.append(ops[item](l, r))
        
        if len(evalStack) == 1:
            return evalStack[0]
        else:
            print("Syntax Error")
            return False
    else:
        print("Syntax Error", file = stderr)
        return False

def main():
    """
    Parses the program input, validates the input, converts it to postfix,
    evaluates the result, then prints the result.
    """

    if len(argv) == 2:
        input = str(argv[1])
        expression = parse(input)
        validatedExpression = None
        postfix = None
        result = None
        if expression:
            validatedExpression = validateSyntax(expression)
        if validatedExpression:
            postfix = (convertToPostfix(validatedExpression))
        if postfix:
            result = evaluatePostfix(postfix)
        if result:
            print(result)
    else:
        print("Invalid Input")

if __name__ == "__main__":
    main()