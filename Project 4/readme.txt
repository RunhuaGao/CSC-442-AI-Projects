This is sole Project for me.

DataParser.py is to parse the dataset given. Please place all dataset txt files and code files in same folder.

DecisionTree.py
    dataset: iris, cars,restaurant
    class DecisionTree is to establish a DecisionTree
    This is more like a stastic class, most methods of it are class methods 
    you could use it as following:
    dt = DecisionTree(dataset)
    tree = dt.learning()
    tree.testData(dataset) # use current tree to test data, return and print error number
    dt.crossvalidation(k) # split dataset to k piece and then return average error number
    # Tip, the k here must meet the requirement: len(dataset)%k == 0

    or you could use docrossvalidation(dataset,num) to finish a cross validation experiment given dataset()
    
NeuralNetwork.py
    dataset: continuousIris, normalizedIris
    class OutputNode is the class of Node at output layer as my network has only two layers: input layer and outputlayer
    This whole file is designed for continuousIris and normalizedIris dataset, could be used for other datasets

    train(trainingtimes,dataset,studyrate) will establsih a neural network given dataset,studyrate and training times(argument times)
    and then do test on original dataset, print and return a error rate


Experiment.py:
    use same dataset for DecisionTree and NeuralNetwork mentioned above
    use matplotlib to get figure
    This file includs one experiment about decision and two experiments about neural network
    
    plotNeuralNetworkwithTrainingtimes(dataset, mintrainingtimes, maxtrainingtimes): plot the change of error rate with change     of training times, neural network experiment,default studyrate is 0.01
    
    plotNeuralNetworkwithStudyrate(dataset,minstudyrate,maxstudyrate,trainingtimes): plot the change of error rate with change
    of studyrate at a stable training times,neural network studyrate
    
    plotDecisionTreewithPieceNum(dataset,num): plot change of error number with change of piece num(do cross validation 
    described above, plot some scattered points, DecisionTree experiment
    
