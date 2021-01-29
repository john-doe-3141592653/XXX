import statistics as stat

sum_array = []

for i in range(10):
	nb_row_array = []
	time_array = []
	
	with open("./experiment/" + str(i) + "/expeOz.csv", "r") as f:
		for line in f:
			tmp, nb_r, t = line[:-1].split(";")
			nb_row_array.append(int(nb_r))
			m = float(t.split("m")[0])
			s = float(t.split("m")[1][:-1])
			time_array.append(60*m + s)

	with open("./experiment/" + str(i) + "/time_stat", "w") as f:
		f.write(str(min(time_array)) + "\n")
		f.write(str(max(time_array)) + "\n")
		f.write(str(stat.median(time_array)) + "\n")
		f.write(str(sum(time_array)) + "\n")
	sum_array.append(sum(time_array))

with open("./time_stat.csv", "w") as f:
	f.write("min;" + str(min(sum_array)) + "\n")
	f.write("max;" + str(max(sum_array)) + "\n")
	f.write("med;" + str(stat.median(sum_array)) + "\n")
	f.write("sum;" + str(sum(sum_array)) + "\n")


