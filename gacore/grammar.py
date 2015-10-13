#!python3
import random
import copy

"""
Grammar based expression builder.

Define non-terminals as functions with 0 args that returns a list of
terminals (strings or integers) or non-terminals.

This does not evaluate an expression.
See gacore.lispeval for this functionality.
"""


class builder:
    def __init__(self, symbols):
        """
        Accept:
            Symbols object.
            See countdowngrammar.py for an example symbols object.
            Must have `startExpression` `call` and `callable` methods.

        Future work:
            Provide abstract version of symbol class.
        """
        self.symIter = 0
        self.symList = []
        self.symbols = symbols

    def buildDepthFirst(self, gNonTerm):

        #instance for recursion
        gb = builder()
        self.gNonTerm = gNonTerm
        #iterate through lists
        if isinstance(self.gNonTerm, list):
            for i in range(len(self.gNonTerm)):
                if (callable(self.gNonTerm[i])):
                    self.gNonTerm[i] = gb.buildDepthFirst(self.gNonTerm[i]())
        #call anything callable
        elif callable(self.gNonTerm):
            self.gNonTerm = gb.buildDepthFirst(self.gNonTerm())
        #leave terminals untouched
        else:
            pass
        return self.gNonTerm


    def buildDepthFirstList(self, gNonTerm, symList, symIter):
        """
            Calling this directly is not recommended.
            See helper function `buildList` below.

            Some commented print statements left here for debugging.

            Further work:
                Implement logging.
        """

        #instance for recursion
        gb = builder(self.symbols)
        self.gNonTerm = gNonTerm
        self.symList = symList
        self.symIter = symIter
        #print(gNonTerm)
        #input("\nPress Enter to continue...")
        #iterate through lists
        if isinstance(self.gNonTerm, list):
            #print("is list")
            for i in range(len(self.gNonTerm)):
                if (self.symbols.callable(self.gNonTerm[i])):
                    self.gNonTerm[i] = gb.buildDepthFirstList( self.symbols.call(self.gNonTerm[i], self.symList[self.__symIterate__()] ),self.symList, self.symIter )

        #call anything callable
        elif self.symbols.callable(self.gNonTerm):
            #print("callable")
            self.gNonTerm = gb.buildDepthFirstList( self.symbols.call(self.gNonTerm, self.symList[self.__symIterate__()] ),self.symList, self.symIter )
        #leave terminals untouched
        else:
            #print("terminal: "+str(self.gNonTerm))
            pass
        return self.gNonTerm


    #Helper function for buildDepthFirst
    def build(self, startSymbol):
        """
        Builds an expression without any guidance.
        Assumes that each non-terminal function can independently decide what
        it needs to return. Useful for building random expressions or
        stochastic expressions.

        For building expressions based on a list of predefined values, see
        buildList below.

        Accept:
            Start Symbol

        Returns:
            A fully built expression.
        """
        #call recursive method
        builtExpression = self.buildDepthFirst(startSymbol)
        #make sure output is always encased in a list
        if not isinstance(builtExpression, list):
            builtExpression = [builtExpression]
        return builtExpression

    #Helper function to iterate through symList
    #returns iterator value and increments it.
    def __symIterate__(self):
        if self.symIter >= len(self.symList):
            self.symIter = 0
        ret = self.symIter
        self.symIter += 1
        return ret

    def buildList(self, symList):
        """
        Builds an expression guided by a predefined list.
        (Helper function for buildDepthFirstList)

        Assumes each non-terminal will accept a number which will decide what
        result to produce.

        Accept:
            List of numbers to be passed one by one (depth first) to
            non-terminals.

        Return:
            A fully built expression.
        """
        #setup symbol list and iterator
        self.symIter = 0
        self.symList = symList
        startSymbol = self.symbols.startExpression()
        #call recursive method
        try:
            builtExpression = self.buildDepthFirstList(startSymbol, self.symList, self.symIter)
        except RecursionError:
            #print("Grammar: Recusion Error while building expression.")
            return [0]
        #make sure output is always encased in a list
        if not isinstance(builtExpression, list):
            builtExpression = [builtExpression]
        return builtExpression

    #return random sequence.
    #Utility function, non-terminals should manage sequence choosing if
    # total random choice is not appropriate.
    def choose(self, sequence):
        return random.choice(sequence)
