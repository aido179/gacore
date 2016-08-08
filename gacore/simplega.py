#!python3
import random
import copy

log = "none"

"""
Simple genetic algorithm implementation.

Population:
    Contains a list of individuals.
    Implements movement from one generation to the next.
    Implements Selection and Crossover.
    Calls mutation operator, implemented in individual.
    Provides glance and look functions to see info about a pop.
    Also provides stats about a population.

Individual:
    Contains chromosome, fitness function.
    Provides accessors and mutators (setters and getters).
    Implements mutation.
    Fitness function:
        May be a higher order function allowing the setPheno func
        to be passed as an argument. This allows the fitness func
        to update the individuals phenotype when called rather
        than building expressions twice (once in getFitness, once
        in a separate setPheno function).
"""

class population():
    def __init__(self, popSize, chromLen, fitnessFunc):
        self.popSize = popSize
        self.chromLen = chromLen
        self.fitnessFunc = fitnessFunc
        self.generation = 0
        #populate population.
        self.individuals = [individual(chromLen, fitnessFunc) for i in range(popSize)]
        self.previousIndividuals = []
        self.bestInd = self.individuals[0]

    def select(self, amount, prevGen):
        #Prevent selecting more than the population size.
        if amount > len(self.individuals):
            raise IndexError("Cannot select "+str(amount)+" from population of "+str(len(self.individuals)))
            return
        #Save computation if selecting entire pop.
        elif amount == len(self.individuals):
            return self.individuals[:]

        selected = []
        for i in range(amount):

            smp = random.sample(prevGen,2)

            #compare individuals and insert the fittest into the next generation
            if smp[0].getFitness() > smp[1].getFitness():
                selected.append(smp[0])
            elif smp[1].getFitness() > smp[0].getFitness():
                selected.append(smp[1])
            else:
                randomInd = random.choice(smp)  #pick one at random
                selected.append(randomInd)      #add it to selected

        return selected

    #single point crossover
    def mateChroms(self, par1, par2):
        crossPoint = random.randint(0,len(par1)-1)
        child1 = par1[:crossPoint]
        child1.extend(par2[crossPoint:])
        child2 = par2[:crossPoint]
        child2.extend(par1[crossPoint:])
        return [child1,child2]

    def crossover(self, crossRate, population, customCrossover = True):
        i = 0
        while i < len(population)*crossRate:

            p1 = random.randrange(0,len(population)-1)
            p2 = random.randrange(0,len(population)-1)
            par1 = population[p1]
            par2 = population[p2]

            if callable(customCrossover):
                childrenChroms = customCrossover(par1.getChrom(),par2.getChrom())
            else:
                childrenChroms = self.mateChroms(par1.getChrom(),par2.getChrom())

            child1 = individual(self.chromLen,self.fitnessFunc, chrom=childrenChroms[0])
            child2 = individual(self.chromLen,self.fitnessFunc, chrom=childrenChroms[1])

            population[p1] = child1
            population[p2] = child2
            i+=1
        return population

    def mutate(self,rate, population):
        for ind in population:
            ind.mutate(rate)
        return population

    def nextGen(self, crossoverRate, mutationRate, customCrossoverFunc = False):
        newGen = []
        self.bestInd = individual(self.chromLen,self.fitnessFunc, chrom=self.individuals[0].getChrom())

        for ind in self.individuals:
            if ind.getFitness() > self.bestInd.getFitness():
                self.bestInd = individual(self.chromLen,self.fitnessFunc, chrom=ind.getChrom())

        #Add Elites for mutation / crossover
        newGen.append(individual(self.chromLen,self.fitnessFunc, chrom=self.bestInd.getChrom()))
        newGen.append(individual(self.chromLen,self.fitnessFunc, chrom=self.bestInd.getChrom()))
        #Tournament selection
        newGen.extend(self.select(self.popSize-3, self.individuals))
        #Crossover
        newGen = self.crossover(crossoverRate, newGen, customCrossoverFunc)
        #Mutation
        newGen = self.mutate(mutationRate, newGen)
        #Add Elite, prevent mutation / crossover
        newGen.append(individual(self.chromLen,self.fitnessFunc, chrom=self.bestInd.getChrom()))

        self.previousIndividuals = self.individuals
        self.individuals = newGen
        self.generation += 1

    def stats(self):
        best = self.individuals[0]
        totalFitness = 0
        for i in self.individuals:
            if best.getFitness() < i.getFitness():
                best = i
            totalFitness += i.getFitness()
        avgFitness = totalFitness / self.popSize
        data = {'topFitness':best.getFitness(),'avgFitness':avgFitness, 'leader':best}
        return data

    def glance(self):
        """
        Provides a simple quick view of a generation
        """
        stats = self.stats()
        print("-----")
        #print("Population size:\t"+str(self.popSize))
        print("Generation:\t"+str(self.generation))
        print("Avg fitness:\t"+str(stats['avgFitness']))
        print("Top Fitness:\t"+str(stats['topFitness']))
        print("-----")

    def look(self):
        """
        Provides a more in depth view of a generation and its population
        """
        stats = self.stats()
        print("-----")
        print("Generation:\t"+str(self.generation))
        print("Avg fitness:\t"+str(stats['avgFitness']))
        print("Top Fitness:\t"+str(stats['topFitness']))
        print("\n")
        for i in self.individuals:
            print("-\nFitness:\t"+str(i.getFitness())+"\nPhenotype\t"+str(i.getPheno())[:60]+"...\nChromosome\t"+str(i.getChrom()[:10])+"...")
        print("-----")

    def lookPrevious(self):
        """
        Provides a view of the previous generations population.
        """
        for i in self.previousIndividuals:
            print(str(i.getFitness())+"\t"+str(i.getPheno())+"\t"+str(i.getChrom()))


class individual():
    def __init__(self, chromLen, fitnessFunc, chrom=[], phenotype=None):
        #if no chrom is provided, start with random chrom.
        #allows testing of certain chroms and seeding a population.
        if chrom == []:
            self.chromosome = [random.randint(0,255) for i in range(chromLen)]
        else:
            self.chromosome = chrom[:]
        self.chromLen = chromLen
        self.fitnessFunc = fitnessFunc
        self.__fitness__ = self.fitnessFunc(self.chromosome, self.setPheno)
        #pheno should be overwritable by the fitness function calling setPheno
        self.pheno = None

    def getFitness(self):
        return self.fitnessFunc(self.chromosome, self.setPheno)

    def calcFitness(self):
        return self.__fitness__

    def getChrom(self):
        return self.chromosome

    def setChrom(self, chromo):
        self.chromosome = chromo

    def setPheno(self,pheno):
        self.pheno = pheno

    def getPheno(self):
        return self.pheno

    def mutate(self, rate):
        for i in range(self.chromLen):
            if random.random() < rate:
                self.chromosome[i] = random.randint(0,255)
