# Webtree
Assign courses to students based on requests, framed as a linear programming problem

To run, first run webtree_preprocessing_v2.py with the proper in and out filenames. 
Then run WebTree_LP_v2.m in MATLAB on the file produced by webtree_preprocessing_v2.py.
To get the matching of students to courses, run create_matching.py on the proper filenames.
To evaluate the results, run evaluation.py on the proper filenames.

Obviously, a final production version would streamline this all into one program. For
expediency's sake, we haven't done that, though it would be trivial to do so.
