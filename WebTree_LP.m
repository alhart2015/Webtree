% The WebTree Problem as an LP problem. Maximize the sum of each student's
% happiness (as decided by a function we'll define), with priority to
% seniors' preferences (because they likely have strict time requirements
% for their majors and graduation).
%
% Authors: Rich Korzelius and Alden Hart
% 3/13/2015

% Read in file data
FILENAME = 'WebTree Data/fall-2013-edited.csv'; % You need to edit the file
                                                % to remove the column
                                                % headers.
fid = fopen(FILENAME);
data = textscan(fid, '%s %s %s %s %s %s %s %s %s %s %s', 'delimiter', ',');
fclose(fid);

ID = data{1};
class_year = data{2};
crn = data{3};
tree = data{4};
branch = data{5};
course_celing = data{6};
major = data{7};
major2 = data{8};
subject = data{9};
number = data{10};
seq = data{11};

all_data = [ID class_year crn tree branch course_celing];

sr_string = cellstr('SENI');
sr_replace = cellstr('4');
jr_string = cellstr('JUNI');
jr_replace = cellstr('3');
so_string = cellstr('SOPH');
so_replace = cellstr('2');
fr_string = cellstr('FRST');
fr_replace = cellstr('1');
ot_replace = cellstr('0');

for i = 1:length(class_year)        % Replace the spellings of the class year
    current_year = class_year(i);   % with something you can sort by
    if strcmp(current_year, sr_string)
        class_year(i) = sr_replace;
    elseif strcmp(current_year, jr_string)
        class_year(i) = jr_replace;
    elseif strcmp(current_year, so_string)
        class_year(i) = so_replace;
    elseif strcmp(current_year, fr_string)
        class_year(i) = fr_replace;
    else
        class_year(i) = ot_replace;
    end
end

sorted_data = sortrows(all_data, [-2 1]);   % Sort by year then ID number

people = unique(ID);
courses = unique(crn);

num_courses = length(courses);

% Get map from CRN to cap
course_celing_map = course_caps(courses.', crn, course_celing);

% Get student preferences
% How to do this?
%     - Sum tree + branch for each choice
student_prefs = get_student_pref(length(people), 25, ID, crn, tree, branch);

% Put students in random order, accounting for seniority

% For each student:
%   Assign coefficients based on choices - objective function
%   Constraints: 
%       All courses >= 0
%       Exactly four courses per student
%           sum(all courses with no coeff == 4)
%   Check course caps
%   Maximize "happiness"
