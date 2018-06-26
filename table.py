class Table:
    knapsack_size = 50

    def __init__(self):
        self.table = []
        with open('data.csv', 'r') as file:
            header = True
            for line in file:
                if header is True:
                    header = False
                    continue

                id, name, size = line.strip().split(',')
                self.table.append({'id': id, 'name': name, 'size': int(size)})

    def get_fitness(self, dna_sequence):
        """ Evaluate the fitness of a given DNA Sequence

        In our simple problem, the fitness is evaluated as:
            - If sum <= knapsack_size:
                sum / knapsack_size
            - If sum > knapsack_size:
                (knapsack_size - (2 * how_much_sum_went_over_knapsack_size)) / knapsack_size
        
        return fitness, valid_value
        *** invalid values cannot be used as BSSF
        """
        NEGATIVE_MULTIPLIER = 2

        # Calculate sum
        sum = 0
        for index, element in enumerate(str(dna_sequence)):
            if element == '1':
                sum += self.table[index]['size']
            
        print("sum:", sum)
        
        # calculate fitness
        if sum <= self.knapsack_size:
            valid_value = True
            return sum / self.knapsack_size, valid_value
        else:
            valid_value = False
            overflow = sum % self.knapsack_size
            overflow_punishment = NEGATIVE_MULTIPLIER * overflow

            return (self.knapsack_size - overflow_punishment) / float(self.knapsack_size), valid_value
