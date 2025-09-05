# import os
# import csv
# import random
# from geneticAlgorithmCore import *
# from geneticAlgorithm_qLearning import genetic_algorithm_qlearning, load_hyperparameters

# RANDOM_SEED = 12345

# def evaluate_all(hyper_file, instances_dir, output_csv):
#     # load all configuration
#     configs = load_hyperparameters(hyper_file)
#     if isinstance(configs, dict):
#         configs = [configs]

#     # load all instances 
#     instances = [os.path.join(instances_dir, f) for f in os.listdir(instances_dir) if f.endswith(".kp")]
#     instances.sort()

#     with open(output_csv, "w", newline="") as f:
#         writer = csv.writer(f)
#         header = ["config_id", "instance", "fitness"] + list(configs[0].keys())
#         writer.writerow(header)

#         for i, cfg in enumerate(configs, start=1):
#             for inst in instances:
#                 print(f"==> Running config {i} on {inst}")

#                 random.seed(RANDOM_SEED)

#                 weights, values, capacity = load_kplib_instance(inst)
#                 problem = KnapsackProblem(weights, values, capacity)

#                 best = genetic_algorithm_qlearning(
#                     problem,
#                     population_size=cfg["population_size"],
#                     generations=cfg["generations"],
#                     mutation_rate=cfg["mutation_rate"],
#                     elitism_size=cfg["elitism_size"],
#                     tournament_size=cfg["tournament_size"],
#                     alpha=cfg["alpha"],
#                     gamma=cfg["gamma"],
#                     epsilon_start=cfg["epsilon_start"],
#                     epsilon_end=cfg["epsilon_end"]
#                 )

#                 row = [i, os.path.basename(inst), best.fitness] + [cfg[k] for k in cfg.keys()]
#                 writer.writerow(row)

#     print(f"✅ Results saved in {output_csv}")


# def main():
#     parser = argparse.ArgumentParser(
#         description="Evaluate Q-learning GA configurations on a set of instances and save results to CSV"
#     )
#     parser.add_argument(
#         "--hyper_file", type=str, required=True,
#         help="Path to the hyperparameter configuration file"
#     )
#     parser.add_argument(
#         "--instances_dir", type=str, required=True,
#         help="Directory containing the .kp problem instances"
#     )
#     parser.add_argument(
#         "--output_csv", type=str, required=True,
#         help="Output CSV file to save results"
#     )

#     args = parser.parse_args()

#     evaluate_all(
#         hyper_file=args.hyper_file,
#         instances_dir=args.instances_dir,
#         output_csv=args.output_csv
#     )

# if __name__ == "__main__":
#     main()



import argparse
import os
import csv
import random
from geneticAlgorithmCore import *
from geneticAlgorithm_qLearning import genetic_algorithm_qlearning
from geneticAlgorithm import genetic_algorithm 

RANDOM_SEED = 12345

def load_hyperparameters(path):
    configs = []
    params = {}

    with open(path, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                if params:  # new config
                    configs.append(params)
                    params = {}
                continue
            if "=" in line:
                key, value = line.split("=")
                key, value = key.strip(), value.strip()
                try:
                    if "." in value:
                        params[key] = float(value)
                    else:
                        params[key] = int(value)
                except ValueError:
                    params[key] = value
        if params:  # last config
            configs.append(params)

    return configs if len(configs) > 1 else configs[0]


def evaluate_qlearning(configs, instances, output_csv):
    with open(output_csv, "w", newline="") as f:
        writer = csv.writer(f)
        header = ["config_id", "instance", "fitness"] + list(configs[0].keys())
        writer.writerow(header)

        for i, cfg in enumerate(configs, start=1):
            for inst in instances:
                print(f"==> Running config {i} on {inst}")

                random.seed(RANDOM_SEED)

                weights, values, capacity = load_kplib_instance(inst)
                problem = KnapsackProblem(weights, values, capacity)

                best = genetic_algorithm_qlearning(
                    problem,
                    population_size=cfg["population_size"],
                    generations=cfg["generations"],
                    mutation_rate=cfg["mutation_rate"],
                    elitism_size=cfg["elitism_size"],
                    tournament_size=cfg["tournament_size"],
                    alpha=cfg["alpha"],
                    gamma=cfg["gamma"],
                    epsilon_start=cfg["epsilon_start"],
                    epsilon_end=cfg["epsilon_end"]
                )

                row = [i, os.path.basename(inst), best.fitness] + [cfg[k] for k in cfg.keys()]
                writer.writerow(row)


def evaluate_ga(configs, instances, output_csv):
    with open(output_csv, "w", newline="") as f:
        writer = csv.writer(f)
        header = ["config_id", "instance", "fitness"] + list(configs[0].keys())
        writer.writerow(header)

        for i, cfg in enumerate(configs, start=1):
            for inst in instances:
                print(f"==> Running config {i} on {inst}")

                random.seed(RANDOM_SEED)

                weights, values, capacity = load_kplib_instance(inst)
                problem = KnapsackProblem(weights, values, capacity)

                best = genetic_algorithm(
                    problem,
                    population_size=cfg["population_size"],
                    generations=cfg["generations"],
                    mutation_rate=cfg["mutation_rate"],
                    elitism_size=cfg["elitism_size"],
                    tournament_size=cfg["tournament_size"]
                )

                row = [i, os.path.basename(inst), best.fitness] + [cfg[k] for k in cfg.keys()]
                writer.writerow(row)

                # print(best.fitness)
                # print(row)


def main():
    parser = argparse.ArgumentParser(
        description="Evaluate GA or Q-learning GA configurations on a set of instances and save results to CSV"
    )
    parser.add_argument("--config_file", type=str, required=True,
                        help="Path to the hyperparameter configuration file")
    parser.add_argument("--instances_dir", type=str, required=True,
                        help="Directory containing the .kp problem instances")
    parser.add_argument("--output_csv", type=str, required=True,
                        help="Output CSV file to save results")
    args = parser.parse_args()

    # load configurations
    configs = load_hyperparameters(args.config_file)
    if isinstance(configs, dict):
        configs = [configs]

    instances = [os.path.join(args.instances_dir, f) for f in os.listdir(args.instances_dir) if f.endswith(".kp")]
    instances.sort()

    if "qLearning" in args.config_file.lower():
        evaluate_qlearning(configs, instances, args.output_csv)
    else:
        evaluate_ga(configs, instances, args.output_csv)


if __name__ == "__main__":
    main()
