#! /usr/bin/env python3

import sys

# 1. Split input into components: operators and operands
# 2. Convert operands from strings to numbers
# 3. Apply operators to operands?

# 

# I can probably use some sort of function dispatch to keep track of available
# operations.
# Validate the string while splitting it into operands and operators.
#   First and last char cannot be operands
#   Two operands cannot be next to each other
# Convert it into postfix notation.
# Evaluate the expression.

operators = "+-"

def splitIntoOpComponents(input):
    comps = []
    number = ""
    # Check first and last characters of the string.
    # If neither is a digit, the syntax is invalid.
    if (input[0] in operators or input[-1] in operators):
        print("Syntax error.", file = sys.stderr)
        return False
    else:
        for c in input:
            # Ignore empty spaces
            if (c != " "):
                if (c in operators):
                    # Add most recent number to the component list if applicable
                    # and empty the number string
                    if (len(number) > 0):
                        comps.append(number)
                        number = ""

                    # If the last item in the component list is an operator,
                    # the syntax of the input string is incorrect
                    if (len(comps) > 0 and comps[-1] in operators):
                        print("Syntax error.", file = sys.stderr)
                        return False
                        
                    # Add the current operator to the component list
                    comps.append(c)
                elif (c.isdigit()):
                    # Add digit to number string
                    number += c
                else:
                    # Character is illegal and the input string is invalid
                    print("Input string is invalid.", file = sys.stderr)
                    return False

        # Add the final number string to the component list
        if (len(number) > 0):
                    comps.append(number)

    return comps

def add(l, r):
    return l + r

def sub(l, r):
    return l - r

ops = {
    "+": add,
    "-": sub,
}

def main():
    input = str(sys.argv[1])
    components = splitIntoOpComponents(input)
    if (components):
        print(components)
    else:
        print("The program encountered an error.")

if __name__ == "__main__":
    main()