import sys

vegetable_check = False
nb_row_check = False
length_check = False
noise_X_check = False
noise_Y_check = False
disappearance_probability_check = False
vegetable_density_check = False
nb_weed_area_check = False
grass_density_check = False
nb_inner_track_width_check = False
gap_check = False
two_pass_check = False
is_first_track_outer_check = False
final_track_outer_check = False
is_track_side_at_left_check = False
is_first_uturn_right_side_check = False
roughness_check = False
persistence_check = False

length_coherence_check = False
length_interval_check = False
is_first_track_outer_coherence_check = False

def compile_checkers_result():
	res = vegetable_check
	res = res or nb_row_check
	res = res or length_check
	res = res or noise_X_check
	res = res or noise_Y_check
	res = res or disappearance_probability_check
	res = res or vegetable_density_check
	res = res or nb_weed_area_check
	res = res or grass_density_check
	res = res or nb_inner_track_width_check
	res = res or gap_check
	res = res or two_pass_check
	res = res or is_first_track_outer_check
	res = res or final_track_outer_check
	res = res or is_track_side_at_left_check
	res = res or is_first_uturn_right_side_check
	res = res or roughness_check
	res = res or persistence_check
	
	res = res or length_coherence_check
	res = res or length_interval_check
	res = res or is_first_track_outer_coherence_check
	return res

def print_checkers_result():
	print("vegetable_check:                      ", vegetable_check)
	print("nb_row_check:                         ", nb_row_check)
	print("length_check:                         ", length_check)
	print("noise_X_check:                        ", noise_X_check)
	print("noise_Y_check:                        ", noise_Y_check)
	print("disappearance_probability_check:      ", disappearance_probability_check)
	print("vegetable_density_check:              ", vegetable_density_check)
	print("nb_weed_area_check:                   ", nb_weed_area_check)
	print("grass_density_check:                  ", grass_density_check)
	print("nb_inner_track_width_check:           ", nb_inner_track_width_check)
	print("gap_check:                            ", gap_check)
	print("two_pass_check:                       ", two_pass_check)
	print("is_first_track_outer_check:           ", is_first_track_outer_check)
	print("final_track_outer_check:              ", final_track_outer_check)
	print("is_track_side_at_left_check:          ", is_track_side_at_left_check)
	print("is_first_uturn_right_side_check:      ", is_first_uturn_right_side_check)
	print("roughness_check:                      ", roughness_check)
	print("persistence_check:                    ", persistence_check)
	print("vegetable_check:                      ", vegetable_check)

	print("length_coherence_check:               ", length_coherence_check)
	print("length_interval_check:                ", length_interval_check)
	print("is_first_track_outer_coherence_check: ", is_first_track_outer_coherence_check)

def check_param(param, a, b):
	for p in param:
		if not a <= float(p) <= b:
			return True
	return False

def check_bool(param):
	if not param in ["True", "False"]:
		return True
	return False

def check_length_coherence():
	if not nb_row == nb_inner_track_width + 1:
		return True
	if not nb_row + 1 == nb_weed_area:
		return True
	return False

def check_length_interval():
	for i in range(1, nb_row):
		if not 0.8999 <= float(length[i])/float(length[i-1]) <= 1.1001:
			return True
	if not 0.8999 <= float(length[0])/float(length[-1]) <= 1.1001:
		return True
	return False

def check_is_first_track_outer_coherence():
	if nb_row == 1:
		if is_first_track_outer != "True":
			return True
	return False

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

if not vegetable in ["leek", "cabbage"]:
	vegetable_check = True
if not 1 <= nb_row <= 100:
	nb_row_check = True
if check_param(length, 10, 100):
	length_check = True
if check_param(noise_X, 0, 5):
	noise_X_check = True
if check_param(noise_Y, 0, 5):
	noise_Y_check = True
if check_param(disappearance_probability, 0, 30):
	disappearance_probability_check = True
if check_param(vegetable_density, 1, 5):
	vegetable_density_check = True
if not 2 <= nb_weed_area <= 101:
	nb_weed_area_check = True
if check_param(grass_density, 0, 5):
	grass_density_check = True
if not 0 <= nb_inner_track_width <= 99:
	nb_inner_track_width_check = True
if nb_row > 1:
	if check_param(gap, 55, 165):
		gap_check = True
if check_bool(two_pass):
	two_pass_check = True
if check_bool(is_first_track_outer):
	is_first_track_outer_check = True
if check_bool(final_track_outer):
	final_track_outer_check = True
if check_bool(is_track_side_at_left):
	is_track_side_at_left_check = True
if check_bool(is_first_uturn_right_side):
	is_first_uturn_right_side_check = True
if not 0 <= roughness <= 1:
	roughness_check = True
if not 0 <= persistence <= 0.7:
	persistence_check = True

check_length_coherence()
check_length_interval()
check_is_first_track_outer_coherence()
#print_checkers_result()

with open(sys.argv[2] + "oracle", "a") as f:
	f.write(str(compile_checkers_result()) + "\n")

