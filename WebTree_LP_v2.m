% Does webtree as a binary integer programming problem. This is our second shot
% at it.
%
% Author: Alden Hart and Rich Korzelius
% 3/22/2015

FILENAME = 'processed_data.csv'
OUTFILE = 'MATLAB_result.txt'

all_data = csvread(FILENAME);
student_ids = all_data(3:end,1);
crns = all_data(1,2:end);
caps = all_data(2,2:end);
prefs = all_data(3:end,2:end);

num_students = length(student_ids);
num_classes = length(crns);
num_variables = num_students * num_classes;

Aeq  = zeros(num_students, num_variables); % The sum of every row needs to equal 4

for i = 1:num_students
    st = num_classes*(i-1) + 1;
    ed = st + num_classes-1;
    Aeq(i, st:ed) = 1;
end

beq = zeros(num_students, 1);
beq(:) = 4;

A = zeros(num_classes, num_variables);  % Every class has to be within its cap

for i = 1:num_classes
    A(i, i:num_classes:end) = 1;
end

b = caps.';

lb = zeros(num_variables, 1);
ub = ones(num_variables, 1);

intcon = 1:num_variables;

f = reshape(prefs.', [1,num_variables]);

tic
[x, fval, exitflag, output] = intlinprog(f, intcon, A, b, Aeq, beq, lb, ub);
toc
fval
exitflag
output

fileid = fopen(OUTFILE, 'w');
fprintf(fileid, '%d\n', x);