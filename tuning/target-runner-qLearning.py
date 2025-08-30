#!/usr/bin/python3
import sys
import subprocess
import os

if len(sys.argv) < 9:
    print("Usage: ./target-runner-qLearning.py <config_id> <instance_id> <seed> <instance_path> <GA params> <alpha> <gamma> <epsilon_start> <epsilon_end>")
    sys.exit(1)

script_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../src"))
ga_script = os.path.join(script_dir, "geneticAlgorithm_qLearning.py")

config_id = sys.argv[1]
instance_id = sys.argv[2]
seed = sys.argv[3]
instance_path = sys.argv[4]
conf_params = sys.argv[5:] 

population_size = conf_params[0]
generations = conf_params[1]
mutation_rate = conf_params[2]
elitism_size = conf_params[3]
tournament_size = conf_params[4]
alpha = conf_params[5]
gamma = conf_params[6]
epsilon_start = conf_params[7]
epsilon_end = conf_params[8]

# # FORBIDDEN RULE 
# if float(epsilon_start) < float(epsilon_end):
#     sys.exit(0)

command = [
    "python3", ga_script,
    "--instance", instance_path,
    "--seed", seed,
    "--population_size", str(population_size),
    "--generations", str(generations),
    "--mutation_rate", str(mutation_rate),
    "--elitism_size", str(elitism_size),
    "--tournament_size", str(tournament_size),
    "--alpha", str(alpha),
    "--gamma", str(gamma),
    "--epsilon_start", str(epsilon_start),
    "--epsilon_end", str(epsilon_end)
]


out_file = f"c{config_id}-{instance_id}-{seed}.stdout"
err_file = f"c{config_id}-{instance_id}-{seed}.stderr"

with open(out_file, "w") as outf, open(err_file, "w") as errf:
    return_code = subprocess.call(command, stdout=outf, stderr=errf)

if return_code != 0:
    print(f"Error: command returned code {return_code}")
    sys.exit(1)

if not os.path.isfile(out_file):
    print(f"Error: output file {out_file} not found")
    sys.exit(1)

with open(out_file) as f:
    line = f.readline().strip()
    try:
        fitness = float(line)
        print(-fitness)  # iRace minimizes
    except ValueError:
        print(f"Error: could not parse fitness value from output: {line}")
        sys.exit(1)

os.remove(out_file)
os.remove(err_file)
sys.exit(0)
