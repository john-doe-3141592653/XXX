import statistics as stat
import os

for i in range(10):
	#for j in range(100):
		#os.system("mv ./" + str(i) + "/test_case_" + str(j) + "/data.txt ./" + str(i) + "/test_case_" + str(j) + "/tax.txt")
		#os.system("mv ./" + str(i) + "/test_case_" + str(j) + "/oz.uml ./" + str(i) + "/test_case_" + str(j) + "/tax.uml")

	first_line = True
	time_array = []
	with open("./" + str(i) + "/expeTax.csv", "r") as f:
		for line in f:
			if first_line:
				first_line = False
			else:
				tmp, nb_t, t = line[:-1].split(";")
				time_array.append(t)
	with open("./" + str(i) + "/time", "w") as f:
		for t in time_array:
			f.write(t + "\n")


