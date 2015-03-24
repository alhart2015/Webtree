'''
Does the preprocessing of the data to run our WebTree matching as a binary
integer programming problem in MATLAB. Reads in the file, sorts it accordingly,
and outputs a text file in an easy-to-parse format.

Author: Alden Hart
3/23/2015
'''

import csv
import numpy as np
import random

FILENAME = './WebTree Data/fall-2013.csv'
# FILENAME = './WebTree Data/test.csv'
OUT_FILENAME = 'processed_data.csv'

FIELDS = ['ID','CLASS','CRN','TREE','BRANCH','COURSE_CEILING',
          'MAJOR','MAJOR2','SUBJ','NUMB','SEQ']
FIELDS_WE_CARE_ABOUT = ['ID','CLASS','CRN','TREE','BRANCH','COURSE_CEILING']
ID = 0
CLASS = 1
CRN = 2
TREE = 3
BRANCH = 4
COURSE_CEILING = 5

BIG_NUMBER = 10000

def read_file(filename):
    """Returns data read in from supplied WebTree data file.

    Parameter:
        filename - the name of the file to be read

    Returns: a list for each column of the information
    """
    all_data = []
    for i in FIELDS_WE_CARE_ABOUT:
        all_data.append([])

    with open(filename, 'r') as csvfile:
        reader = csv.DictReader(csvfile, fieldnames=FIELDS)
        reader.next()   # get rid of the header line

        for row in reader:
            id = int(row['ID'])
            all_data[ID].append(id)

            class_year = row['CLASS']
            all_data[CLASS].append(class_year)

            crn = int(row['CRN'])
            all_data[CRN].append(crn)

            tree = int(row['TREE'])
            all_data[TREE].append(tree)

            branch = int(row['BRANCH'])
            all_data[BRANCH].append(branch)

            ceiling = int(row['COURSE_CEILING'])
            all_data[COURSE_CEILING].append(ceiling)

    return all_data

def replace_with_numbers(class_years):
    '''Replaces the SENI, JUNI, SOPH, FRST, OTHER tags with numbers 4, 3, 2, 1,
        0, so that we can sort by this column.

    Parameter:
        class_years - a list of the class years as returned by read_file()

    Returns: a new list with ints instead of strings
    '''
    out = []
    for year in class_years:
        if year == 'SENI':
            out.append(4)
        elif year == 'JUNI':
            out.append(3)
        elif year == 'SOPH':
            out.append(2)
        elif year == 'FRST':
            out.append(1)
        else:
            out.append(0)
    return out

def sort_by_class(ids, class_years, crns, trees, branches, ceilings):
    '''Puts students in order by class. Seniors are organized first, then 
        juniors, sophomores, freshmen. NOTE the incoming data is organized
        so that for any i, ids[i], class_years[i], crns[i], trees[i],
        branches[i], ceilings[i] all correspond to row i in the original data.

    Parameters:
        ids - the list of student IDs
        class_years - the list of class years, as numbers
        crns - the list of crns
        trees - the list of tree preferences
        branches - the list of branch preferences
        ceilings - the course ceilings

    Returns: a numpy array sorted as described above
    '''
    raw_data = np.array([ids, class_years, crns, trees, branches, ceilings])
    data = np.transpose(raw_data)
    sorted_data = data[np.argsort(data[:, 1])]
    desc_sorted_data = sorted_data[::-1]
    
    return desc_sorted_data

def course_map(data):
    '''Returns a map from CRNs to their index in the list and the course cap.

    Parameter:
        data - a two-dimensional numpy matrix of the data
    
    Returns: a dict with keys of CRNs and values of (index, cap) tuples
    '''
    found_classes = set()
    class_map = {}
    i = 0

    for row in data:
        crn = row[CRN]
        if crn not in found_classes:
            cap = row[COURSE_CEILING]
            class_map[crn] = (i, cap)
            i += 1
            found_classes.add(crn)

    return class_map

def get_unique_students(data):
    '''Gets a list of students with no repeats

    Parameter:
        data - a numpy matrix of the data

    Returns: a list with no repeats of student IDs
    '''
    return list(set(data[:,ID]))

def get_unique_classes(data):
    '''Gets a list of classes with no repeats

    Parameter:
        data - a numpy matrix of the data

    Returns: a list with no repeats of CRNs
    '''
    return list(set(data[:,CRN]))

def get_student_prefs(data, num_unique_students, num_unique_classes):
    '''Make a linear ordering of each student's class preferences

    Parameter:
        data - a numpy matrix of the data
        num_unique_students - the number of individual students
        num_unique_classes - the number of classes offered

    Returns: a numpy matrix. Each row corresponds to a student's class choices,
        each column corresponds to a class
    '''

    used_students = {}  # Dictionary from student ID to their corresponding row
    i = 0
    class_map = course_map(data)

    preference_matrix = np.empty([num_unique_students+2, num_unique_classes+1], dtype=np.int)
    preference_matrix.fill(BIG_NUMBER)  # If they don't want it, put a big number

    for row in data:
        student = row[ID]
        if student not in used_students:
            used_students[student] = i
            i += 1
        course = row[CRN]
        preference = 7*(row[TREE] - 1) + row[BRANCH]
        cap = class_map[course][1]
        # print student, course, class_map[course], preference, cap
        
        r = used_students[student] + 2
        c = class_map[course][0] + 1    # The index in the list of that course
        
        if preference_matrix[r][c] > preference:
            preference_matrix[r][c] = preference
        preference_matrix[r][0] = student
        preference_matrix[0][c] = course
        preference_matrix[1][c] = cap

    return preference_matrix

def write_file(data, filename):
    '''Writes the data to a CSV file'''
    with open(filename, 'wt') as f:
        writer = csv.writer(f)
        for row in data:
            writer.writerow(row)

def main():
    all_data = read_file(FILENAME)
    ids = all_data[ID]
    raw_class_years = all_data[CLASS]
    class_years = replace_with_numbers(raw_class_years)
    crns = all_data[CRN]
    trees = all_data[TREE]
    branches = all_data[BRANCH]
    ceilings = all_data[COURSE_CEILING]

    sorted_data = sort_by_class(ids, class_years, crns, trees, branches, ceilings)
    # print sorted_data

    unique_students = get_unique_students(sorted_data)
    num_unique_students = len(unique_students)
    unique_classes = get_unique_classes(sorted_data)
    num_unique_classes = len(unique_classes)
    print num_unique_students, num_unique_classes

    preference_matrix = get_student_prefs(sorted_data, num_unique_students, num_unique_classes)
    # print preference_matrix

    write_file(preference_matrix, OUT_FILENAME)


if __name__ == '__main__':
    main()
