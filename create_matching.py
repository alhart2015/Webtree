'''
Takes the result MATLAB spits out and turns it into a matching of students
and their assigned classes.

Author: Alden Hart
3/23/2015
'''

import numpy as np
import csv

MATLAB_RESULT = 'MATLAB_result_spring-2015.txt'
INPUT_DATA = 'processed_data_spring-2015.csv'
OUTFILE = 'class_matching_spring-2015.txt'

def read_in_result(MATLAB_RESULT):
    '''Reads in what MATLAB spit out. Returns it as a list.'''
    text_file = open(MATLAB_RESULT, 'r')
    lines = text_file.readlines()
    text_file.close()

    out = []
    for i in lines:
        out.append(int(i))
    return out

def read_input_data(INPUT_DATA):
    '''Reads in what you gave MATLAB so that you can figure out what class is
        what and what person is who.

    Parameter:
        INPUT_DATA - the name of the file you put into MATLAB

    Returns: a 2-D numpy array of the matrix
    '''
    out = []
    with open(INPUT_DATA, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            out.append(row)

    return out

def class_assignments(results, people, classes):
    '''Takes the string of 1's and 0's that MATLAB gives you and turns that
        into an assignment of four classes for each person.

    Parameter:
        results - the list of MATLAB results
        people - the list of student IDs, in order
        classes - the list of CRNs in order

    Returns: a dictionary with keys of people and values of the four classes
        this person got (as a list)
    '''
    assignments = {}
    num_classes = len(classes)

    for i in xrange(len(results)):
        if results[i] == 1:
            student_index = i / num_classes
            class_index = i % num_classes
            student = people[student_index]
            crn = classes[class_index]
            if student in assignments:
                assignments[student].append(crn)
            else:
                assignments[student] = [crn]

    return assignments

def write_out(assignments, filename):
    '''Writes the final assignments to a txt file.'''
    with open(filename, 'w') as f:
        for a in sorted(assignments):
            f.write(str(a) + ' ')
            for c in assignments[a]:
                f.write(str(c) + ' ')
            f.write('\n')


def main():
    result = read_in_result(MATLAB_RESULT)
    input_data = read_input_data(INPUT_DATA)
    print 'Num results', len(result)
    print 'Total classes assigned', sum(result)
    crns = input_data[0][1:]
    print 'Unique classes', len(crns)
    # print crns[:10]
    people = []
    for row in input_data[2:]:
        people.append(int(row[0]))
    # print people[:10]
    print 'Unique people', len(people)

    assignments = class_assignments(result, people, crns)
    # for p in assignments:
    #     print p, assignments[p]
    write_out(assignments, OUTFILE)

if __name__ == '__main__':
    main()