'''
Does the preprocessing of the data to run our WebTree matching as a binary
integer programming problem in MATLAB. Reads in the file, sorts it accordingly,
and outputs a text file in an easy-to-parse format.

Author: Alden Hart
3/18/2015
'''
import csv
import numpy as np
from student import Student

FILENAME = './WebTree Data/fall-2013.csv'
FIELDS = ['ID','CLASS','CRN','TREE','BRANCH','COURSE_CEILING',
          'MAJOR','MAJOR2','SUBJ','NUMB','SEQ']

def read_file(filename):
    """Returns data read in from supplied WebTree data file.

    Parameter:
        filename - the name of the file to be read

    Returns: a numpy matrix of the information
    """

def main():
    student_requests, students_by_class, courses = read_file(FILENAME)
    print student_requests[0]
    print students_by_class[0]
    print courses[0]

if __name__ == '__main__':
    main()
