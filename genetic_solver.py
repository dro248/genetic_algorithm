from table import Table
import random

class GeneticSolver:
    population_size = 50000
    population = set()
    bssf = "0" * 26
    bssf_count = 0
    max_cycles = 1000
    stop = False


    def __init__(self, table):
        self.table = table
        self.generate_random_population()
        print("Random Population Generated!")
        print()
    
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
            sum += self.table.get_fitness(element)[0]
        return sum / float(self.population_size)

    def get_and_remove_random_entity_from_population(self):
        # Careful: Sometimes the size of the population will be 999... not 1000
        rand_index = random.randint(0, self.population_size-2)
        random_entity = list(self.population)[rand_index]
        self.population.remove(random_entity)
        return random_entity

    def create_child(self, parent1, parent2):
        # Crossover 
        child = self.get_crossover(parent1, parent2)

        # Mutuate
        mutated_child = self.get_mutation(child)
        
    def get_crossover(self, parent1, parent2):
        crossover_point = random.randint(1, len(parent1)-2)
        child = parent1[:crossover_point] + parent2[crossover_point:]
        return child
    
    def mutate_flag(self):
        return True if random.randint(1, self.table.get_string_length()-1) < 2 else False
        
    def get_mutation(self, dna_sequence):
        seq_list = list(dna_sequence)

        for index, letter in enumerate(seq_list):
            # We want the mutation to be based on a probability 
            if self.mutate_flag() is True:
                # flip the bit
                seq_list[index] = '1' if (letter is '0') else '0'
        
        mutated_sequence = "".join(seq_list)

        if self.table.get_fitness(mutated_sequence)[1] is True:
            print("Mutated sequence: ", mutated_sequence)
            print("Mutated seq is valid: ", self.table.get_fitness(mutated_sequence)[1])
            print("Mutated seq fitness: ", self.table.get_fitness(mutated_sequence)[0])

        return mutated_sequence
    
    def update_stopping_criteria(self):
        self.bssf_count += 1
        if self.bssf_count >= self.max_cycles:
            self.stop = True

    def update_bssf(self):
        tmp_best_sequence = self.bssf
        tmp_best_fitness, tmp_valid = self.table.get_fitness(tmp_best_sequence)

        # Find the best solution
        for item_sequence in self.population:
            item_fitness, item_valid = self.table.get_fitness(item_sequence)
            if item_valid and (item_fitness > tmp_best_fitness):
                tmp_best_sequence = item_sequence
                tmp_best_fitness = item_fitness

        # if tmp_best_sequence is different than self.bssf, reset self.bssf_count
        if (tmp_best_sequence != self.bssf) and tmp_valid:
            self.bssf = tmp_best_sequence
            self.bssf_count = 0
            print("Updated BSSF: ", self.bssf, str(self.table.get_fitness(self.bssf)[0]))
    
    def validate_population(self):
        valid_pop = False
        
        while not valid_pop:
            try:
                self.population.remove(None)
            except KeyError:
                pass
            self.generate_random_population()
            
            valid_pop = False if (None in self.population) else True 

    def run(self):
        """ Navigate the solution space using:

            * Tournament Selection
            * Crossover + Mutation
            * Tournament Population Placement
        """
        
        while not self.stop:
            # print(self.table.get_fitness(self.bssf))

            # Get 2 parents
            parent1 = self.get_and_remove_random_entity_from_population()
            parent2 = self.get_and_remove_random_entity_from_population()

            # Create 2 children
            child1 = self.create_child(parent1, parent2)
            child2 = self.create_child(parent1, parent2)

            mating_pool = [
                {'sequence': parent1, 'fitness': self.table.get_fitness(parent1) },
                {'sequence': parent2, 'fitness': self.table.get_fitness(parent2) },
                {'sequence': child1, 'fitness': self.table.get_fitness(child1) },
                {'sequence': child2, 'fitness': self.table.get_fitness(child2) }
            ]

            # Add the top two contenders back into the population (throw away the others)
            top1, top2, _, _ = sorted(mating_pool, key=lambda k: k['fitness'][0], reverse=True)
            
            self.population.add(top1['sequence'])
            self.population.add(top2['sequence'])

            # If for some strange reason population still isn't full, top it off
            self.generate_random_population()

            # Update bssf and stopping_criteria
            self.update_bssf()
            self.update_stopping_criteria()

            # print("Mean Fitness: {f}".format(f=str(self.get_population_mean_fitness())))
            print("Best solution: ", self.bssf)
            print("Best Fitness: ", str(self.table.get_fitness(self.bssf)))
            print('+'*30)
            # print("Population Size:", str(len(self.population)))

            # print("BSSF is valid: ", (self.table.get_fitness(self.bssf)[1]))

            self.validate_population()

        if self.stop:
            print("Best solution: ", self.bssf)
            print("Best Fitness: ", str(self.table.get_fitness(self.bssf)))
        


GeneticSolver(Table()).run()
