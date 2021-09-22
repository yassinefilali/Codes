# Tolerance
epsilon = 0.0001

"""
Function used to transform a column with numerical values into one or several binary columns.

Arguments:
 - data: table which contains the column that will be binarized (1 row = 1 individual, 1 column = 1 feature);
 - header: header of the column of data that will be binarized
 - intervals: array of values which delimits the binarization (ex : [2, 4, 6, 8] will lead to 3 columns respectively equal to 1 if the value of column "header" is in [2, 3], [4, 5] and [6, 7])

 Example:
  createColumns(:Age, [1, 17, 50, Inf], data, features) will create 3 binary columns in features named "Age1-16", "Age17-49", "Age50-Inf"
"""
function createColumns(header::Symbol, intervals, data::DataFrames.DataFrame, features::DataFrames.DataFrame)
    for i in 1:size(intervals, 1) - 1
        lb = intervals[i]
        ub = intervals[i+1]
        features[!, Symbol(header, lb, "-", (ub-1))] = ifelse.((data[!, header] .>= lb) .& (data[!, header] .< ub), 1, 0) 
    end
end

"""
Create the train and test csv files of a data set

Arguments:
 - dataFolder: folder which contains the data set csv file (ex: "./data")
 - dataSet: name of the data set (ex: "titanic")

Important remark: the first column of the output files must correspond to the class of each individual (and it must be 0 or 1)
"""
function createFeatures(dataFolder::String, dataSet::String)

    # Get the input file path
    rawDataPath = dataFolder * dataSet * ".csv"

    # Test its existence
    if !isfile(rawDataPath)
        println("Error in createFeatures: Input file not found: ", rawDataPath)
        return
    end

    # Put the data in a DataFrame variable
    rawData = CSV.File(rawDataPath,  header=true) |> DataFrame

    # Output files path
    trainDataPath = dataFolder * dataSet * "_train.csv"
    testDataPath = dataFolder * dataSet * "_test.csv"

    # If the train or the test file do not exist
    if !isfile(trainDataPath) || !isfile(testDataPath)

        # Shuffle the individuals rawData
        rawData = rawData[shuffle(1:size(rawData, 1)),:]

        # Percentage of data in the train set
        trainPercentage = 2/3

        if dataSet == "adult"
            trainPercentage = 1/32
        end

        # Get the rawDatas which are in the train set 
        # (trainRawData can be used to chose select the features)
        trainLimit = trunc(Int, size(rawData, 1) * trainPercentage)
        trainRawData = rawData[1:trainLimit, :]

        println("=== Creating the features")

        # Create the table that will contain the features
        features::DataFrame = DataFrames.DataFrame()
        
        # Create the features of the titanic data set
        if dataSet == "titanic"

            # Add the column related to the class (always do it first!)
            # Remark: here the rawData already contain 0/1 values so no change needed
            features.Survived = rawData.Survived

            #### First example of the binarization of a column with numerical values
            # Add columns related to the ages
            # -> 3 columns ([0, 16], [17, 49], [50, +infinity[)
            # Ex : if the age is 20, the value of these 3 columns will be 0, 1 and 0, respectively.
            createColumns(:Age, [0, 17, 50, Inf], rawData, features)
            
            # Add columns related to the fares
            # -> 3 columns ([0, 9], [10, 19], [20, +infinity[)
            createColumns(:Fare,  [0, 10, 20, Inf], rawData, features)
            
            #### First example of the binarization of a column with categorical values
            # Add 1 column for the sex (female or not)
            # Detailed description of the command:
            # - create in DataFrame "features" a column named "Sex"
            # - for each row of index i of "rawData", if column "Sex" is equal to "female", set the value of column "Sex" in row i of features to 1; otherwise set it to 0
            features.Sex = ifelse.(rawData.Sex .== "female", 1, 0)
            
            # Add columns related to the passenger class
            # -> 3 columns (class 1, class 2 and class 3)
            
            # For each existing value in the column "Pclass"
            for a in sort(unique(rawData.Pclass))

                # Create 1 feature column named "Class1", "Class2" or "Class3"
                features[!, Symbol("Class", a)] = ifelse.(rawData.Pclass .<= a, 1, 0)
            end

            # Add a column related  to the number of relatives
            # -> 1 column (0: no relatives, 1: at least one relative)
            features.Relative = ifelse.(rawData[!, Symbol("Siblings/Spouses Aboard")] + rawData[!, Symbol("Parents/Children Aboard")] .> 0, 1, 0)

        end

        if dataSet == "adult"
#####################################################################################################################################
            # Warning: this must remain the first column added to features
            features.income = ifelse.(rawData.income .== " <=50K", 0, 1)

            #features 
            features.sex = ifelse.(rawData.sex .== " Female", 1, 0)		
            createColumns(:age, [0.0,20.0, 30.0, 45.0, Inf], rawData, features)
            createColumns(:education_num, [0.0, 9.0, 12.0, Inf], rawData, features)
            createColumns(:hours_per_week, [0.0, 20.0, 30.0,40.0,50.0, Inf], rawData, features)
            #createColumns(:fnlwgt, [0, 40000, 80000,120000, Inf], rawData, features)
            features.capital_gain = ifelse.(rawData.capital_gain .< 5000.0, 1, 0)
            #features.exec = ifelse.(rawData.occupation .==  " Exec-managerial" , 1, 0)
            #features.Prof = ifelse.(rawData.occupation .==  " Prof-specialty" , 1, 0)
            #features.sales = ifelse.(rawData.occupation .==  " Sales" , 1, 0)
            #features.rep = ifelse.(rawData.occupation .==  " Craft-repair" , 1, 0)
            

            #for a in sort(unique(rawData.workclass))
                #str = "workclass_"+a
            #   features[!, Symbol("Class", a)] = ifelse.(rawData.workclass .== a, 1, 0)
            #end

            #for a in sort(unique(rawData.relationship))
            #    features[!, Symbol("Class1", a)] = ifelse.(rawData.education .== a, 1, 0)
            #  end

            #for a in sort(unique(rawData.native_country))
                #features[!, Symbol("Class", a)] = ifelse.(rawData.native_country .== a, 1, 0)
                #end



        end
#####################################################################################################################################
        # Shuffle the individuals
        features = features[shuffle(1:size(features, 1)),:]

        # Split them between train and test sets
        train = features[1:trainLimit, :]
        test = features[(trainLimit+1):end, :]
        
        CSV.write(trainDataPath, train)
        CSV.write(testDataPath, test)

    # If the train and test file already exist
    else
        println("=== Warning: Existing features found, features creation skipped")
        println("=== Loading existing features")
        train = CSV.File(trainDataPath) |> DataFrame
        test = CSV.File(testDataPath) |> DataFrame
    end
    
    println("=== ... ", size(train, 1), " individuals in the train set")
    println("=== ... ", size(test, 1), " individuals in the test set")
    println("=== ... ", size(train, 2), " features")
    
    return train, test
end 


"""
Create the association rules related to a training set

Arguments
 - dataSet: name of the data ste
 - resultsFolder: name of the folser in which the rules will be written
 - train: DataFrame with the training set (each line is an individual, the first column is the class, the other are the features)

Output
 - table of rules (each line is a rule, the first column corresponds to the rules class)
"""
function createRules(dataSet::String, resultsFolder::String, train::DataFrames.DataFrame)

    # Create the result folder if necessary
    if !isdir(resultsFolder)
        mkdir(resultsFolder)
    end

    # Output file
    rulesPath = resultsFolder * dataSet * "_rules.csv"
    rules = DataFrame()

    if !isfile(rulesPath)

        println("=== Generating the rules")

        # Transactions
        t::DataFrame = train[:, 2:end]

        # Class of the transactions
        # Help: to get the class of transaction nb i:
        # - do not use: transactionClass[i]
        # - use: transactionClass[i, 1]
        transactionClass::DataFrame = train[:, 1:1]

        # Number of features
        d::Int64 = size(t, 2)

        # Number of transactions
        n::Int64 = size(t, 1)

        mincovy::Float64 = 0.05
        iterlim::Int64 = 5
        RgenX::Float64 = 0.1 / n
        RgenB::Float64 = 0.1 / (n * d)
        
        ##################
        # Find the rules for each class
        ##################
#####################################################################################################################################"
        for y = 0:1
            println("-- Classe $y")
            P = Model(CPLEX.Optimizer)
            set_optimizer_attribute(P, "CPX_PARAM_SCRIND", 0)
            #rules = DataFrame()
            s = 0
            iter=1
            cmax=n
            @variable(P,x[i in 1:n], Bin)
            @variable(P,b[i in 1:d], Bin)
            @constraint(P, [i=1:n,j=1:d], x[i] <= 1+(t[i,j]-1)*b[j])
            @constraint(P, [i=1:n], x[i] >= 1 + sum((t[i,j]-1)*b[j] for j=1:d))
            
            @objective(P, Max, sum(x[i] for i=1:n if transactionClass[i, 1]==y)-RgenX*sum(x[i] for i=1:n)-RgenB*sum(b[j] for j=1:d) )

            while (cmax >=n* mincovy)
                if iter==1
                    @constraint(P, sum(x[i] for i=1:n) <= cmax)
                    optimize!(P)
                    #println(JuMP.value.(b))
                    B = trunc.(Int, JuMP.value.(b))
                    X = trunc.(Int, JuMP.value.(x))
                    s = sum(X[i] for i=1:n if transactionClass[i,1]==y)
                    iter=iter+1
                end
                ## Ajouter la règle à l'ensemble des règles
                B = trunc.(Int, JuMP.value.(b))
                rule = DataFrame(hcat(append!([y], B)...), :auto)
                append!(rules, rule)
                #println(B)
                
                ## 
                ## Add constraint
                @constraint(P,  sum( b[j] for j = 1:d if B[j] == 0) + sum(1-b[j] for j = 1:d if B[j] == 1) >=1  )
                ## 
                if iter < iterlim
                    optimize!(P)
                    B = trunc.(Int, JuMP.value.(b))
                    X = trunc.(Int, JuMP.value.(x))
                    stemp = sum(X[i] for i=1:n if transactionClass[i, 1]==y)
                    if stemp < s
                        cmax = min(cmax-1, sum(X[i] for i=1:n))
                        iter = 1
                    else
                        iter = iter + 1
                    end
                else
                    cmax = cmax - 1
                    iter = 1

                        
                end
                #println("#################################",iter)
            end



            

            ## Hint 1 
            # Each time you solve the model for a class y, the value of variable b represents a rule.
            # To convert the value of b into a DataFrame, you can use the following instruction: 
            # rule = DataFrame(hcat(append!([y], trunc.(Int, JuMP.value.(b)))...), :auto)
            #
            #       Here are some explanations (optional):
            #       - trunc.(Int, JuMP.value.(b)): get the value of b in the current solution and truncate it.
            #       - append!([y], x): add y at the beginning of vector x
            #       - hcat(x...): convert vector x into a matrix in which the only line corresponds to x
            #       - DataFrame(x, :auto): convert a matrix into a data frame
            #
            # The rule can then be appended to rules:
            # append!(rules, rule)
            
        end
#####################################################################################################################################"
        CSV.write(rulesPath, rules)

    else
        println("=== Warning: Existing rules found, rules creation skipped")
        println("=== Loading the existing rules")
        rules = CSV.File(rulesPath) |> DataFrame
    end
    
    println("=== ... ", size(rules, 1), " rules obtained") 

    return rules
end

"""
Sort the rules

Arguments
  - dataSet: name of the dataset folder
  - resultsFolder: name of the folder in which the results are written
  - train: train data set (1 row = 1 individual)
      - rules: rules which must be sorted (1 ro = 1 rule)
  - tilim: maximal running time of CPLEX in seconds
"""
function sortRules(dataSet::String, resultsFolder::String, train::DataFrames.DataFrame, rules::DataFrames.DataFrame, tilim::Int64)

    orderedRulesPath = resultsFolder * dataSet * "_ordered_rules.csv"

    if !isfile(orderedRulesPath)

        println("=== Sorting the rules")
        
        # Transactions
        t = train[:, 2:end]

        # Class of the transactions
        transactionClass = train[:, 1:1]

        # Number of features
        d = size(t, 2)

        # Number of transactions
        n = size(t, 1)

        # Add the two null rules in first position
        nullrules = similar(rules, 0)
        push!(nullrules, append!([0], zeros(d)))
        push!(nullrules, append!([1], zeros(d)))
        rules = vcat(nullrules, rules)

        # Remove duplicated rules
        rules = unique(rules)

        # Number of rules
        L = size(rules)[1]

        Rrank = 1/L

        ################
        # Compute the v_il and p_il constants
        # p_il = :
        #  0 if rule l does not apply to transaction i
        #  1 if rule l applies to transaction i and   correctly classifies it
        # -1 if rule l applies to transaction i and incorrectly classifies it
        ################
        p = zeros(n, L)

        # For each transaction and each rule
        for i in 1:n
            for l in 1:L

                # If rule l applies to transaction i
                # i.e., if the vector t_i - r_l does not contain any negative value
                if !any(x->(x<-epsilon), [sum(t[i, k]-rules[l, k+1]) for k in 1:d])

                    # If rule l correctly classifies transaction i
                    if transactionClass[i, 1] == rules[l, 1]
                        p[i, l] = 1
                    else
                        p[i, l] = -1 
                    end
                end
            end
        end

        v = abs.(p)

        ################
        # Create and solve the model
        ###############
        #CPX_PARAM_SCRIND=0
        m = Model(CPLEX.Optimizer)
        set_optimizer_attribute(m, "CPX_PARAM_SCRIND", 0)
        set_optimizer_attribute(m, "CPX_PARAM_TILIM", tilim)
        
        # u_il: rule l is the highest which applies to transaction i
        @variable(m, u[1:n, 1:L], Bin)

        # r_l: rank of rule l
        @variable(m, 1 <= r[1:L] <= L, Int)

        # rstar: rank of the highest null rule
        @variable(m, 1 <= rstar <= L)
        @variable(m, 1 <= rB <= L)

        # g_i: rank of the highest rule which applies to transaction i
        @variable(m, 1 <= g[1:n] <= L, Int)

        # s_lk: rule l is assigned to rank k
        @variable(m, s[1:L,1:L], Bin)

        # Rank of null rules
        rA = r[1]
        rB = r[2]

        # rstar == rB?
        @variable(m, alpha, Bin)

        # rstar == rA?
        @variable(m, 0 <= beta <= 1)

        # Maximize the classification accuracy
        @objective(m, Max, sum(p[i, l] * u[i, l] for i in 1:n for l in 1:L)
                   + Rrank * rstar)

        # Only one rule is the highest which applies to transaction i
        @constraint(m, [i in 1:n], sum(u[i, l] for l in 1:L) == 1)

        # g constraints
        @constraint(m, [i in 1:n, l in 1:L], g[i] >= v[i, l] * r[l])
        @constraint(m, [i in 1:n, l in 1:L], g[i] <= v[i, l] * r[l] + L * (1 - u[i, l]))

        # Relaxation improvement
        @constraint(m, [i in 1:n, l in 1:L], u[i, l] >= 1 - g[i] + v[i, l] * r[l])
        @constraint(m, [i in 1:n, l in 1:L], u[i, l] <= v[i, l]) 

        # r constraints
        @constraint(m, [k in 1:L], sum(s[l, k] for l in 1:L) == 1)
        @constraint(m, [l in 1:L], sum(s[l, k] for k in 1:L) == 1)
        @constraint(m, [l in 1:L], r[l] == sum(k * s[l, k] for k in 1:L))

        # rstar constraints
        @constraint(m, rstar >= rA)
        @constraint(m, rstar >= rB)
        @constraint(m, rstar - rA <= (L-1) * alpha)
        @constraint(m, rA - rstar <= (L-1) * alpha)
        @constraint(m, rstar - rB <= (L-1) * beta)
        @constraint(m, rB - rstar <= (L-1) * beta)
        @constraint(m, alpha + beta == 1)

        # u_il == 0 if rstar > rl (also improve relaxation)
        @constraint(m, [i in 1:n, l in 1:L], u[i, l] <= 1 - (rstar - r[l])/ (L - 1))

        status = optimize!(m)

        ###############
        # Write the rstar highest ranked rules and their corresponding class
        ###############

        # Number of rules kept in the classifier
        # (all the rules ranked lower than rstar are removed)
        relevantNbOfRules=L-trunc(Int, JuMP.value(rstar))+1

        # Sort the rules and their class by decreasing rank
        rulesOrder = JuMP.value.(r)
        orderedRules = rules[sortperm(L.-rulesOrder), :]

        orderedRules = orderedRules[1:relevantNbOfRules, :]

        CSV.write(orderedRulesPath, orderedRules)

    else
        println("=== Warning: Sorted rules found, sorting of the rules skipped")
        println("=== Loading the sorting rules")
        orderedRules = CSV.File(orderedRulesPath) |> DataFrame
    end 

    return orderedRules

end

"""
Compute for a given data set the precision and the recall of 
- each class
- the whole data set (with and without weight for each class)

Arguments
  - orderedRules: list of rules of the classifier (1st row = 1st rule to test)
  - dataset: the data set (1 row = 1 individual)
"""
function showStatistics(orderedRules::DataFrames.DataFrame, dataSet::DataFrames.DataFrame)

    
    # Number of transactions
    n = size(dataSet, 1)

    # Statistics with respect to class 0:
    # - true positive;
    # - true negative;
    # - false positive;
    # - false negative
    tp::Int = 0
    fp::Int = 0
    fn::Int = 0
    tn::Int = 0

    # Number of individuals in each class
    classSize = Array{Int, 1}([0, 0])
    
    # For all transaction i in the data set
    for i in 1:n

        # Get the first rule satisfied by transaction i
        ruleId = findfirst(all, collect(eachrow(Array{Float64, 2}(orderedRules[:, 2:end])  .<= Array{Float64, 2}(DataFrame(dataSet[i, 2:end])))))

        # If transaction i is classified correctly (i.e., if it is a true)
        if orderedRules[ruleId, 1] == dataSet[i, 1]

            # If transaction i is of class 0
            if dataSet[i, 1] == 0
                tp += 1
                classSize[1] += 1
            else
                tn += 1
                classSize[2] += 1
            end 

            # If it is a negative
        else

            # If transaction i is of class 0
            if dataSet[i, 1] == 0
                fn += 1
                classSize[1] += 1
            else
                fp += 1
                classSize[2] += 1
            end 
        end
    end

    precision = Array{Float64, 1}([tp / (tp+fp), tn / (tn+fn)])
    recall = Array{Float64, 1}([tp / (tp + fn), tn / (tn + fp)])

        @show tp, fp, tn, fn
        @show precision, recall, classSize
    println("Class\tPrec.\tRecall\tSize")
    println("0\t", round(precision[1], digits=2), "\t", round(recall[1], digits=2), "\t", classSize[1])
    println("1\t", round(precision[2], digits=2), "\t", round(recall[2], digits=2), "\t", classSize[2], "\n")
    println("avg\t", round((precision[1] + precision[2])/2, digits=2), "\t", round((recall[1] + recall[2])/2, digits=2))
    println("w. avg\t", round(precision[1] * classSize[1] / size(dataSet, 1) + precision[2] * classSize[2] / size(dataSet, 1), digits = 2), "\t", round(recall[1] * classSize[1] / size(dataSet, 1) + recall[2] * classSize[2] / size(dataSet, 1), digits = 2), "\n")
    
end 
