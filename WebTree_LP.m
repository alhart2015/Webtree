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
data = textscan(fid, '%d %s %d %d %d %d %s %s %s %d %s', 'delimiter', ',');
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

people = unique(ID);
courses = unique(crn);

num_courses = length(courses);

% Get map from CRN to cap
course_celing_map = course_caps(courses.', crn, course_celing);

% Populate the constraint matrices
constraints = zeros(num_courses);
constants = zeros(num_courses, 1);
% Loop through the courses and set a constraint for each
for i = 1:length(courses)
    course_in_question = courses(i);
    constraints(i, i) = 1;
    constants(i) = course_celing_map(course_in_question);
end

