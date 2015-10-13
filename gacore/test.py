#!python3

import grammar
import lispeval
import unittest

#Define Grammar

#non-terminals for randomly building grammar
#each terminal should return a list of symbols
#randomly. Randomness omitted here for testing.
def exp():
    sequences = [[op2, var, var]]
    return sequences[0]

def op2():
    sequences = ["add","subtract"]
    return sequences[0]

def var():
    sequences = range(10)
    return sequences[2] #returns number 2

#non-terminals for list based grammar building
#terminals should return a list of symbols at
#the nth position, determined by list.
def exp_l(n):
    sequences = [[op2_l, var_l, var_l],var_l]
    return sequences[n % len(sequences)]

def op2_l(n):
    sequences = ["add","subtract"]
    return sequences[n % len(sequences)]

def var_l(n):
    sequences = range(10)
    return sequences[n % len(sequences)]

g = grammar.builder();

class GrammarTest(unittest.TestCase):
    def test_random_grammar_builder(self):
        self.assertEqual(g.build(exp), ['add',2,2])

    def test_list_based_grammar_builder(self):
        #test getting single variable
        self.assertEqual(g.buildList(exp_l,[1,2]), [2])
        #test getting single op with vars
        self.assertEqual(g.buildList(exp_l,[0,2,2,6]), ['add', 2, 6])
        #test getting single op with vars, and wraparound list values
        self.assertEqual(g.buildList(exp_l,[0,2,2]), ['add', 2, 0])


#Define terminals used in grammar, to be eval'd by evaluator

def add(n1, n2):
    return n1+n2

def subtract(n1, n2):
    return n1-n2

#list of terminals passed to evaluator.
terminals = {'add':add, 'subtract':subtract}

lisp = lispeval.evaluator(terminals)

class EvaluatorTest(unittest.TestCase):
    def test_lisp_evaluator(self):
        self.assertEqual(lisp.eval(*['add',2,2]), 4)
        self.assertEqual(lisp.eval(*['subtract',2,2]), 0)
        self.assertEqual(lisp.eval(*['add',['subtract', 10, 6],4]), 8)


#Run tests
unittest.main()
