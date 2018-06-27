# Morgan Sorbaro
# 10/14/17
# Rush extra credit class

# imports
from random import choice
from random import uniform
import time

#this takes a list of sororities and people and a min people who should be in that sorority and the max amount and places everyone
class Rush:

    #constructor. takes all the data given
    def __init__(self, fileName, min, cap, sororities, people ):
        self.filename= fileName; #file to read in from
        self.variables_to_assignment = {} #all the assignments mapped to boolean
        self.negative_clauses = [] #two clauses that are negative and not possible
        self.one_true_clauses = [] #one that can be true

        self.createData() #fills the data structures above
        self.sororities = sororities #list of sororities grabbed in
        self.cap= cap #largest amount of people who can be in sorority (inclusive)
        self.min = min #minimum amount of people who can be in sorority (incluvisve)


    #method the takes in the data from the files
    def createData(self):

        #create file
        file_object = open(self.filename, "r")

        #loop through each line
        for line in file_object:
            listofwords = line.split(" ") #split by spaces

            #remove all white space possiblities
            if '\n' in listofwords:
                listofwords.remove('\n')
            if ' ' in listofwords:
                listofwords.remove(' ')
            if '' in listofwords:
                listofwords.remove('')

            #remove all new line characters at the end of the line
            for i in range(0, len(listofwords)):
                listofwords[i] = listofwords[i].rstrip('\n')


            #if the lendth of hte list of words is two, we want it in the pairs list
            if len(listofwords) == 2:

                #remove the negative signs and replace with nothing
                if "-" in listofwords[0]:
                    listofwords[0]= listofwords[0].replace("-", "")
                if "-" in listofwords[1]:
                    listofwords[1]= listofwords[1].replace("-", "")

                #create two tuples as values between girls and sorority
                list1 = listofwords[0].split(",")
                val1= (list1[0], list1[1])
                list2 = listofwords[1].split(",")
                val2  = (list2[0],list2[1])

                #add the two tuples to the negative list
                self.negative_clauses.append([val1, val2])
                #randomly assign a variable.
                self.variables_to_assignment[val1] = choice([True, False])
                self.variables_to_assignment[val2] = choice([True, False])

            #if the length is greater than 2
            elif len(listofwords) > 2:
                #create a list for the tuples to go in
                tuplelist = []
                #loop through each word in the list of words
                for word in listofwords:
                    #split by comma because comma seperates girl and sorority
                    l = word.split(",")
                    #create the tuple
                    val = (l[0], l[1])
                    #randomly give tuple a value
                    self.variables_to_assignment[val] = choice([True, False])
                    #add tuple to list of tuples
                    tuplelist.append(val)

                #add the list of tuples
                self.one_true_clauses.append(tuplelist)


    # solves the binary contraint problem of rush
    def walksat(self):

        # while the current assignemnt is not good
        while (self.checkAssignment() == False):

            # choose a random clause from the list of clauses where one needs to be true
            clause = choice(self.one_true_clauses)

            # Keep choosing a new clause until it is a "good" clause (it makes sense to flip becuase isnt already accurate)
            while (self.isgood(clause) == True):
                # new clause choice
                clause = choice(self.one_true_clauses)

            # choose a random value betwewen 0 and 1
            randomval = uniform(0, 1)

            # if the random val is greater than this probability (high to it almost never happens)
            if randomval > .97:
                # choose a random variable from the random clause
                randomvar = choice(clause)
                # flip the random variable
                self.variables_to_assignment[randomvar] = not self.variables_to_assignment[randomvar]

            # the more likely conidition is that we calculate the scores for the one to flip
            else:

                scores = {}  # set which will map var -> score
                # loop through varialbes in the clause and get the score for each
                for var in clause:
                    scores[var] = self.calculateScore(var)  # put score in set

                largest = -1  # start at -1 because will always be greater
                results = []  # empry list of the variables with the largest value to be in

                # loop through all the variables
                for var in scores:
                    # if that variables score is greater than the largest score
                    if scores[var] > largest:
                        largest = scores[var]  # replace largest with the new score
                        results = []  # create a new results array
                        results.append(var)  # add the new variable to the array
                    # if the variables largest is equal to the current scores largest
                    elif scores[var] == largest:
                        results.append(var)  # add that to the list as well

                # choose a random variable from the list of results with the largest scores to flip
                randomvar = choice(results)

                # flip the value associated with that variable
                self.variables_to_assignment[randomvar] = not self.variables_to_assignment[randomvar]

        # when it gets here all things food so return this
        return self.variables_to_assignment

        # this method takes a variable and calculates teh score for it

    def calculateScore(self, var):

        opposite = not self.variables_to_assignment[var]  # opposite value from the current variables assignment
        count = 0  # start score is 0

        # loop through all the pairs in the negative clauses ex: [-111, -121]
        for pair in self.negative_clauses:
            # if the vaeriable is in the pair, we wnat to figure out what the other variable is in the pair
            if var in pair:
                # check var is first in pair
                if pair[0] == var:
                    other = pair[1]  # the second val in the pair is other
                # other must be the first pair if not the second
                else:
                    other = pair[0]

                # the value associated with the other variable
                otherval = self.variables_to_assignment[other]

                # if at least one o the values is false, this is a good statement
                if otherval == False or opposite == False:
                    count = count + 1  # increase count

        # each list in all the one true classes list
        for list in self.one_true_clauses:

            trues = 0  # count for all the true varialbes

            # for each var in the list
            for curr in list:
                if curr != var:  # if it is not the current variable
                    # if it is equal to true
                    if self.variables_to_assignment[curr] == True:
                        # increment the true count
                        trues = trues + 1
            # if there are only one true value and the opposite will also be false and hold this
            if trues == 1 and opposite == False:
                count = count + 1  # increment count
            # if there are no true values and opposite is true and will hold this
            elif trues == 0 and opposite == True:
                count = count + 1  # increment count

        # return count, the total score for the variable
        return count


    # This method checks the assignment of variables nad checks to see if it fits all restraints
    def checkAssignment(self):
        # loop through the pairs of negative caluses
        for pair in self.negative_clauses:
            ##if both of them are true then return false- this is not ok
            if self.variables_to_assignment[pair[0]] == True and self.variables_to_assignment[pair[1]] == True:
                return False

        # loop though all the lists in the true clauses
        for list in self.one_true_clauses:
            truecount = 0  # count the amount of times they have the value of true
            # for each variable in the list
            for var in list:
                # see if the value is true
                if self.variables_to_assignment[var] == True:
                    truecount = truecount + 1  # increment the True's count

            # if true count is not 1 (need on value to be true onyl for suduko)
            if truecount != 1:
                return False  # returnfalse

        #we also have to check the amount of people matches the nececity of people
        sororities = {}
        #add all soririties to this dictionary with count values starting at 0
        for s in self.sororities:
            sororities[s] = 0

        #go through each variable
        for var in self.variables_to_assignment:
            #go through each sorority
            for sorority in sororities:
                #if that person is in the sorority
                if sorority in var and self.variables_to_assignment[var] == True:
                    #add the count to sorority
                    sororities[sorority] = sororities[sorority] + 1

        #loop through each sorority
        for sorority in sororities:
            #if the amount is greater than max or less than min return false because not good
            if sororities[sorority] < self.min or sororities[sorority] > self.cap:
                return False

        #everything else solid return true
        return True

    #this method writes the solution out into a dictionary
    def write_solution(self):
        #dictionary to be filled. Maps soririty to set of memebrs
        sororitytopeople = {"":{}}
        #loop through assignment
        for assignment in self.variables_to_assignment:
            #if this is a true varable
            if self.variables_to_assignment[assignment] == True:
                #we see if the sorority is already there
                if assignment[1] in sororitytopeople:
                    #if so add
                    sororitytopeople[assignment[1]].add(assignment[0])
                #otherwise we add the entry as a whole
                else:
                    sororitytopeople[assignment[1]]={assignment[0]}

        del sororitytopeople[""] #delete the test one i had to make

        #for each sorority
        for sorority in sororitytopeople:
            #nake string w each sorority and its members
            str = "sorority " + sorority + ": "
            for person in sororitytopeople[sorority]:
                str = str+ person +", "
            #print the string
            print(str)
        #print hte whole map
        print(sororitytopeople)



    # this method checks the random clause that is choosen in walksat and returns True if it is a complete clause and false otherwise
    def isgood(self, clause):

        # check if the length of the caluse is 2 because then a pair
        if len(clause) == 2:
            # if they are both true, return false because this is not a satisfied pair
            if self.variables_to_assignment[clause[0]] == True and self.variables_to_assignment[clause[1]] == True:
                return False

        # if the lendth is greater than 2
        if len(clause) > 2:
            truecount = 0  # count trues

            # loop through all variables in the clause
            for var in clause:
                # if they are true update true count
                if self.variables_to_assignment[var] == True:
                    truecount = truecount + 1

            # if the true count is not equal to 1, also return false
            if truecount != 1:
                return False

        #put all sororitties into this empty set with a score of 0 people start w 0 people
        sororities = {}
        for s in self.sororities:
            sororities[s] = 0

        #count true values
        tcount = 0
        #loop through all variables, if value is true, update true count
        for var in self.variables_to_assignment:
            if self.variables_to_assignment[var] == True:
                tcount = tcount +1

        #if the total amount of true values is not the amount of sororities, return false
        if tcount!=len(self.sororities):
            return False

        #if it is the right length
        if tcount == len(self.sororities):
            #loop through variables
            for var in self.variables_to_assignment:
                #for each sorority
                for sorority in sororities:
                    #if the sorority exists and the variables True
                    if sorority in var and self.variables_to_assignment[var] == True:
                        #update the person count
                        sororities[sorority] = sororities[sorority] + 1

            #for each sorority
            for sorority in sororities:
                #check the cap
                if sororities[sorority] < self.min or sororities[sorority] > self.cap:
                    return False

        #everything must be good, return true
        return True


#Function outside the class. Write everything to the file for me
def writeBinaryConstraints(filename, sororities, people):

    #create the file
    file_object = open(filename, "w")

    #loop through all the poeple in the people list
    for i in range (0, len(people)):

        #string
        sororitystring = ""

        #for each of the sororities
        for s in sororities:
            #make a string with each sorority with each person
            sororitystring = sororitystring + people[i]+","+s + " "
        file_object.write(sororitystring+"\n")

        #then loop through and do the negative constrings
        for s1 in range(0, len(sororities)):
            for s2 in range(s1, len(sororities)):
                #if they are not equal
                if sororities[s1] != sororities[s2]:
                    #put the negative constrint in
                    file_object.write("-"+people[i]+","+sororities[s1]+" "+"-"+people[i]+","+sororities[s2] + "\n")
    #close file
    file_object.close()

##small test case to start
sororities = ["kkg", "xd","kde"]
people = ["ak", "ms", "vm", "lr"]

##larger case some sororities
sororities2 = ["kkg", "xd","kde", "aphi", "sd"]

#these are initials
people2 = ["zz", "ak", "ms", "vm", "lr", "ap", "sg", "fc", "ej", "aw", "mn", "sh", "ab", "zq", "lm", "am", "kk"]

#create the constraints for the file
writeBinaryConstraints("excredit.cnf", sororities2, people2)

#create the problem. min and max  all the people from those sets
f17 = Rush("excredit.cnf", 2, 7, sororities2, people2)

#slve this
f17.walksat()

#print solution nice
f17.write_solution()
