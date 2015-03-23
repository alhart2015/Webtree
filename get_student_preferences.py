"""
Function to get a linear ordering of each student'a course preferences

Authors: Rich Korzelius and Alden Hart
3/18/2015
"""

def get_student_prefs(num_unique_students, possibles, student_ids, crns, trees, branches):
	used_students = [None] * num_unique_students
	student_pref_matrix = [[None]*possible] * num_unique_students

	for i ibn range(len(student_ids)):
		student_in_question = student_ids[i]
		class_in_question = crns[i]
		preference = 7*(trees[i] - 1) + branches[i]
		student_pref_matrix[student_in_question][preference - 1] = class_in_question


	return student_pref_matrix