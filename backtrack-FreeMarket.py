#!/usr/bin/env python3

def checkwff(answers, wff, max):

    temp = wff.copy()

    for clause in wff:
        for item in clause:

            if abs(int(item)) <= len(answers): #Able to check
                if int(item) < 0 and answers[abs(int(item))-1][1] == 0:
                    index = temp.index(clause)
                    temp.pop(index)
                    break
                elif int(item) > 0 and answers[abs(int(item))-1][1] == 1:
                    index = temp.index(clause)
                    temp.pop(index)
                    break

    if not len(temp):
        return True
    
    return False

wff = [[-3,-2],[4,4],[-2,-4],[1,4],[-3,1],[-1,1],[-4,-4],[2,-4],[-3,2],[-3,-4]]

max = 4
answers = [[1,1]] #Push to answers all possible combinations

while len(answers):

    if len(answers) < max:
        answers.append( [answers[-1][0] + 1, 1] )

    #Check wff for validity
    sat = checkwff(answers,wff,max)
    print(sat)
    
    if(len(answers) == max and answers[-1][1]):
        x = answers.pop()
        x[1] = 0
        answers.append(x)
    elif len(answers) == max and not answers[-1][1]:
        x = answers.pop()
        while len(answers) and not x[1]:
            x = answers.pop()

        if not (x[1] == 0 and not len(answers)):
            x[1] = 0
            answers.append(x)

    

