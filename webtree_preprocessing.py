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

# FILENAME = './WebTree Data/fall-2013.csv'
FILENAME = './WebTree Data/test.csv'
FIELDS = ['ID','CLASS','CRN','TREE','BRANCH','COURSE_CEILING',
          'MAJOR','MAJOR2','SUBJ','NUMB','SEQ']
FIELDS_WE_CARE_ABOUT = ['ID','CLASS','CRN','TREE','BRANCH','COURSE_CEILING']
ID = 0
CLASS = 1
CRN = 2
TREE = 3
BRANCH = 4
COURSE_CEILING = 5

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

def random_by_class(ids, class_years, crns, trees, branches, ceilings):
    '''Puts students in random order by class. Seniors are organized first,
        then juniors, sophomores, freshmen. NOTE the incoming data is organized
        so that for any i, ids[i], class_years[i], crns[i], trees[i],
        branches[i], ceilings[i] all correspond to row i in the original data.

    Parameters:
        ids - the list of student IDs
        class_years - the list of class years, as numbers
        crns - the list of crns
        trees - the list of tree preferences
        branches - the list of branch preferences
        ceilings - the courst ceilings

    Returns: each of these lists sorted as described above
    '''
    data = np.array([ids, class_years, crns, trees, branches, ceilings])
    print data


def main():
    all_data = read_file(FILENAME)
    ids = all_data[ID]
    raw_class_years = all_data[CLASS]
    class_years = replace_with_numbers(raw_class_years)
    crns = all_data[CRN]
    trees = all_data[TREE]
    branches = all_data[BRANCH]
    ceilings = all_data[COURSE_CEILING]
    # print ids[5]
    # print class_years[5]
    # print crns[5]
    # print trees[5]
    # print branches[5]
    # print ceilings[5]

if __name__ == '__main__':
    main()
