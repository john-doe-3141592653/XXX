import statistics as stat

sum_array = []

for i in range(10):
	nb_tax_array = []
	time_array = []
	first_line = True
	
	with open("./experiment/" + str(i) + "/expeTax.csv", "r") as f:
		for line in f:
			if first_line:
				first_line = False
			else:
				tmp, nb_t, t = line[:-1].split(";")
				
				nb_tax_array.append(int(nb_t))
				if t == "timeout":
					time_array.append(600)
				else:
					time_array.append(float(t))

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


