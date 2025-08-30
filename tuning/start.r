# library("irace")
# setwd("~/Desktop/tuning_avrp/")
# parameters <- readParameters("parameters.txt")
# scenario <- readScenario(filename = "scenario.txt",
#                          scenario = defaultScenario())
# irace(scenario = scenario, parameters = parameters)

library("irace")

if (!exists("use_qlearning")) {
    use_qlearning <- FALSE
}

if (use_qlearning) {
    cat("==> Pokrećem GA + Q-learning verziju\n")
    scenario <- readScenario(filename = "scenario-qLearning.txt")
} else {
    cat("==> Pokrećem obični GA\n")
    scenario <- readScenario(filename = "scenario-ga.txt")
}


results <- irace(scenario = scenario)

print(results$eliteConfigurations)