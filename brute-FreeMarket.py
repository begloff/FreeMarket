#!/usr/bin/env python3

import time
import sys

def readWff():

    first = True
    output = []
    wff = []

    f = open(sys.argv[1], "r")
    w = open("brute-" + sys.argv[1].split('.')[0] + "-output.csv","w")

    sat_total = 0
    unsat_total = 0
    wff_total = 0
    answers_provided = 0
    answers_correct = 0

    for line in f:
        
        if line[0] == 'c': #Signals new wff

            if(first):
                first = False
            else:

                #Determines the satisfiability of the wff given all inputs
                correctness = False

                start_time = time.time() * 1000000
                string_input = int(num_variables) * "0" #Gives starting string

                while string_input != ("1" * int(num_variables) ):

                    if verify(wff,string_input):
                        end_time = time.time() * 1000000
                        correctness = True
                        break


                    string_input = assignments(string_input)

                if string_input == "1" * int(num_variables):
                    if verify(wff,string_input):
                        end_time = time.time() * 1000000
                        correctness = True
                    else:
                        end_time = time.time() * 1000000

                if correctness:
                    sat_prediction = "S"
                    sat_total = sat_total + 1
                else:
                    sat_prediction = "U"
                    unsat_total = unsat_total + 1

                if test_answer == '?':
                    agree_with = "0"
                elif test_answer == sat_prediction:
                    answers_provided += 1
                    answers_correct += 1
                    agree_with = "1"
                else:
                    answers_provided += 1
                    agree_with = "-1"

                sat_input = string_input

                execution_time = end_time - start_time

                wff_total += 1

                w.write(f'{problem_number},{num_variables},{num_clauses},{k},{num_literals},{sat_prediction},{agree_with},{execution_time}')

                if(sat_prediction == "S"):
                    for char in sat_input:
                        w.write(f',{char}')

                w.write('\n')

            num_literals = 0


            # If not the first one, need to push to output
            comment = line.split()
            problem_number = comment[1]
            k = comment[2]
            test_answer = comment[3]

        elif(line[0] == 'p'):

            problem = line.split()
            num_variables = problem[2]
            num_clauses = problem[3]

            wff = []

        else:
            clause = line.split(',')[:-1]
            wff.append(clause)
            num_literals += len(clause)


    #Since Code finishes execution, and doesn't loop through again, need to repeat code as if new comment line 

    #Determines the satisfiability of the wff given all inputs
    correctness = False

    start_time = time.time() * 1000000
    string_input = int(num_variables) * "0" #Gives starting string

    while string_input != ("1" * int(num_variables) ):

        if verify(wff,string_input):
            end_time = time.time() * 1000000
            correctness = True
            break


        string_input = assignments(string_input)

    if string_input == "1" * int(num_variables):
        if verify(wff,string_input):
            end_time = time.time() * 1000000
            correctness = True
        else:
            end_time = time.time() * 1000000

    if correctness:
        sat_prediction = "S"
        sat_total = sat_total + 1
    else:
        sat_prediction = "U"
        unsat_total = unsat_total + 1

    if test_answer == '?':
        agree_with = "0"
    elif test_answer == sat_prediction:
        agree_with = "1"
        answers_provided += 1
        answers_correct += 1
    else:
        agree_with = "-1"
        answers_provided += 1

    sat_input = string_input

    execution_time = end_time - start_time
    wff_total += 1

    file_no_ext = sys.argv[1].split('.')[0]


    w.write(f'{problem_number},{num_variables},{num_clauses},{k},{num_literals},{sat_prediction},{agree_with},{execution_time}')

    if(sat_prediction == "S"):
        for char in sat_input:
            w.write(f',{char}')

    w.write('\n')
    
    w.write(f'{file_no_ext},FreeMarket,{wff_total},{sat_total},{unsat_total},{answers_provided},{answers_correct}')

        
    
def assignments(prev_input):   #input is a string, to be interpreted as binary, return value is string of binary + 1

    l = len(prev_input)


    temp = int(prev_input, 2)
    temp += 1

    newbinary = str(bin(temp)).split("0b")[1]
    comp = l - len(newbinary)
    answer = comp *"0"

    answer += newbinary

    return answer


def verify(wff, assignment):
    valid = 0

    for clause in wff:
        valid = 0
        for value in clause:
            temp = int(assignment[abs(int(value))-1])
            if (int(value) < 0):
                if (temp == 0):
                    temp = 1
                else:
                    temp = 0
            valid = valid or temp

        if valid == 0:
            return False
            
    return True
readWff()