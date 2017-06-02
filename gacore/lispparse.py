#!python3
import ast
"""
Simple s-expression parser.

Reads expressions from plain text
(one exp per line)

returns a list which can be used by the evaluator.

"""

class parser:
    def __init__(self, filename):
        self.filename = filename

    #read a single line from the file and return an expression list.
    def readOne(self, line):
        f = open(self.filename,'r')
        for l in range(0,line):
            line = f.readline()
        f.close()
        return self.parse(line)

    #read all lines from the file and return an iterable of expression lists.
    def readAll(self):
        f = open(self.filename,'r')
        lines = f.readlines()
        f.close()
        parsed = map(self.parse, lines)
        return parsed

    #parses text to a list
    def parse(self, text):
        return ast.literal_eval(text)
