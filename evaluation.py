'''
Takes the matching from students to assigned courses and figures out whether
the student is satisfied with the choices.

Author: Alden Hart
3/24/2015
'''

import csv
import numpy as np

ASSIGNMENT_FILENAME = 'class_matching_fall-2013.txt'
ORIGINAL_FILENAME = './WebTree Data/fall-2013.csv'

FIELDS = ['ID','CLASS','CRN','TREE','BRANCH','COURSE_CEILING',
          'MAJOR','MAJOR2','SUBJ','NUMB','SEQ']
FIELDS_WE_CARE_ABOUT = ['ID','CLASS','CRN','TREE','BRANCH','COURSE_CEILING']
ID = 0
CLASS = 1
CRN = 2
TREE = 3
BRANCH = 4
COURSE_CEILING = 5

def read_in_assignments(ASSIGNMENT_FILENAME):
    '''Reads in the assigned courses'''
    assignments = {}
    with open(ASSIGNMENT_FILENAME, 'r') as f:
        for row in f:
            split_row = row.split(' ')
            student = split_row[0]
            # assignments[student] = [int(x) for x in split_row[1:-1]]
            assignments[student] = split_row[1:-1]

    return assignments


def read_file(filename):
    """Returns data read in from supplied WebTree data file.

    Parameter:
        filename - the name of the file to be read

    Returns: a list for each column of the information
    """
    ids = []
    classes = []
    crns = []
    trees = []
    branches = []
    ceilings = []

    with open(filename, 'r') as csvfile:
        reader = csv.DictReader(csvfile, fieldnames=FIELDS)
        reader.next()   # get rid of the header line

        for row in reader:
            id = int(row['ID'])
            ids.append(id)

            class_year = row['CLASS']
            classes.append(class_year)

            crn = int(row['CRN'])
            crns.append(crn)

            tree = int(row['TREE'])
            trees.append(tree)

            branch = int(row['BRANCH'])
            branches.append(branch)

            ceiling = int(row['COURSE_CEILING'])
            ceilings.append(ceiling)

    raw_array = np.array([ids, classes, crns, trees, branches, ceilings])
    return np.transpose(raw_array)

def assigned_ranks(assignments, requests):
    '''Looks at the classes each person was assigned and compares them to 
        their rank in their trees.

    Parameter:
        assignments - a dictionary with student IDs as keys and their four
            assigned classes as values
        requests - the matrix of all request data

    Returns: a dictionary with student IDs as keys and a list of tuples of
        (CRN, tree, branch) of each course assigned.
    '''
    ranks = {}
    for row in requests:
        student = row[ID]
        course = row[CRN]
        if course in assignments[student]:  # They were assigned this course
            tree = row[TREE]
            branch = row[BRANCH]
            if student in ranks:
                ranks[student].append( (course, tree, branch) )
            else:
                ranks[student] = [ (course, tree, branch) ]
    return ranks

def remove_uniques(ranks):
    '''The assigned_ranks() function returns a list of where the user ranked
        each of their assigned courses in the trees. However, it is likely that
        users put courses more than once in their tree. This removes all
        duplicates, leaving you with one 3-tuple for each course corresponding
        to the lowest rank (highest priority) time they put that course in the
        tree.

    Parameter:
        ranks - a dictionary as returned by assigned_ranks()

    Returns: a dictionary with duplicates removed.
    '''
    unique_ranks = {}
    for student, lst in ranks.iteritems():
        unique_ranks[student] = unique_classes(lst)

    return unique_ranks

def unique_classes(lst):
    '''Helper function to take a list of (class, tree, branch) tuples and 
        return a list of tuples with no repeats of classes and only the 
        lowest tree, branch choices for each class.

    Parameter:
        lst - a list of tuples

    Returns: a list with the most preferred classes chosen
    '''
    classes = {}
    for tple in lst:
        crn = tple[0]
        if crn in classes:
            class_in_dict = classes[crn]
            new_class = (tple[1], tple[2])
            if higher_preference(new_class, class_in_dict):
                classes[crn] = new_class
        else:
            classes[crn] = (tple[1], tple[2])

    uniques = []
    for k, v in classes.iteritems():
        uniques.append( (k, v[0], v[1]) )

    return uniques

def higher_preference(class_a, class_b):
    '''Determines which of class_a and class_b the user wanted more.

    Parameter:
        class_a - a 3-tuple of (crn, tree, branch)
        class_b - a 3-tuple of (crn, tree, branch)

    Returns: true if the user preferred class_a, false otherwise
    '''
    tree_a = class_a[0]
    branch_a = class_a[1]
    tree_b = class_b[0]
    branch_b = class_b[1]

    if tree_a <= tree_b:
        if tree_a < tree_b:
            return True
        elif branch_a < branch_b:
            return True

    return False



def main():
    assignments = read_in_assignments(ASSIGNMENT_FILENAME)
    requests = read_file(ORIGINAL_FILENAME)
    ranks = assigned_ranks(assignments, requests)
    unique_ranks = remove_uniques(ranks)
    for i in range(10):
        print requests[i]

    j = 0
    for k, v in assignments.iteritems():
        if j < 10:
            print k, v
        j += 1

    j = 0
    for k, v in ranks.iteritems():
        if j < 10:
            print k, v
        j += 1

    j = 0
    for k, v in unique_ranks.iteritems():
        if j < 10:
            print k, v
        j += 1

    print '344' in assignments
    print '15262' in assignments['344']
    print assignments['344']
    print 15262 in assignments['344']

if __name__ == '__main__':
    main()

# 344 [15262, 15261, 15561, 15513]