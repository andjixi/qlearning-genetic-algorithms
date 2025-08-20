library("irace")
setwd("~/Desktop/tuning_avrp/")
parameters <- readParameters("parameters.txt")
scenario <- readScenario(filename = "scenario.txt",
                         scenario = defaultScenario())
irace(scenario = scenario, parameters = parameters)
