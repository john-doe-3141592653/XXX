import sys
import os
import statistics as stat

oracle = []
time = []
cov = []
lim = []

for i in range(10):
	print("folder -> " + str(i))
	time_array = []
	with open("./" + sys.argv[1] + "/experiment/" + str(i) + "/time", "r") as f:
		for line in f:
			time_array.append(float(line[:-1]))
	time.append(sum(time_array))
	with open("./" + sys.argv[1] + "/experiment/" + str(i) + "/time_stat", "w") as f:
		f.write(str(min(time_array)) + "\n")
		f.write(str(max(time_array)) + "\n")
		f.write(str(stat.median(time_array)) + "\n")
		f.write(str(sum(time_array)) + "\n")
	
	for j in range(100):
		os.system("python3 ./" + sys.argv[1] + "/oracle_" + sys.argv[1] + ".py " + sys.argv[1] + "/experiment/" + str(i) + "/test_case_" + str(j) + "/test_artifact_0/ " + sys.argv[1] + "/experiment/" + str(i) + "/")
		os.system("python3 ./" + sys.argv[1] + "/analysis_" + sys.argv[1] + ".py " + sys.argv[1] + "/experiment/" + str(i) + "/test_case_" + str(j) + "/test_artifact_0/ " + sys.argv[1] + "/experiment/" + str(i) + "/")

	with open("./" + sys.argv[1] + "/experiment/" + str(i) + "/oracle", "r") as f:
		tmp = "False"
		for line in f:
			if line[:-1] == "True":
				tmp = "True"
		oracle.append(tmp)


	coverage = []
	coverage_percentage = []

	with open(sys.argv[1] + "/experiment/" + str(i) + "/analysis.csv", "r") as f:
		line_nb = 0
		nb_X = 0
		for line in f:
			for j, v in enumerate(line[:-1].split(";")):
				if line_nb == 0:
					if v == "True":
						coverage.append(True)
						nb_X += 1
					else:
						coverage.append(False)
				else:
					if v == "True" and coverage[j] == False:
						coverage[j] = True
						nb_X += 1
			coverage_percentage.append(nb_X/len(line.split(";")))
			line_nb += 1

	limit = 100
	tmp = coverage_percentage[-1]
	cov.append(tmp)
	for j in range(2, len(coverage_percentage) + 1):
		if tmp == coverage_percentage[-j]:
			limit = 100 - j
	lim.append(limit)

	with open(sys.argv[1] + "/experiment/" + str(i) + "/coverage.csv", "w") as f:
		for j in range(100):
			f.write(str(coverage_percentage[j]) + "\n")
	with open(sys.argv[1] + "/experiment/" + str(i) + "/coverage_limit", "w") as f:
		f.write(str(limit) + "\n")

with open("./" + sys.argv[1] + "/experiment/time_stat.csv", "w") as f:
	f.write("min;" + str(min(time)) + "\n")
	f.write("max;" + str(max(time)) + "\n")
	f.write("med;" + str(stat.median(time)) + "\n")
	f.write("sum;" + str(sum(time)) + "\n")


with open("./" + sys.argv[1] + "/experiment/coverage.csv", "w") as f:
	f.write("min;" + str(min(cov)) + "\n")
	f.write("max;" + str(max(cov)) + "\n")
	f.write("med;" + str(stat.median(cov)) + "\n")

with open("./" + sys.argv[1] + "/experiment/coverage_limit.csv", "w") as f:
	f.write("min;" + str(min(lim)) + "\n")
	f.write("max;" + str(max(lim)) + "\n")
	f.write("med;" + str(stat.median(lim)) + "\n")


with open("./" + sys.argv[1] + "/experiment/oracle.csv", "w") as f:
	for i in oracle:
		f.write(str(i) + "\n")




