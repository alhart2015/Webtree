% Function to get a linear ordering of each student's course preferences

% Author: Rich Korzelius and Alden Hart
% 3/17/2015

function [student_pref_matrix] = get_student_pref(num_unique_students, possibles, student_ids, crns, trees, branches)
    % Gets a matrix of student course preferences
    %
    % Parameters:
    %   num_unique_students - int - the number of students (no repeats)
    %   possibles - int - the total number of courses you get to pick in WebTree
    %   student_ids - list of int - the order of student_ids in the csv
    %   crns - list of int - the order of crns in the csv
    %   trees - list of int - the order of trees in the csv
    %   branches - list of int - the order of branches in the csv

    used_students = zeros(num_unique_students, 1);
    student_pref_matrix = zeros(num_unique_students, possibles);

    for i = 1:length(student_ids)   % Do this for every row in the table
        student_in_question = student_ids(i);   % Student you're looking at
        class_in_question = crns(i);            % Corresponding class
        preference = 7*(trees(i) - 1) + branches(i);    % How bad they want it
        student_pref_matrix(student_in_question, preference) = class_in_question;
    end