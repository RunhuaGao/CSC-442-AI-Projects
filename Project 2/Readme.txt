AI Project 2
Runhua Gao

The problems are stored in separete files.

Problem1: Problem_1_ModusPonen.py
Problem2: Problem_2_WumpusWorld.py
Problem3: Problem_3_Hornclauses.py
Probelm4: Problem_4_LiarsandTruthTellers.py
Problem5: Problem_5_MoreLiarsandTruthTellers.py
Problem6: Problem_6_DoorofEnlightment.py

Ways to do model checking:
Pass in all literal symbols and knowledge base, enumerate all models and print models that satisfies the knowledge base


Ways to do PL_Resolution test:
Pass in a literal and its negation(ie: amy and !amy for Problem 4) and CNF knowledge base(convert it by hand), to see the PL_Resolution algorithm's result, clarify it is same as model checking
testFunction: resolutionTest(kb,literal): pass in a cnfformat knowledge base and a literal you wanna find its truth value


For problem1: 
to see the modelchecking result, run modelchecking() function; run resolutionTest(resolutionKB(), "Q") to see the PL_Resolution result
Or you could direclt run the problem file to see the modelchecking and PL_Resolution result


For problem2: 
to see the modelchecking result, run modelchecking() function; run resolutionTest(resolutionKB(), "P_1_2") to see the PL_Resolution result
Or you could direclt run the problem file to see the modelchecking and PL_Resolution result


For problem3: 
to see the modelchecking result, run modelchecking() function;
to see the PL_Resolution result, run testResolution() function
Or you could direclt run the problem file to see the modelchecking and PL_Resolution result


For problem4: 
For part a: run modelcheckingParta() to see modelchecking result; run testParta() to see PL_Resolution result
For part b: run modelcheckingPartb() to see modelchecking result; run testPartb() to see PL_Resolution result
Or you could direclt run the problem file to see the modelchecking and PL_Resolution result


For problem5:
to see the modelchecking result, run modelchecking() function;
to see PL_Resolution result, run testResolution();
Or you could direclt run the problem file to see the modelchecking and PL_Resolution result


For problem6:
Part a:
    run modelcheckingParta() to see modelchecking result;run testParta() to see PL_Resolution result
Part b:
    run modelcheckingPartb() to see modelchecking result;run testPartb() to see PL_Resolution result