#!python3

"""
Simple lisp style preorder expression evaluator.

Accepts expressions in the following style:
['function', 'arg', 'arg']

Accepts a dictionary of defined functions.
Anything not found in the funcs dict is assumed
to be a literal.

Raises:
    ExpressionConstraintError
    Allows user defined constraints to make an
    expression invalid.
"""

class evaluator:
    def __init__(self, funcs, varsIn = None):
        #dict of functions to be used
        self.functions = funcs
        self.vars = varsIn

    #Allow functions to be called by name in an argument, like in lisp.
    #ie.    lisp: (funcname arg1 arg2 ... argn)
    #       here: ['funcname', 'arg1', 'arg2', ..., 'argn']
    def eval(self, *args):
        #repackage arguments minus the function name
        funcArgs = list(args[1:])
        funcName = args[0]
        #skip if the function is just a number
        if isinstance(funcName,int):
            return funcName

        #convert function name strings to defined functions
        if isinstance(args[0], str) and (args[0] in self.functions):
            funcName = self.functions[args[0]]

        #call any callable arguments
        for i in range(len(funcArgs)):
            #this will handle functions without args
            if callable(funcArgs[i]):
                funcArgs[i] = funcArgs[i]()
            elif self.vars!=None and self.vars.callable(funcArgs[i]):
                funcArgs[i] = self.vars.call(funcArgs[i])
            #this will handle lisp style functions with args
            elif isinstance(funcArgs[i], list):
                funcArgs[i] = self.eval(*funcArgs[i])
        try:
            return funcName(*funcArgs)
        except TypeError as err:
            #funcName must be string.
            #Either funcName has not been defined or it is a defined var.
            if (self.vars != None) and (self.vars.callable(funcName)):
                return self.vars.call(funcName)
            else:
                print(format(err))



#Handle constraints that make an expression invalid:
class ExpressionConstraintError(ValueError):
    '''raise this when there are constraints that make an expression invalid'''
