# import pdb
# import lib601.sm as sm
import string
import operator


class BinaryOp:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __str__(self):
        return self.opStr + '(' + \
            str(self.left) + ', ' +\
            str(self.right) + ')'
    __repr__ = __str__

    def eval(self, env):
        return self.op(self.left.eval(env), self.right.eval(env))


class Sum(BinaryOp):
    opStr = 'Sum'
    op = operator.add


class Prod(BinaryOp):
    opStr = 'Prod'
    op = operator.mul


class Quot(BinaryOp):
    opStr = 'Quot'
    op = operator.div


class Diff(BinaryOp):
    opStr = 'Diff'
    op = operator.sub


class Assign(BinaryOp):
    opStr = 'Assign'

    def eval(self, env):
        env[self.left.name] = self.right.eval(env)
        return True


class Number:
    def __init__(self, val):
        self.value = val

    def __str__(self):
        return 'Num('+str(self.value)+')'
    __repr__ = __str__

    def eval(self, env):
        return self.value


class Variable:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return 'Var('+self.name+')'
    __repr__ = __str__

    def eval(self, env):
        return env[self.name]


# characters that are single-character tokens
seps = ['(', ')', '+', '-', '*', '/', '=']


class StateMachine():
    def __init__(self):
        pass

    def getNextValue(self, state, inp):
        pass

    def step(self, inp):
        (self.state, out) = self.getNextValue(self.state, inp)
        return out

    def transduce(self, str):
        return [self.step(inp) for inp in str]


class Tokenizer(StateMachine):
    def __init__(self, seps):
        self.state = [1, '']
        self.seps = seps

    def isSeparator(self, seps, char):
        for x in seps:
            if char == x:
                return True
        return False

    def getNextValue(self, state, inp):
        acc = state[1]

        if self.isSeparator(self.seps, inp):
            next = 2
            if not acc == '':
                out = [acc, inp]
            else:
                out = [inp]
            acc = ''
        elif state[0] == 1 and inp == '\n':
            out = [acc]
            next = 3
        else:
            out = []
            next = 1
            if not inp == ' ':
                acc += str(inp)

        return ([next, acc], out)


# Convert strings into a list of tokens (strings)
def tokenize(string):
    # <your code here>
    t = Tokenizer(seps)
    a = []
    for y in t.transduce(string + '\n'):
        a = a + y
    return a


# tokens is a list of tokens
# returns a syntax tree:  an instance of {\tt Number}, {\tt Variable},
# or one of the subclasses of {\tt BinaryOp}
def parse(tokens):
    def parseExp(index):
        # <your code here>
        t = tokens[index]
        ni = index + 1

        if numberTok(t):
            p = Number(float(t))
        elif variableTok(t):
            p = Variable(t)
        else:
            # then the token is
            (left, ni) = parseExp(ni)
            op_tok = tokens[ni]
            ni += 1
            (right, ni) = parseExp(ni)
            # account for ')'
            ni += 1

            # seps = ['(', ')', '+', '-', '*', '/', '=']
            if op_tok == '+':
                p = Sum(left, right)
            elif op_tok == '-':
                p = Diff(left, right)
            elif op_tok == '/':
                p = Quot(left, right)
            elif op_tok == '*':
                p = Prod(left, right)
            elif op_tok == '=':
                p = Assign(left, right)

        return (p, ni)

    (parsedExp, nextIndex) = parseExp(0)
    return parsedExp


# token is a string
# returns True if contains only digits
def numberTok(token):
    for char in token:
        if char not in string.digits:
            return False
    return True


# token is a string
# returns True its first character is a letter
def variableTok(token):
    for char in token:
        if char in string.letters:
            return True
    return False


# thing is any Python entity
# returns True if it is a number
def isNum(thing):
    return type(thing) == int or type(thing) == float


# Run calculator interactively
def calc():
    env = {}
    while True:
        inp = raw_input('%')            # prints %, returns user input
        print '%', parse(tokenize(inp)).eval(env)
        print '   env =', env


# exprs is a list of strings
# runs calculator on those strings, in sequence, using the same environment
def calcTest(exprs):
    env = {}
    for e in exprs:
        print '%', e                    # e is the experession
        print parse(tokenize(e)).eval(env)
        print '   env =', env

# Simple tokenizer tests
'''Answers are:
['fred']
['777']
['777', 'hi', '33']
['*', '*', '-', ')', '(']
['(', 'hi', '*', 'ho', ')']
['(', 'fred', '+', 'george', ')']
['(', 'hi', '*', 'ho', ')']
['(', 'fred', '+', 'george', ')']
'''


def testTokenize():
    print tokenize('fred ')
    print tokenize('777 ')
    print tokenize('777 hi 33 ')
    print tokenize('**-)(')
    print tokenize('( hi * ho )')
    print tokenize('(fred + george)')
    print tokenize('(hi*ho)')
    print tokenize('( fred+george )')


# Simple parsing tests from the handout
'''Answers are:
Var(a)
Num(888.0)
Sum(Var(fred), Var(george))
Quot(Prod(Var(a), Var(b)), Diff(Var(cee), Var(doh)))
Quot(Prod(Var(a), Var(b)), Diff(Var(cee), Var(doh)))
Assign(Var(a), Prod(Num(3.0), Num(5.0)))
'''


def testParse():
    print parse(['a'])
    print parse(['888'])
    print parse(['(', 'fred', '+', 'george', ')'])
    print parse(['(', '(', 'a', '*', 'b', ')', '/', '(',
                'cee', '-', 'doh', ')', ')'])
    print parse(tokenize('((a * b) / (cee - doh))'))
    print parse(tokenize('(a = (3 * 5))'))

####################################################################
# Test cases for EAGER evaluator
####################################################################


def testEval():
    env = {}
    Assign(Variable('a'), Number(5.0)).eval(env)
    print Variable('a').eval(env)
    env['b'] = 2.0
    print Variable('b').eval(env)
    env['c'] = 4.0
    print Variable('c').eval(env)
    print Sum(Variable('a'), Variable('b')).eval(env)
    print Sum(Diff(Variable('a'), Variable('c')), Variable('b')).eval(env)
    Assign(Variable('a'), Sum(Variable('a'), Variable('b'))).eval(env)
    print Variable('a').eval(env)
    print env

# Basic calculator test cases (see handout)
testExprs = ['(2 + 5)',
             '(z = 6)',
             'z',
             '(w = (z + 1))',
             'w'
             ]
# calcTest(testExprs)

####################################################################
# Test cases for LAZY evaluator
####################################################################

# Simple lazy eval test cases from handout
'''Answers are:
Sum(Var(b), Var(c))
Sum(2.0, Var(c))
6.0
'''


def testLazyEval():
    env = {}
    Assign(Variable('a'), Sum(Variable('b'), Variable('c'))).eval(env)
    print Variable('a').eval(env)
    env['b'] = Number(2.0)
    print Variable('a').eval(env)
    env['c'] = Number(4.0)
    print Variable('a').eval(env)

# Lazy partial eval test cases (see handout)
lazyTestExprs = ['(a = (b + c))',
                 '(b = ((d * e) / 2))',
                 'a',
                 '(d = 6)',
                 '(e = 5)',
                 'a',
                 '(c = 9)',
                 'a',
                 '(d = 2)',
                 'a']
# calcTest(lazyTestExprs)

# More test cases (see handout)
partialTestExprs = ['(z = (y + w))',
                    'z',
                    '(y = 2)',
                    'z',
                    '(w = 4)',
                    'z',
                    '(w = 100)',
                    'z']

# calcTest(partialTestExprs)
