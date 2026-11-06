import numpy as np

marks = np.array([
	[70, 80, 90],
	[60, 75, 85],
	[88, 92, 79],
	[55, 65, 70],
])

print("Shape:", marks.shape)
print("Dtype:", marks.dtype)
print("Size:", marks.size)

# Select the last subject mark for the first two students.
print("First two students, last subject:", marks[:2, -1])

student_averages = marks.mean(axis=1)
subject_averages = marks.mean(axis=0)
print("Student averages:", np.round(student_averages, 2))
print("Subject averages:", subject_averages)

# Broadcasting adds five grace marks to every score.
grace_marks = marks + 5
print("Marks with grace marks:\n", grace_marks)

weights = np.array([0.3, 0.3, 0.4])
weighted_scores = np.dot(marks, weights)
print("Weighted scores:", weighted_scores)

reshaped = np.arange(12).reshape(3, 4)
print("Reshaped arange:\n", reshaped)
