# library("irace")
# setwd("~/Desktop/tuning_avrp/")
# parameters <- readParameters("parameters.txt")
# scenario <- readScenario(filename = "scenario.txt",
#                          scenario = defaultScenario())
# irace(scenario = scenario, parameters = parameters)

library("irace")
# parameters <- readParameters("parameters.txt")
scenario <- readScenario(filename = "scenario.txt")

results <- irace(scenario = scenario)

print(results$eliteConfigurations)