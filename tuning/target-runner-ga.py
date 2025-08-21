#!/usr/bin/python
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

import datetime
import os.path
import subprocess
import sys

exe = "python"
script_path = "../src/geneticAlgorithm.py" 

if len(sys.argv) < 5:
    print("\nUsage: ./target-runner-ga.py <configuration_id> <instance_id> <seed> <instance_path_name> <list of parameters>\n")
    sys.exit(1)

configuration_id = sys.argv[1]
instance_id = sys.argv[2]
seed = sys.argv[3]
instance = sys.argv[4]
conf_params = sys.argv[5:]

# Build the command to run your genetic algorithm
command = [exe, script_path, "--instance", instance, "--seed", seed] + conf_params

out_file = f"c{configuration_id}-{instance_id}{seed}.stdout"
err_file = f"c{configuration_id}-{instance_id}{seed}.stderr"

def target_runner_error(msg):
    now = datetime.datetime.now()
    print(str(now) + " error: " + msg)
    sys.exit(1)

outf = open(out_file, "w")
errf = open(err_file, "w")
return_code = subprocess.call(command, stdout=outf, stderr=errf)
outf.close()
errf.close()

if return_code != 0:
    target_runner_error("command returned code " + str(return_code))

if not os.path.isfile(out_file):
    target_runner_error("output file " + out_file  + " not found.")

# Read the cost value from the output file (assumes your script prints only the cost)
with open(out_file) as f:
    cost_line = f.readline().strip()
print(cost_line)

os.remove(out_file)
os.remove(err_file)
sys.exit(0)