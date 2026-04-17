'''
HIT137 - Group Assignment 2, Group: Sydney 14
Question 2: Recursive descent parser/evaluator for mathematical expressions.
'''

import os


# breaks the expression string into a list of tokens
def tokenise(text):
    tokens = []
    i = 0

    while i < len(text):
        ch = text[i]

        # skip whitespace
        if ch == ' ' or ch == '\t':
            i += 1

        # grab the full number including decimals
        elif ch.isdigit() or ch == '.':
            j = i
            while j < len(text) and (text[j].isdigit() or text[j] == '.'):
                j += 1
            tokens.append(('NUM', text[i:j]))
            i = j

        # single character operators + - * /
        elif ch in '+-*/':
            tokens.append(('OP', ch))
            i += 1

        # left and right brackets
        elif ch == '(':
            tokens.append(('LPAREN', '('))
            i += 1

        elif ch == ')':
            tokens.append(('RPAREN', ')'))
            i += 1

        else:
            # unknown character means the expression is invalid
            return None

    # signal the end of the token list
    tokens.append(('END', ''))
    return tokens


# formats token list into the required output string e.g. [NUM:3] [OP:+] [END]
def format_tokens(tokens):
    if tokens is None:
        return 'ERROR'

    parts = []
    for type_, value in tokens:
        if type_ == 'END':
            parts.append('[END]')
        elif type_ == 'LPAREN':
            parts.append('[LPAREN:(]')
        elif type_ == 'RPAREN':
            parts.append('[RPAREN:)]')
        else:
            parts.append(f'[{type_}:{value}]')

    return ' '.join(parts)


# peek at the current token without moving forward
def current(tokens, pos):
    return tokens[pos[0]]


# return the current token and step forward by one
def consume(tokens, pos):
    token = tokens[pos[0]]
    pos[0] += 1
    return token


# handles the highest precedence: numbers, brackets and unary minus
def parse_factor(tokens, pos):
    tok = current(tokens, pos)

    # unary minus e.g. -5 or -(3+4) - recurse to get the operand after the minus
    if tok[0] == 'OP' and tok[1] == '-':
        consume(tokens, pos)
        operand = parse_factor(tokens, pos)
        if operand is None:
            return None
        return ('neg', operand)

    # unary + is not supported, return error
    if tok[0] == 'OP' and tok[1] == '+':
        return None

    # plain number, just wrap it in a node
    if tok[0] == 'NUM':
        consume(tokens, pos)
        return ('num', float(tok[1]))

    # parenthesised expression - recurse back to the top and expect a closing bracket
    if tok[0] == 'LPAREN':
        consume(tokens, pos)                    # eat the (
        node = parse_expression(tokens, pos)
        if node is None:
            return None
        if current(tokens, pos)[0] != 'RPAREN':
            return None                         # closing bracket missing
        consume(tokens, pos)                    # eat the )

        # handle implicit multiplication e.g. (3+4)(2) or (3+4)5
        nxt = current(tokens, pos)
        if nxt[0] in ('NUM', 'LPAREN'):
            right = parse_factor(tokens, pos)
            if right is None:
                return None
            node = ('*', node, right)

        return node

    return None


# handles * and / by calling parse_factor for each side
def parse_term(tokens, pos):
    left = parse_factor(tokens, pos)
    if left is None:
        return None

    # keep looping while we keep seeing * or /
    while (current(tokens, pos)[0] == 'OP' and
           current(tokens, pos)[1] in '*/'):
        op = consume(tokens, pos)[1]
        right = parse_factor(tokens, pos)
        if right is None:
            return None
        left = (op, left, right)

    return left


# handles + and - by calling parse_term for each side
def parse_expression(tokens, pos):
    left = parse_term(tokens, pos)
    if left is None:
        return None

    # keep looping while we keep seeing + or -
    while (current(tokens, pos)[0] == 'OP' and
           current(tokens, pos)[1] in '+-'):
        op = consume(tokens, pos)[1]
        right = parse_term(tokens, pos)
        if right is None:
            return None
        left = (op, left, right)

    return left


# entry point for the parser - kicks off parsing and checks nothing is left over
def parse(tokens):
    if tokens is None:
        return None

    pos = [0]                                   # use a list so it can be modified inside functions
    tree = parse_expression(tokens, pos)

    # if we didn't reach END then there were unexpected tokens
    if tree is None or current(tokens, pos)[0] != 'END':
        return None

    return tree


# converts the parse tree into the required output string e.g. (+ 3 5)
def format_tree(node):
    if node is None:
        return 'ERROR'

    # just a number, return it without decimal if whole
    if node[0] == 'num':
        val = node[1]
        if val == int(val):
            return str(int(val))
        return str(val)

    # unary negation node
    if node[0] == 'neg':
        return f'(neg {format_tree(node[1])})'

    # binary operation - operator goes first then left and right subtrees
    op, left, right = node
    return f'({op} {format_tree(left)} {format_tree(right)})'


# walks the tree and computes the actual result
def evaluate(node):
    if node is None:
        return None

    # base case - just return the number value
    if node[0] == 'num':
        return node[1]

    # negate the result of the operand
    if node[0] == 'neg':
        val = evaluate(node[1])
        if val is None:
            return None
        return -val

    # evaluate both sides then apply the operator
    op = node[0]
    left = evaluate(node[1])
    right = evaluate(node[2])

    if left is None or right is None:
        return None

    if op == '+': return left + right
    if op == '-': return left - right
    if op == '*': return left * right
    if op == '/':
        if right == 0:
            return None                         # can't divide by zero
        return left / right

    return None


# formats the result as a clean number or ERROR
def format_result(value):
    if value is None:
        return 'ERROR'
    # drop the decimal point for whole numbers e.g. 8 not 8.0
    if value == int(value):
        return str(int(value))
    return str(round(value, 4))


# reads expressions from the input file, evaluates each one and writes output.txt
def evaluate_file(input_path: str) -> list[dict]:
    with open(input_path, 'r') as f:
        lines = f.readlines()

    results = []
    output_lines = []

    for line in lines:
        expr = line.rstrip('\n')                # strip the newline but keep everything else

        # tokenise the expression
        tokens = tokenise(expr)
        tokens_str = format_tokens(tokens)

        # parse into a tree
        tree = parse(tokens)
        tree_str = format_tree(tree)

        # evaluate the tree
        if tree is None:
            value = None
        else:
            value = evaluate(tree)

        result_str = format_result(value)

        # store the result as a dict
        result_dict = {
            'input': expr,
            'tree': tree_str,
            'tokens': tokens_str,
            'result': value if value is not None else 'ERROR'
        }
        results.append(result_dict)

        # write the 4-line block for this expression
        output_lines.append(f'Input: {expr}')
        output_lines.append(f'Tree: {tree_str}')
        output_lines.append(f'Tokens: {tokens_str}')
        output_lines.append(f'Result: {result_str}')
        output_lines.append('')                 # blank line between blocks

    # save everything to output.txt in the same folder as the input
    output_path = os.path.join(os.path.dirname(input_path), 'output.txt')
    with open(output_path, 'w') as f:
        f.write('\n'.join(output_lines))

    return results


if __name__ == '__main__':
    # run on sample_input.txt by default, or pass a file as argument
    sample_expressions = [
        '3 + 5',
        '2 + 3 * 4',
        '-(3 + 4)',
        '--5',
        '(10 - 2) * 3 + -4 / 2',
        '3 @ 5',
        '1 / 0',
    ]

    # write the sample input file
    with open('sample_input.txt', 'w') as f:
        f.write('\n'.join(sample_expressions))

    # run the evaluator
    results = evaluate_file('sample_input.txt')

    # print each result to the screen
    for r in results:
        print(f"Input:   {r['input']}")
        print(f"Tree:    {r['tree']}")
        print(f"Tokens:  {r['tokens']}")
        print(f"Result:  {format_result(r['result']) if r['result'] != 'ERROR' else 'ERROR'}")
        print()