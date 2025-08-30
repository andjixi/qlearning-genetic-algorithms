import argparse
from geneticAlgorithmCore import KnapsackProblem, load_kplib_instance
from geneticAlgorithm import genetic_algorithm
from geneticAlgorithm_qLearning import genetic_algorithm_qlearning
import random

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--instance', type=str, required=True)
    parser.add_argument('--seed', type=int, required=True)
    parser.add_argument('--population_size', type=int, default=50)
    parser.add_argument('--generations', type=int, default=50)
    parser.add_argument('--mutation_rate', type=float, default=0.05)
    parser.add_argument('--crossover_op', type=str, default='single_point')
    parser.add_argument('--mutation_op', type=str, default='bit_flip')
    parser.add_argument('--elitism_size', type=int, default=2)
    parser.add_argument('--tournament_size', type=int, default=3)
    args = parser.parse_args()

    random.seed(args.seed)
    weights, values, capacity = load_kplib_instance(args.instance)
    problem = KnapsackProblem(weights, values, capacity)
    best = genetic_algorithm(
        problem=problem,
        population_size=args.population_size,
        generations=args.generations,
        mutation_rate=args.mutation_rate,
        crossover_op=args.crossover_op,
        mutation_op=args.mutation_op,
        elitism_size=args.elitism_size,
        tournament_size=args.tournament_size
    )
    
    print(best.fitness)

if __name__ == "__main__":
    main()
