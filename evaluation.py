'''
Takes the matching from students to assigned courses and figures out whether
the student is satisfied with the choices.

Author: Alden Hart
3/24/2015
'''

import csv
import numpy as np

FA_2013_ASSIGNMENT_FILENAME = 'class_matching_fall-2013.txt'
FA_2013_BASELINE_MATCHING = 'baseline_matches_fall-2013.txt'
FA_2013_ORIGINAL_FILENAME = './WebTree Data/fall-2013.csv'

FA_2014_ASSIGNMENT_FILENAME = 'class_matching_fall-2014.txt'
FA_2014_BASELINE_MATCHING = 'baseline_matches_fall-2014.txt'
FA_2014_ORIGINAL_FILENAME = './WebTree Data/fall-2014.csv'

SP_2014_ASSIGNMENT_FILENAME = 'class_matching_spring-2014.txt'
SP_2014_BASELINE_MATCHING = 'baseline_matches_spring-2014.txt'
SP_2014_ORIGINAL_FILENAME = './WebTree Data/spring-2014.csv'

SP_2015_ASSIGNMENT_FILENAME = 'class_matching_spring-2015.txt'
SP_2015_BASELINE_MATCHING = 'baseline_matches_spring-2015.txt'
SP_2015_ORIGINAL_FILENAME = './WebTree Data/spring-2015.csv'

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

def duplicate_counts(ranks):
    '''Returns an estimation for the success of the ranking. If a user put
        a class multiple times, it is likely that the user really wanted to
        get that class. This counts the number of duplicates in a user's 
        assigned courses and sets that to be their "score" (higher scores
        are better)

    Parameter:
        ranks - a dictionary as assigned by assigned_ranks()

    Returns: a dictionary with student IDs as keys and scores as values.
    '''
    scores = {}
    for student, lst in ranks.iteritems():
        scores[student] = count_classes(lst)

    return scores

def count_classes(lst):
    '''Counts the number of duplicate classes in the given list.

    Parameter:
        lst - a list of 3-tuples (crn, tree, branch)

    Returns: the number of duplicates in the list
    '''
    count = 0
    found_classes = set()
    for tple in lst:
        current_class = tple[0]
        if current_class in found_classes:
            count += 1
        else:
            found_classes.add(current_class)

    return count

def average_count_score(duplicate_counts):
    '''Returns the average duplicate count of the set of assignments, as a 
        metric for how good the matching was.
    '''
    total_score = 0
    total_counts = 0.0
    for person, score in duplicate_counts.iteritems():
        total_counts += 1
        total_score += score

    return total_score / total_counts

def d_score(assignment_file, request_file):
    '''Returns the average number of times a person put a courses they got in 
        WebTree, as a measure of how good the matching was.
    '''
    assignments = read_in_assignments(assignment_file)
    requests = read_file(request_file)
    ranks = assigned_ranks(assignments, requests)
    duplicate_scores = duplicate_counts(ranks)

    return average_count_score(duplicate_scores)

def tree_score(unique_ranks):
    '''Returns the average (tree, branch) position of the four assigned classes.
    '''
    tot_tree = 0
    tot_branch = 0
    num_students = 0.0
    for student, classes in unique_ranks.iteritems():
        # tot_tree += classes[1]
        # tot_branch += classes[2]
        student_scores = individual_score(classes)
        tot_tree += student_scores[0]
        tot_branch += student_scores[1]
        num_students += 1

    return (tot_tree/num_students, tot_branch/num_students)

def individual_score(classes):
    '''Calculates the average tree and branch position of the four classes
        assigned to the student.

    Parameter:
        classes - a list of (crn, tree, branch) tuples of the classes assigned

    Returns: a tuple of (average tree, average branch)
    '''
    tot_tree = 0.0
    tot_branch = 0.0
    for c in classes:
        tot_tree += float(c[1])
        tot_branch += float(c[2])

    return (tot_tree/len(classes), tot_branch/len(classes))

def all_scores(assignment_file, request_file):
    '''Computes both the duplicate score and tree score for the given assignment.

    Parameter:
        assignment_file - the file with the class assignments
        request_file - the WebTree data file

    Returns: a 3-tuple (duplicate score, tree score, branch score)
    '''
    assignments = read_in_assignments(assignment_file)
    requests = read_file(request_file)
    ranks = assigned_ranks(assignments, requests)
    unique_ranks = remove_uniques(ranks)
    duplicate_scores = duplicate_counts(ranks)
    avg_d_score = average_count_score(duplicate_scores)
    avg_tree_score = tree_score(unique_ranks)
    avg_num_classes = avg_classes_assigned(assignments)

    return (avg_d_score, avg_tree_score[0], avg_tree_score[1], avg_num_classes)

def avg_classes_assigned(assignments):
    '''Maybe the most important metric is how many classes get assigned per 
        person. This returns the average number of classes per person.

    Parameter:
        assignments - the class assignments

    Returns: the average number of classes assigned to each person
    '''
    total_classes = 0.0
    for person, classes in assignments.iteritems():
        total_classes += len(classes)

    return total_classes/len(assignments)


def main():
    # assignments = read_in_assignments(ASSIGNMENT_FILENAME)
    # requests = read_file(ORIGINAL_FILENAME)
    # ranks = assigned_ranks(assignments, requests)
    # unique_ranks = remove_uniques(ranks)
    # duplicate_scores = duplicate_counts(ranks)

    # our_score = d_score(ASSIGNMENT_FILENAME, ORIGINAL_FILENAME)
    # baseline_score = d_score(BASELINE_MATCHING, ORIGINAL_FILENAME)
    # our_tree_score = t_score(ASSIGNMENT_FILENAME, ORIGINAL_FILENAME)

    fa_2013_our_score = all_scores(FA_2013_ASSIGNMENT_FILENAME, FA_2013_ORIGINAL_FILENAME)
    fa_2013_baseline_score = all_scores(FA_2013_BASELINE_MATCHING, FA_2013_ORIGINAL_FILENAME)
    print 'fall-2013'
    print 'ours', fa_2013_our_score
    print 'baseline', fa_2013_baseline_score

    fa_2014_our_score = all_scores(FA_2014_ASSIGNMENT_FILENAME, FA_2014_ORIGINAL_FILENAME)
    fa_2014_baseline_score = all_scores(FA_2014_BASELINE_MATCHING, FA_2014_ORIGINAL_FILENAME)
    print 'fall-2014'
    print 'ours', fa_2014_our_score
    print 'baseline', fa_2014_baseline_score

    sp_2014_our_score = all_scores(SP_2014_ASSIGNMENT_FILENAME, SP_2014_ORIGINAL_FILENAME)
    sp_2014_baseline_score = all_scores(SP_2014_BASELINE_MATCHING, SP_2014_ORIGINAL_FILENAME)
    print 'spring-2014'
    print 'ours', sp_2014_our_score
    print 'baseline', sp_2014_baseline_score

    sp_2015_our_score = all_scores(SP_2015_ASSIGNMENT_FILENAME, SP_2015_ORIGINAL_FILENAME)
    sp_2015_baseline_score = all_scores(SP_2015_BASELINE_MATCHING, SP_2015_ORIGINAL_FILENAME)
    print 'spring-2015'
    print 'ours', sp_2015_our_score
    print 'baseline', sp_2015_baseline_score

    # # The raw data
    # for i in range(10):
    #     print requests[i]

    # # Each person's class assignment
    # j = 0
    # for k, v in assignments.iteritems():
    #     if j < 10:
    #         print k, v
    #     j += 1

    # # The ranks people gave the classes they got
    # j = 0
    # for k, v in ranks.iteritems():
    #     if j < 10:
    #         print k, v
    #     j += 1

    # The highest rank of each class given to a person
    # j = 0
    # for k, v in unique_ranks.iteritems():
    #     if j < 10:
    #         print k, v
    #     j += 1

    # The "duplicate score" of each person
    # j = 0
    # for k, v in duplicate_scores.iteritems():
    #     if j < 10:
    #         print k, v
    #     j += 1

    # print average_count_score(duplicate_scores)

    # print '344' in assignments
    # print '15262' in assignments['344']
    # print assignments['344']
    # print 15262 in assignments['344']

if __name__ == '__main__':
    main()

# 344 [15262, 15261, 15561, 15513]