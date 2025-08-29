import subprocess
import itertools
import csv

# Q-learning parameter ranges
alphas = [0.1, 0.2, 0.5]
gammas = [0.8, 0.9, 0.99]
epsilon_starts = [0.2, 0.5]
epsilon_ends = [0.02, 0.05]
seeds = [42, 123, 999]

# R-tuned GA configurations
r_configs = [
    {
        "population_size": 111,
        "generations": 483,
        "mutation_rate": 0.0194,
        "crossover_op": "uniform",
        "mutation_op": "swap",
        "elitism_size": 2,
        "tournament_size": 5
    },
    {
        "population_size": 174,
        "generations": 280,
        "mutation_rate": 0.0907,
        "crossover_op": "uniform",
        "mutation_op": "swap",
        "elitism_size": 2,
        "tournament_size": 3
    },
    {
        "population_size": 331,
        "generations": 246,
        "mutation_rate": 0.0551,
        "crossover_op": "single_point",
        "mutation_op": "swap",
        "elitism_size": 1,
        "tournament_size": 3
    },
    #add the rest!   
]

instance_paths = [
    "../instances/test/n00050_R01000_s000.kp",
    "../instances/test/n00100_R01000_s001.kp",
    "../instances/test/n00200_R01000_s002.kp",
    # add more 
]
results = []


for instance_path in instance_paths:
    for config in r_configs:
        for alpha, gamma, eps_start, eps_end in itertools.product(alphas, gammas, epsilon_starts, epsilon_ends):
            for seed in seeds:
                cmd = [
                    "python", "../src/geneticAlgorithm_qLearning.py",
                    "--instance", instance_path,
                    "--seed", str(seed),
                    "--population_size", str(config["population_size"]),
                    "--generations", str(config["generations"]),
                    "--mutation_rate", str(config["mutation_rate"]),
                    "--elitism_size", str(config["elitism_size"]),
                    "--tournament_size", str(config["tournament_size"]),
                    "--alpha", str(alpha),
                    "--gamma", str(gamma),
                    "--epsilon_start", str(eps_start),
                    "--epsilon_end", str(eps_end)
                ]
                try:
                    output = subprocess.check_output(cmd, universal_newlines=True, timeout=300)
                    best_fitness = float(output.strip())
                except Exception as e:
                    best_fitness = None
                    print(f"Run failed: {e}")

                results.append({
                    "instance": instance_path,
                    "population_size": config["population_size"],
                    "generations": config["generations"],
                    "mutation_rate": config["mutation_rate"],
                    "crossover_op": config["crossover_op"],
                    "mutation_op": config["mutation_op"],
                    "elitism_size": config["elitism_size"],
                    "tournament_size": config["tournament_size"],
                    "alpha": alpha,
                    "gamma": gamma,
                    "epsilon_start": eps_start,
                    "epsilon_end": eps_end,
                    "seed": seed,
                    "best_fitness": best_fitness
                })

with open("qlearning_tuning_results.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=results[0].keys())
    writer.writeheader()
    writer.writerows(results)

print("Tuning complete. Results saved to qlearning_tuning_results.csv.")