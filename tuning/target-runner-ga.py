#!/usr/bin/python3
###############################################################################
# This script is the command that is executed every run.
# PARAMETERS:
# argv[1] is the candidate configuration number
# argv[2] is the instance ID
# argv[3] is the seed
# argv[4] is the instance name
# The rest (argv[5:]) are parameters to the run
# RETURN VALUE:
# This script should print one numerical value: the cost that must be minimized.
# Exit with 0 if no error, with 1 in case of error
###############################################################################


"""
Target runner for iRace to tune the Genetic Algorithm (GA).
It receives configuration parameters from iRace, runs the GA on a given instance,
and outputs the value to be minimized (negative fitness).
"""

import sys
import subprocess
import os
import time


# print(f"DEBUG: args = {sys.argv}", file=sys.stderr)


if len(sys.argv) < 5:
    print("Usage: ./target-runner-ga.py <config_id> <instance_id> <seed> <instance_path> <GA params>")
    sys.exit(1)

script_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../src"))
# ga_script = os.path.join(script_dir, "geneticAlgorithm.py")
ga_script = os.path.join(script_dir, "main.py")


config_id = sys.argv[1]
instance_id = sys.argv[2]
seed = sys.argv[3]
instance_path = sys.argv[4]
conf_params = sys.argv[5:]

# bound_max = int(sys.argv[5])
# conf_params = sys.argv[6:]

population_size = conf_params[0]
generations = conf_params[1]
mutation_rate = conf_params[2]
crossover_op = conf_params[3]
mutation_op = conf_params[4]
elitism_size = conf_params[5]
tournament_size = conf_params[6]

command = [
    "python3", ga_script,
    "--instance", instance_path,
    "--seed", seed,
    "--population_size", str(population_size),
    "--generations", str(generations),
    "--mutation_rate", str(mutation_rate),
    "--crossover_op", str(crossover_op),
    "--mutation_op", str(mutation_op),
    "--elitism_size", str(elitism_size),
    "--tournament_size", str(tournament_size)
]


out_file = f"c{config_id}-{instance_id}-{seed}.stdout"
err_file = f"c{config_id}-{instance_id}-{seed}.stderr"


import signal

# def timeout_handler(signum, frame):
#     print(bound_max)  # penal ako istekne vreme
#     sys.exit(0)

# signal.signal(signal.SIGALRM, timeout_handler)
# signal.alarm(bound_max)


with open(out_file, "w") as outf, open(err_file, "w") as errf:
    # return_code = subprocess.call(command, stdout=outf, stderr=errf, timeout=bound_max)
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
        print(-fitness)  
    except ValueError:
        print(f"Error: could not parse fitness value from output: {line}")
        sys.exit(1)

os.remove(out_file)
os.remove(err_file)

sys.exit(0)