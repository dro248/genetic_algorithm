from table import Table
import random

class GeneticSolver:
    population_size = 1000
    population = set()
    bssf = None

    def __init__(self, table):
        self.table = table
        self.generate_random_population()
    
    def generate_random_population(self):
       while len(self.population) < self.population_size:
           self.population.add(self.generate_random_dna_sequence())
    
    def generate_random_dna_sequence(self):
        dna_length = len(self.table.table)
        my_sequence = ""

        for i in range(dna_length):
            my_sequence += str(random.randint(0,1))
        return my_sequence
    
    def get_population_mean_fitness(self):
        sum = 0
        for element in self.population:
            sum += self.table.get_fitness(element)
        return sum / float(self.population_size)

    def evolve(self):
        """ Navigate the solution space using:

            * Tournament Selection
            * Crossover + Mutation
            * Tournament Population Placement
        """

GeneticSolver(Table())