using CSV
using JuMP
using CPLEX
using DataFrames
using Random

include("functions.jl")


# Set to "titanic" to consider the corresponding dataset
dataSet = "adult"
dataFolder = "../data/"
resultsFolder = "../res/"

# Create the features tables (or load them if they already exist)
# Note: each line corresponds to an individual, the 1st column of each table contain the class
# Details:
# - read the file ./data/adult.csv
# - save the features in ./data/adult_test.csv and ./data/adult_train.csv
#
# Warning: this step is skipped if files adult_test.csv and adult_train.csv already exist
train, test = createFeatures(dataFolder, dataSet)

# Create the rules (or load them if they already exist)
# Note: each line corresponds to a rule, the first column corresponds to the class
# Details:
# - read the file ./data/kidney_train.csv
# - save the rules in ./res/kidney_rules.csv
#
# Warning: this step is skipped if file kidney_rules.csv already exists

@time rules = createRules(dataSet, resultsFolder, train)

#println(rules)
# Order the rules (limit the resolution to 300 seconds)
# Details:
# - read the file ./data/kidney_rules.csv
# - save the rules in ./res/kidney_ordered_rules.csv
#
# Warning: this step is skipped if file kidney_ordered_rules.csv already exists
timeLimitInSeconds = 300
@time orderedRules = sortRules(dataSet, resultsFolder, train, rules, timeLimitInSeconds)

println("-- Train results")
showStatistics(orderedRules, train)

println("-- Test results")
showStatistics(orderedRules, test)
