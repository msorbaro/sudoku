#Morgan Sorbaro
#10/14/17
#SAT class

#imports
from random import choice
from random import uniform
import time


#The SAT class holds information for a SAT problem. #uses the walkSAT and gSAT algorithms to solve binary constraints
class SAT:

    #The SAT class holds many thing to solve the problem
    def __init__(self, fileName):
        self.filename= fileName;  #First the file name: Used to read in information from file
        self.variables_to_assignment = {} #set that holds all variables (111) and maps if they are True or False
        self.negative_clauses = [] #this is a list of the "negative clauses" aka [[-121, -123], [-456, -467]]
        self.one_true_clauses = [] #this is a list of the other types of clauses aka ['921', '922', '923', '924', '925', '926', '927', '928', '929']]
        self.createData() #this function fills all these data structures

    #this reads in from the file and creates the data structures described above
    def createData(self):

        #create the file object
        file_object = open(self.filename, "r")

        #read in each line of the file -928 -929  or 931 932 933 934 935 936 937 938 939 type stuff
        for line in file_object:

            #create a list of each word split by spaces
            listofwords = line.split(" ")

            #get rid of all whitespaces, new lines, blank things.
            if '\n' in listofwords:
                listofwords.remove('\n')
            if ' ' in listofwords:
                listofwords.remove(' ')
            if '' in listofwords:
                listofwords.remove('')

            #Make sure no line has a new line character at the end, if so, get rid of it
            for i in range(0, len(listofwords)):
                listofwords[i] = listofwords[i].rstrip('\n')

            #if the list of words is 1, that means there is only one thing there and it must be true
            if len(listofwords) == 1:
                self.variables_to_assignment[listofwords[0]] = True

            #if the length of list of words is two, we know the constraint looks like: '-283', '-683']
            elif len(listofwords) == 2:
                #we want to remove the - from the word to be placed into the data structures
                if "-" in listofwords[0]:
                    listofwords[0]= listofwords[0].replace("-", "") ##replace words without -
                if "-" in listofwords[1]:
                    listofwords[1]= listofwords[1].replace("-", "") ##replace words without -

                ##Since this is a double, it must go in the negative clauses list.
                self.negative_clauses.append(listofwords)

                #put each randomly in the variables to assignment dictionary mapped to either true or false randomly
                self.variables_to_assignment[listofwords[0]] = choice([True, False])
                self.variables_to_assignment[listofwords[1]] = choice([True, False])

            #if the length is greater than 2, it is a statement like: ['988', '888', '788', '588', '288', '688', '488', '388', '188']
            elif len(listofwords) > 2:
                #we want to add this statemenet to the set that contains clauses like this that have one true value
                self.one_true_clauses.append(listofwords)

                #we wnat to loop through all of the list of words and assign them a random variable of true or false
                for i in range (0, len(listofwords)):
                    self.variables_to_assignment[listofwords[i]] = choice([True, False]) #assign randm value


    #The GSAT algorithm looks at all the assignmenets and returns one that works with the constraints.
    def GSAT(self):

        #the current assignment is not perfect wea re going to keep trying things.
        while(self.checkAssignment() == False):

            #choose a random value between 0 and 1
            randomval = uniform(0,1)

            #if the random value is greater than .5 (50% chance) we flip things randomly
            if randomval > .97:
                #randomly choose a varaible from the currently assigned variables
                randomvar = choice(list(self.variables_to_assignment))
                #flip it so the value is the opposite than before
                self.variables_to_assignment[randomvar] = not self.variables_to_assignment[randomvar]

            #if the value is less than .5 (50% chance), do some in depth scoring to choose which to flip
            else:
                scores = {} #set that will hold the variable and their scores

                #loop through all the variables and calculate the score
                for var in self.variables_to_assignment:
                    scores[var] = self.calculateScore(var) #place new variable -> score in a map

                largest = -1 #largest val (going to be switched)
                results = [] #list that will hold all values that have the largest score above

                #loop through all the variables
                for var in scores:
                    #see if that variables score is greater than the largest
                    if scores[var] > largest:
                        #if it is, replace largest with the new score
                        largest = scores[var]
                        #restart the results array with just var
                        results= [var]

                    #if the scores var is the same size as largest
                    elif scores[var] == largest:
                        #add the variable to the array because it also the size of hte largest
                        results.append(var)

                #randomly choose a variable from all the possible results
                randomvar = choice(results)

                #flip the random variable choosen
                self.variables_to_assignment[randomvar] = not self.variables_to_assignment[randomvar]

        #return the assignment because when it gets here it is good
        return self.variables_to_assignment

    # This is the better algorithm that loops less and therefore runs quicker
    # solves the binary contraint problem of soduko
    def walksat(self):

        #while the current assignemnt is not good
        while(self.checkAssignment()== False):

            #choose a random clause from the list of clauses where one needs to be true
            clause = choice(self.one_true_clauses)

            #Keep choosing a new clause until it is a "good" clause (it makes sense to flip becuase isnt already accurate)
            while(self.isgood(clause) == True):
                #new clause choice
                clause = choice(self.one_true_clauses)


            #choose a random value betwewen 0 and 1
            randomval = uniform(0,1)

            #if the random val is greater than this probability (high to it almost never happens)
            if randomval > .85:
                #choose a random variable from the random clause
                randomvar = choice(clause)
                #flip the random variable
                self.variables_to_assignment[randomvar] = not self.variables_to_assignment[randomvar]

            #the more likely conidition is that we calculate the scores for the one to flip
            else:

                scores={} #set which will map var -> score
                #loop through varialbes in the clause and get the score for each
                for var in clause:
                    scores[var] = self.calculateScore(var) #put score in set

                largest = -1 #start at -1 because will always be greater
                results = [] #empry list of the variables with the largest value to be in

                #loop through all the variables
                for var in scores:
                    #if that variables score is greater than the largest score
                    if scores[var] > largest:
                        largest = scores[var] #replace largest with the new score
                        results = [] #create a new results array
                        results.append(var) #add the new variable to the array
                    #if the variables largest is equal to the current scores largest
                    elif scores[var] == largest:
                        results.append(var) #add that to the list as well

                #choose a random variable from the list of results with the largest scores to flip
                randomvar = choice(results)

                #flip the value associated with that variable
                self.variables_to_assignment[randomvar] = not self.variables_to_assignment[randomvar]

        #when it gets here all things food so return this
        return self.variables_to_assignment

    #this method takes a variable and calculates teh score for it
    def calculateScore(self, var):

        opposite = not self.variables_to_assignment[var] #opposite value from the current variables assignment
        count = 0 #start score is 0

        #loop through all the pairs in the negative clauses ex: [-111, -121]
        for pair in self.negative_clauses:
            #if the vaeriable is in the pair, we wnat to figure out what the other variable is in the pair
            if var in pair:
                #check var is first in pair
                if pair[0] == var:
                    other = pair[1] #the second val in the pair is other
                #other must be the first pair if not the second
                else:
                    other = pair[0]

                #the value associated with the other variable
                otherval = self.variables_to_assignment[other]

                #if at least one o the values is false, this is a good statement
                if otherval == False or opposite == False:
                    count = count+1 #increase count

        # each list in all the one true classes list
        for list in self.one_true_clauses:

            trues = 0 # count for all the true varialbes

            #for each var in the list
            for curr in list:
                if curr != var: #if it is not the current variable
                    #if it is equal to true
                    if self.variables_to_assignment[curr] == True:
                        #increment the true count
                        trues= trues+1
            #if there are only one true value and the opposite will also be false and hold this
            if trues == 1 and opposite == False:
                count = count+1 #increment count
            #if there are no true values and opposite is true and will hold this
            elif trues ==0 and opposite ==True:
                count = count+1 #increment count

        #return count, the total score for the variable
        return count


    #This method checks the assignment of variables nad checks to see if it fits all restraints
    def checkAssignment(self):
        #loop through the pairs of negative caluses
        for pair in self.negative_clauses:
            ##if both of them are true then return false- this is not ok
            if self.variables_to_assignment[pair[0]] == True and  self.variables_to_assignment[pair[1]] == True:
                return False

        #loop though all the lists in the true clauses
        for list in self.one_true_clauses:
            truecount = 0 #count the amount of times they have the value of true
            #for each variable in the list
            for var in list:
                #see if the value is true
                if self.variables_to_assignment[var] == True:
                    truecount = truecount + 1 #increment the True's count

            #if true count is not 1 (need on value to be true onyl for suduko)
            if truecount != 1:
                return False #returnfalse

        #if it doesnt return false anywhere else then must be good :)
        return True



    #this method checks the random clause that is choosen in walksat and returns True if it is a complete clause and false otherwise
    def isgood(self, clause):

        #check if the length of the caluse is 2 because then a pair
        if len(clause) == 2:
            #if they are both true, return false because this is not a satisfied pair
            if self.variables_to_assignment[clause[0]] == True and  self.variables_to_assignment[clause[1]] == True:
                return False

        #if the lendth is greater than 2
        if len(clause) > 2:
            truecount = 0 #count trues

            #loop through all variables in the clause
            for var in clause:
                #if they are true update true count
                if self.variables_to_assignment[var] == True:
                    truecount = truecount + 1

            #if the true count is not equal to 1, also return false
            if truecount != 1:
                return False
        #everything must be gkd p> return true
        return True



    #This method writes out the solution into a file so the other program can print it nicely
    def write_solution(self, fileWrite):

        #create file
        file_object = open(fileWrite, "w")

        #loop through all the assigned varialbes
        for var in self.variables_to_assignment:
            #if the variables maps to a true numher, write it out positive
            if self.variables_to_assignment[var] == True:
                file_object.write(var+"\n")
            #otherwise, add the - sign to show that it is a false statement
            else:
                file_object.write("-"+var+"\n")

        #close file to not break computer
        file_object.close()





