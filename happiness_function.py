"""
Fitness (Happiness) Function for Webtree course assignemnts
-Sum of student preferences for assigned courses

Authors: Alden Hart and Rich Korzelius
"""



def evaluate_happiness(assignments, student_pref_matrix):
	happiness_sum = 0
	NUM_PREFS = 25

	for student in assignments:
		courses = assignments[student] #get student course assignments
		preferences = student_pref_matrix[int(student) - 1] #get list of student preferences 
		for i in range(len(courses)):
			happiness_sum += NUM_PREFS - preferences.index(courses[i]) #add the prefernece level of each assigned course to happiness sum

	return happiness_sum
