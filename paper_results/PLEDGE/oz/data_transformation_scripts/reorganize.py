import statistics as stat
import os

for i in range(10):
	for j in range(100):
		os.system("mv ./" + str(i) + "/test_case_" + str(j) + "/data.txt ./" + str(i) + "/test_case_" + str(j) + "/oz.txt")
		os.system("mv ./" + str(i) + "/test_case_" + str(j) + "/data.uml ./" + str(i) + "/test_case_" + str(j) + "/oz.uml")

	time_array = []
	with open("./" + str(i) + "/expeOz.csv", "r") as f:
		for line in f:
			tmp, nb_r, t = line[:-1].split(";")
			m = float(t.split("m")[0])
			s = float(t.split("m")[1][:-1])
			time_array.append(60*m + s)
	with open("./" + str(i) + "/time", "w") as f:
		for t in time_array:
			f.write(str(t) + "\n")


