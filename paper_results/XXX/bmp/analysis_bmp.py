import sys

def extract_pixel(f):
	r = int.from_bytes(f.read(1), "little")
	g = int.from_bytes(f.read(1), "little")
	b = int.from_bytes(f.read(1), "little")
	if r != g or g != b:
		gray_check = True
	return r

def extract_padding(f, n):
	padding = int.from_bytes(f.read(n), "little")

def return_interval(param, name):
	#print(name + ": " + str(param))
	if 0 <= param < 0.33:
		return "True;False;False"
	elif 0.33 <= param <= 0.67:
		return "False;True;False"
	elif 0.67 < param <= 1:
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
		if 0 <= p < 0.33:
			L = True
		elif 0.33 <= p <= 0.67:
			M = True
		elif 0.67 < p <= 1:
			H = True
		else:
			print("ERROR: invalid " + name)
			exit()

	return str(L) + ";" + str(M) + ";" + str(H)

def analyse_size():
	return return_interval((img_w-10)/90, "size")

def analyse_gray():
	tmp = []
	for i in range(img_w):
		for j in range(img_w):
			tmp.append(pixel_array[i][j]/255)
	return return_interval_array(tmp, "gray")

def analyse_padding():
	tmp = (4-(3*img_w)%4)%4
	if tmp == 0:
		return "True;False;False;False"
	elif tmp == 1:
		return "False;True;False;False"
	elif tmp == 2:
		return "False;False;True;False"
	else:
		return "False;False;False;True"

def analyse_min_max():
	min = 255
	max = 0
	for i in range(img_w):
		for j in range(img_w):
			tmp = pixel_array[i][j]
			if tmp < min:
				min = tmp
			if tmp > max:
				max = tmp
	return return_interval(min/255, "min") + ";" + return_interval(max/255, "max")

def analyse_border():
	tmp_H = []
	tmp_V = []
	for i in range(img_w):
		tmp_H.append((pixel_array[i][-1] - pixel_array[i][0])/255)
		tmp_V.append((pixel_array[-1][i] - pixel_array[0][i])/255)
	return return_interval_array(tmp_H, "horizontal_border") + ";" + return_interval_array(tmp_V, "vertical_border")

def analyse_interval():
	tmp_H = []
	tmp_V = []

	for i in range(img_w):
		for j in range(i, img_w-1):
			tmp_H.append((pixel_array[i][j+1] - pixel_array[i][j])/255)
			tmp_V.append((pixel_array[j+1][i] - pixel_array[j][i])/255)
	return return_interval_array(tmp_H, "horizontal_interval") + ";" + return_interval_array(tmp_V, "vertical_interval")

pixel_array = []
img_w = 0

with open(sys.argv[1] + "bmp.bmp", "rb") as f:
	ID_field = f.read(2).decode("utf-8")
	size = int.from_bytes(f.read(4), "little")
	unused = int.from_bytes(f.read(4), "little")
	offset = int.from_bytes(f.read(4), "little")
	dib_header_size = int.from_bytes(f.read(4), "little")
	img_w = int.from_bytes(f.read(4), "little")
	img_h = int.from_bytes(f.read(4), "little")
	nb_color_plane = int.from_bytes(f.read(2), "little")
	bit_per_pixel = int.from_bytes(f.read(2), "little")
	compression_method = int.from_bytes(f.read(4), "little")
	data_size = int.from_bytes(f.read(4), "little")
	print_resolution_w = int.from_bytes(f.read(4), "little")
	print_resolution_h = int.from_bytes(f.read(4), "little")
	nb_color = int.from_bytes(f.read(4), "little")
	nb_important_color = int.from_bytes(f.read(4), "little")

	for i in range(img_h):
		tmp = []
		for j in range(img_w):
			tmp.append(extract_pixel(f))
		pixel_array.append(tmp)
		extract_padding(f, (4-(3*img_w)%4)%4)

with open(sys.argv[2] + "analysis.csv", "a") as f:
	f.write(analyse_size() + ";"+ analyse_gray() + ";" + analyse_padding() + ";" + analyse_min_max() + ";" + analyse_border() + ";" + analyse_interval() + "\n")
