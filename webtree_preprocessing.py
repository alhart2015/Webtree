'''
Does the preprocessing of the data to run our WebTree matching as a binary
integer programming problem in MATLAB. Reads in the file, sorts it accordingly,
and outputs a text file in an easy-to-parse format.

Author: Alden Hart
3/18/2015
'''
import csv
import numpy as np
import random

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
        ceilings - the courst ceilings

    Returns: a numpy array sorted as described above
    '''
    raw_data = np.array([ids, class_years, crns, trees, branches, ceilings])
    data = np.transpose(raw_data)
    sorted_data = data[np.argsort(data[:, 1])]
    desc_sorted_data = sorted_data[::-1]
    
    return desc_sorted_data

def random_ordering(data):
    '''Takes sorted data and puts it in a random ordering by class. Seniors
        all come before juniors, juniors before sophomores, etc.

    Parameters:
        data - a 2-D numpy array sorted in descending order by class

    Returns: a numpy array scrambled as described above
    '''
    # Find where each class ends
    senior_found, junior_found, soph_found, frsh_found = False, False, False, False
    for i in xrange(len(data)):
        if not senior_found and data[i][CLASS] == 3:
            senior_found = True
            last_senior = i
        elif not junior_found and data[i][CLASS] == 2:
            junior_found = True
            last_junior = i
        elif not soph_found and data[i][CLASS] == 1:
            soph_found = True
            last_sophomore = i
        elif not frsh_found:
            if data[i][CLASS] == 0:
                frsh_found = True
                last_freshman = i
            else:
                last_freshman = 0

    print last_senior, last_junior, last_sophomore, last_freshman

    # Preallocate for speed
    scrambled = np.zeros([len(data), len(data[0])])

    for i in xrange(len(data)):
        # Randomly arrange the seniors
        for j in xrange(last_senior):
            row = random.choice(last_senior)
            scrambled[i] = row

        # Randomly arrange the juniors
        num_juniors = last_junior-last_senior
        for k in xrange(num_juniors):
            row = random.choice(num_juniors)
            scrambled[i] = row

        # Randomly arrange the sophomores
        num_sophs = last_sophomore-last_junior
        for m in xrange(num_sophs):
            row = random.choice(num_sophs)
            scrambled[i] = row

        # Randomly arrange the freshmen
        num_frosh = last_freshman-last_sophomore
        for n in xrange(num_frosh):
            row = random.choice(num_frosh)
            scrambled[i] = row

        # If anyone is "other," scramble them
        if last_freshman > 0:
            num_other = len(data) - last_freshman
            for p in xrange(num_other):
                row = random.choice(num_other)
                scrambled[i] = row
    return scrambled

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
    print sorted_data
    scrambled_data = random_ordering(sorted_data)
    print scrambled_data

    # print ids[5]
    # print class_years[5]
    # print crns[5]
    # print trees[5]
    # print branches[5]
    # print ceilings[5]

if __name__ == '__main__':
    main()
