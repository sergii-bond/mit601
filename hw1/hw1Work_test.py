__author__ = 'sergii'

import hw1Work

# tokens = hw1Work.tokenize('(((285+364)*50)/(2+3)')
# 
# print tokens
# 
# p = hw1Work.parse(tokens)
# p = hw1Work.parse(hw1Work.tokenize('z'))
# p = hw1Work.tokenize('z')
# print p
# 
# hw1Work.testTokenize()
# hw1Work.testParse()
# hw1Work.testEval()
testExprs = ['(2 + 5)',
             '(z = 6)',
             'z',
             '(w = (z + 1))',
             'w'
             ]

hw1Work.calcTest(testExprs)
hw1Work.calc()
