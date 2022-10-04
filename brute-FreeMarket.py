#!/usr/bin/env python3

import time
import sys

# Global Variables --> Used for final line of output
sat_total = 0
unsat_total = 0
wff_total = 0
answers_provided = 0
answers_correct = 0

w = open("brute-" + sys.argv[1].split('.')[0] + "-output.csv","w") #Opens output file
f = open(sys.argv[1], "r") #Opens input file

def readWff():

    first = True
    output = []
    wff = []

    for line in f: #Reads in each line of file
        
        if line[0] == 'c': #Signals new wff

            if(first): #First wff skips, as no other info is loaded
                first = False
            else:

                correctness = False #Each wff is considered false to start

                start_time = time.time() * 1000000 #Start before first generated string
                string_input = int(num_variables) * "0" #Gives starting string

                while len(string_input) <= int(num_variables) : #While not ending string

                    if verify(wff,string_input): #Try to verify brute force combo
                        end_time = time.time() * 1000000 #If verified end timer
                        correctness = True
                        break


                    string_input = assignments(string_input) #Generate new string

                if(not end_time): #If not verified --> set end_time
                    end_time = time.time() * 1000000

                output_func(correctness,string_input,start_time,end_time,test_answer,problem_number,num_variables,num_clauses,k,num_literals)

            num_literals = 0

            comment = line.split() #Parse Comment Line
            problem_number = comment[1]
            k = comment[2]
            test_answer = comment[3]
            end_time = 0 #Reset End Time

        elif(line[0] == 'p'):

            problem = line.split()
            num_variables = problem[2]
            num_clauses = problem[3]

            wff = []

        else:
            clause = line.split(',')[:-1]
            wff.append(clause)
            num_literals += len(clause)


    #Since Code finishes execution, and doesn't loop through again, need to repeat code as if new comment line to finish last set of input

    correctness = False #Each wff is considered false to start

    start_time = time.time() * 1000000 #Start before first generated string
    string_input = int(num_variables) * "0" #Gives starting string

    while len(string_input) <= int(num_variables) : #While not ending string

        if verify(wff,string_input): #Try to verify brute force combo
            end_time = time.time() * 1000000 #If verified end timer
            correctness = True
            break


        string_input = assignments(string_input) #Generate new string

    if(not end_time): #If not verified --> set end_time
        end_time = time.time() * 1000000

    output_func(correctness,string_input,start_time,end_time,test_answer,problem_number,num_variables,num_clauses,k,num_literals)

    file_no_ext = sys.argv[1].split('.')[0] #Gets test file name 

    w.write('\n')
    
    w.write(f'{file_no_ext},FreeMarket,{wff_total},{sat_total},{unsat_total},{answers_provided},{answers_correct}')

        
    
def assignments(prev_input):   #input is a string, to be interpreted as binary, return value is string of binary + 1

    l = len(prev_input)


    temp = int(prev_input, 2) #Convert binary string to base 2 int
    temp += 1

    #Parse binary string into acceptable format
    newbinary = str(bin(temp)).split("0b")[1] 
    comp = l - len(newbinary)
    answer = comp *"0" #Add 0s to the start of string if not present

    answer += newbinary

    return answer


def verify(wff, assignment):
    valid = 0

    for clause in wff: #Loop through each clause of wff
        valid = 0 #Clause assumed to be invalid to start
        for value in clause: #Loop through each value in each clause

            temp = int(assignment[abs(int(value))-1]) #Get integer value of assignment string to compare to value

            if (int(value) < 0): #If negative value
                if (temp == 0): #Temp must be a 0 (not)
                    temp = 1
                else: #Clause is unsatisfiable
                    temp = 0

            #If value is positive, the value of temp will determine if clause is true

            #Only need to evaluate 1 clause for truth -> ors

            if(temp): #No need to check other clauses
                valid = 1
                break

        if valid == 0:
            return False
            
    return True

def output_func(correctness,string_input,start_time,end_time,test_answer,problem_number,num_variables,num_clauses,k,num_literals):
    if correctness:
        sat_prediction = "S"
        global sat_total
        sat_total = sat_total + 1
    else:
        sat_prediction = "U"
        global unsat_total
        unsat_total = unsat_total + 1

    if test_answer == '?':
        agree_with = "0"
    elif test_answer == sat_prediction:
        global answers_provided
        answers_provided += 1
        global answers_correct
        answers_correct += 1
        agree_with = "1"
    else:
        answers_provided += 1
        agree_with = "-1"

    sat_input = string_input

    execution_time = end_time - start_time

    global wff_total
    wff_total += 1

    w.write(f'{problem_number},{num_variables},{num_clauses},{k},{num_literals},{sat_prediction},{agree_with},{execution_time}')

    if(sat_prediction == "S"):
        for char in sat_input:
            w.write(f',{char}')

    w.write('\n')

readWff()