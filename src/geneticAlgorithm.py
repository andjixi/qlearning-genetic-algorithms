from geneticAlgorithmCore import *

def genetic_algorithm(
    problem: KnapsackProblem,
    population_size=50,
    generations=50,
    tournament_size=3,
    mutation_rate=0.05,
    elitism_size=2,
    crossover_op='single_point',        # choose: 'single_point', 'two_point', 'uniform'
    mutation_op='bit_flip'              # choose: 'bit_flip', 'swap', 'scramble'
):
    population = [Individual(problem) for _ in range(population_size)]

    crossover_ops = {
        'single_point': single_point_crossover,
        'two_point': two_point_crossover,
        'uniform': uniform_crossover,
        'arithmetic': arithmetic_crossover
    }

    mutation_ops = {
        'bit_flip': lambda ind: bit_flip_mutation(ind, mutation_rate),
        'swap': swap_mutation,
        'scramble': scramble_mutation
    }

    crossover_func = crossover_ops[crossover_op]
    mutation_func = mutation_ops[mutation_op]

    # # track progress
    # best_per_gen = []

    for _ in range(generations):
        population.sort(key=lambda ind: ind.fitness, reverse=True)
        # best_per_gen.append(population[0].fitness)

        new_population = population[:elitism_size]

        while len(new_population) < population_size:
            parent1 = selection(population, tournament_size)
            parent2 = selection(population, tournament_size)
            child1, child2 = crossover_func(parent1, parent2)

            mutation_func(child1)
            mutation_func(child2)

            child1.fitness = child1.evaluate_fitness()
            child2.fitness = child2.evaluate_fitness()

            new_population.extend([child1, child2])

        population = new_population[:population_size]

    return max(population, key=lambda ind: ind.fitness)
    # best_ind = max(population, key=lambda ind: ind.fitness)

    # return best_ind, best_per_gen