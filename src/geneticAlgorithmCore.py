import random
import argparse


class KnapsackProblem:
    def __init__(self, weights, values, capacity):
        self.weights = weights
        self.values = values
        self.capacity = capacity
        self.num_items = len(weights)

class Individual:
    def __init__(self, problem: KnapsackProblem):
        self.problem = problem
        self.genotype = [random.random() < 0.5 for _ in range(problem.num_items)]
        self.fitness = self.evaluate_fitness()

    def evaluate_fitness(self):
        total_weight = 0
        total_value = 0

        for i, bit in enumerate(self.genotype):
            if bit:
                total_weight += self.problem.weights[i]
                total_value += self.problem.values[i]

        if total_weight > self.problem.capacity:
            return -1

        return total_value
    

# Crossover Operators
def arithmetic_crossover(p1, p2, alpha=None):
    if alpha is None:
        alpha = random.random()

    child1 = Individual(p1.problem)
    child2 = Individual(p2.problem)

    child1.genotype = [
        bool(round(alpha * g1 + (1 - alpha) * g2))
        for g1, g2 in zip(p1.genotype, p2.genotype)
    ]
    child2.genotype = [
        bool(round(alpha * g2 + (1 - alpha) * g1))
        for g1, g2 in zip(p1.genotype, p2.genotype)
    ]

    return child1, child2

def single_point_crossover(p1, p2):
    point = random.randint(1, len(p1.genotype) - 1)

    child1 = Individual(p1.problem)
    child2 = Individual(p2.problem)

    child1.genotype = p1.genotype[:point] + p2.genotype[point:]
    child2.genotype = p2.genotype[:point] + p1.genotype[point:]

    return child1, child2

def two_point_crossover(p1, p2):
    a, b = sorted(random.sample(range(len(p1.genotype)), 2))

    child1 = Individual(p1.problem)
    child2 = Individual(p2.problem)

    child1.genotype = (
        p1.genotype[:a] + p2.genotype[a:b] + p1.genotype[b:]
    )
    child2.genotype = (
        p2.genotype[:a] + p1.genotype[a:b] + p2.genotype[b:]
    )

    return child1, child2

def uniform_crossover(p1, p2):
    child1 = Individual(p1.problem)
    child2 = Individual(p2.problem)

    child1.genotype = []
    child2.genotype = []

    for bit1, bit2 in zip(p1.genotype, p2.genotype):
        if random.random() < 0.5:
            child1.genotype.append(bit1)
            child2.genotype.append(bit2)
        else:
            child1.genotype.append(bit2)
            child2.genotype.append(bit1)

    return child1, child2


# Selection operators
def selection(population, tournament_size):
    candidates = random.sample(population, tournament_size)
    return max(candidates, key=lambda ind: ind.fitness)


# Mutation Operators
def bit_flip_mutation(individual, mutation_rate):
    for i in range(len(individual.genotype)):
        if random.random() < mutation_rate:
            individual.genotype[i] = not individual.genotype[i]
    # individual.fitness = individual.evaluate_fitness()

def swap_mutation(individual):
    idx1, idx2 = random.sample(range(len(individual.genotype)), 2)
    individual.genotype[idx1], individual.genotype[idx2] = individual.genotype[idx2], individual.genotype[idx1]
    # individual.fitness = individual.evaluate_fitness()

def scramble_mutation(individual):
    start, end = sorted(random.sample(range(len(individual.genotype)), 2))
    subseq = individual.genotype[start:end]
    random.shuffle(subseq)
    individual.genotype[start:end] = subseq
    # individual.fitness = individual.evaluate_fitness()




def load_kplib_instance(path):
    with open(path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]  

    n = int(lines[0])           
    capacity = int(lines[1])   

    weights = []
    values = []

    for line in lines[2:2+n]:
        w, v = map(int, line.split())
        weights.append(w)
        values.append(v)

    return weights, values, capacity