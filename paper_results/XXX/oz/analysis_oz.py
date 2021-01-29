import sys

def return_interval(param, name):
	#print(name + ": " + str(param))
	if -0.001 <= param < 0.33:
		return "True;False;False"
	elif 0.33 <= param <= 0.67:
		return "False;True;False"
	elif 0.67 < param <= 1.001:
		return "False;False;True"
	else:
		print("ERROR: invalid " + name)
		exit()

def return_interval_array(param, name):
	#print(name + ": " + str(param))
	L = False
	M = False
	H = False
	
	for p in param:
		if -0.001 <= p < 0.33:
			L = True
		elif 0.33 <= p <= 0.67:
			M = True
		elif 0.67 < p <= 1.001:
			H = True
		else:
			print("ERROR: invalid " + name)
			exit()

	return str(L) + ";" + str(M) + ";" + str(H)

def return_bool(b, name):
	if b == "True":
		return "True;False"
	elif b == "False":
		return "False;True"
	else:
		print("ERROR: invalid " + name)
		exit()

def analyse_vegetable():
	if vegetable == "cabbage":
		return "True;False"
	else:
		return "False;True"

def analyse_nb_row():
	return return_interval(nb_row/100, "nb_row")

def analyse_length():
	tmp = []
	for l in length:
		tmp.append((float(l)-10)/90)
	return return_interval_array(tmp, "length")

def analyse_noise():
	tmp_X = []
	tmp_Y = []
	for n in noise_X:
		tmp_X.append(float(n)/5)
	for n in noise_Y:
		tmp_Y.append(float(n)/5)
	return return_interval_array(tmp_X, "noise_X") + ";" + return_interval_array(tmp_Y, "noise_Y")

def analyse_disappearence_probability():
	tmp = []
	for dp in disappearance_probability:
		tmp.append(float(dp)/30)
	return return_interval_array(tmp, "disappearance_probability")

def analyse_vegetable_density():
	vd_L = False
	vd_M = False
	vd_H = False

	for vd in vegetable_density:
		if int(vd) in [1,2]:
			vd_L = True
		elif int(vd) == 3:
			vd_M = True
		else:
			vd_H = True
	return str(vd_L) + ";" + str(vd_M) + ";" + str(vd_H)

def analyse_interval():
	if nb_row < 2:
		return "None;None;None"
	tmp = []
	for i in range(1, nb_row):
		tmp.append(((float(length[i])/float(length[i-1]))-0.9)*5)
	return return_interval_array(tmp, "interval")

def analyse_extremal():
	if nb_row < 3:
		return "None;None;None"
	return return_interval(((float(length[0])/float(length[-1])) - 0.9)*5, "extremal")

def analyse_first_length():
	return return_interval((float(length[0])-10)/90, "first_length")

def analyse_grass_density():
	tmp = []
	for gd in grass_density:
		tmp.append(float(gd)/5)
	return return_interval_array(tmp, "grass_density")

def analyse_gap():
	if nb_row == 1:
		return "None;None;None"
	tmp = []
	for g in gap:
		tmp.append((float(g)-55)/110)
	return return_interval_array(tmp, "gap")

def analyse_roughness():
	return return_interval(roughness, "roughness")

def analyse_persistence():
	return return_interval(persistence/0.7, "persistence")

with open(sys.argv[1] + "oz.csv", "r") as f:
	vegetable = f.readline()[:-1]
	nb_row = int(f.readline()[:-1])
	length = f.readline()[:-1].split(";")
	noise_X = f.readline()[:-1].split(";")
	noise_Y = f.readline()[:-1].split(";")
	disappearance_probability = f.readline()[:-1].split(";")
	vegetable_density = f.readline()[:-1].split(";")

	nb_weed_area = int(f.readline()[:-1])
	grass_density = f.readline()[:-1].split(";")

	nb_inner_track_width = int(f.readline()[:-1])
	gap = f.readline()[:-1].split(";")

	two_pass = f.readline()[:-1]
	is_first_track_outer = f.readline()[:-1]
	final_track_outer = f.readline()[:-1]
	is_track_side_at_left = f.readline()[:-1]
	is_first_uturn_right_side = f.readline()[:-1]

	roughness = float(f.readline()[:-1])
	persistence = float(f.readline()[:-1])

with open(sys.argv[2] + "analysis.csv", "a") as f:
	f.write(analyse_vegetable() + ";" + analyse_nb_row() + ";" + analyse_length() + ";" + analyse_noise() + ";" + analyse_disappearence_probability() + ";" + analyse_vegetable_density() + ";" + analyse_interval() + ";" + analyse_extremal() + ";" + analyse_first_length() + ";" + analyse_grass_density() + ";" + analyse_gap() + ";" + return_bool(two_pass, "two_pass") + ";" + return_bool(is_first_track_outer, "is_first_track_outer") + ";" + return_bool(final_track_outer, "final_track_outer") + ";" + return_bool(is_track_side_at_left, "is_track_side_at_left") + ";" + return_bool(is_first_uturn_right_side, "is_first_uturn_right_side") + ";" + analyse_roughness() + ";" + analyse_persistence() + "\n")

