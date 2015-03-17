% Function to match the course numbers with their caps
%
% Author: Alden Hart
% 3/15/2015

function [course_map] = course_caps(unique_courses, all_courses, caps_list)
    % Matches course numbers with the respective enrollment caps
    %
    % Parameters:
    %   unique_courses - a column vector of the unique CRNs
    %   all_courses - a column vector of all the classes picked
    %   caps_list - a column vector of the enrollment caps
    %
    % Returns: a MATLAB Map object with keys of CRNs and values of the cap for
    %          that class
    caps = zeros(length(unique_courses), 1);
    used_courses = zeros(length(unique_courses), 1);
    last_course_added = 1;
    last_used_added = 1;

    % Loop through the list of courses (not unique) and match it with the cap
    for i = 1:length(all_courses)
        this_class = all_courses(i);
        if ~ismember(this_class, used_courses)
            caps(last_course_added) = caps_list(i);
            used_courses(last_used_added) = this_class;
            last_used_added = last_used_added + 1;
            last_course_added = last_course_added + 1;
        end
    end

    course_map = containers.Map(used_courses, caps);
