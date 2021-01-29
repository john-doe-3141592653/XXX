import statistics as stat
import os

def array_to_string(array):
	res = ""
	for a in array:
		res += str(a) + ";"
	return res[:-1] + "\n"

for i in range(10):
	for j in range(100):
		nb_cabbage = -1
		nb_leek = -1
		nb_row = -1
		nb_weed_area = -1
		cabbage_id = ""
		leek_id = ""
		length = []
		noise_x = []
		noise_y = []
		disapearence_probability = []
		vegetable_density = []
		grass_density = []
		gap = []
		two_pass = False
		is_first_track_outer = False
		final_track_outer = False
		is_track_side_at_left = False
		is_first_uturn_right_side = False
		roughness = 0
		persistence = 0

		with open("./" + str(i) + "/test_case_" + str(j) + "/oz.uml", "r") as f:
			for line in f:
				if "rows" in line:
					nb_row += 1
				if "CABBAGE" in line:
					cabbage_id = line.split(" ")[5][:-1][8:]
				elif "LEEK" in line:
					leek_id = line.split(" ")[5][:-1][8:]
				if cabbage_id != "" and cabbage_id in line:
					nb_cabbage += 1
				if leek_id != "" and leek_id in line:
					nb_leek += 1
				if "length" in line and "value=" in line:
					length.append(line.split(" ")[-1][7:][:-4])
				if "vegetable_density" in line and "value=" in line:
					vegetable_density.append(line.split(" ")[-1][7:][:-4])
				if "two_pass" in line and "value=" in line:
					two_pass = True
				if "is_first_track_outer" in line and "value=" in line:
					is_first_track_outer = True
				if "final_track_outer" in line and "value=" in line:
					final_track_outer = True
				if "is_track_side_at_left" in line and "value=" in line:
					is_track_side_at_left = True
				if "is_first_uturn_right_side" in line and "value=" in line:
					is_first_uturn_right_side = True

		if nb_cabbage == 1:
			vegetable = "cabbage"
		else:
			vegetable = "leek"
		for l in length:
			noise_x.append(0)
			noise_y.append(0)
			disapearence_probability.append(0)
			grass_density.append(0)
			gap.append(55)
		grass_density.append(0)
		gap.pop()

		with open("./" + str(i) + "/test_case_" + str(j) + "/oz.csv", "w") as f:
			f.write(vegetable + "\n")
			f.write(str(nb_row) + "\n")
			f.write(array_to_string(length))
			f.write(array_to_string(noise_x))
			f.write(array_to_string(noise_y))
			f.write(array_to_string(disapearence_probability))
			f.write(array_to_string(vegetable_density))
			f.write(str(len(grass_density)) + "\n")
			f.write(array_to_string(grass_density))
			f.write(str(len(gap)) + "\n")
			f.write(array_to_string(gap))
			f.write(str(two_pass) + "\n")
			f.write(str(is_first_track_outer) + "\n")
			f.write(str(final_track_outer) + "\n")
			f.write(str(is_track_side_at_left) + "\n")
			f.write(str(is_first_uturn_right_side) + "\n")
			f.write(str(roughness) + "\n")
			f.write(str(persistence) + "\n")

