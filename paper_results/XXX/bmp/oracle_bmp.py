import sys

MIN_W = 10
MAX_W = 100

ID_field_check = False
size_check = False
unused_check = False
offset_check = False
dib_header_size_check = False
img_w_check = False
img_h_check = False
nb_color_plane_check = False
bit_per_pixel_check = False
compression_method_check = False
data_size_check = False
print_resolution_w_check = False
print_resolution_h_check = False
nb_color_check = False
nb_important_color_check = False

size_coherence_check = False
gray_check = False
slope_check = False
zeros_padding_check = False

def extract_pixel(f):
	r = int.from_bytes(f.read(1), "little")
	g = int.from_bytes(f.read(1), "little")
	b = int.from_bytes(f.read(1), "little")
	if r != g or g != b:
		gray_check = True
	return r

def extract_padding(f, n):
	padding = int.from_bytes(f.read(n), "little")
	if padding != 0:
		zeros_padding_check = True

def compile_checkers_result():
	res = ID_field_check
	res = res or size_check 
	res = res or unused_check
	res = res  or offset_check
	res = res or dib_header_size_check
	res = res or img_w_check
	res = res or img_h_check
	res = res or nb_color_plane_check
	res = res or bit_per_pixel_check
	res = res or compression_method_check
	res = res or data_size_check
	res = res or print_resolution_w_check
	res = res or print_resolution_h_check
	res = res or nb_color_check
	res = res or nb_important_color_check

	res = res or size_coherence_check
	res = res or gray_check
	res = res or slope_check
	res = res or zeros_padding_check
	return res

def print_checkers_result():
	print("ID_field_check:           ", ID_field_check)
	print("size_check:               ", size_check)
	print("unused_check:             ", unused_check)
	print("offset_check:             ", offset_check)
	print("dib_header_size_check:    ", dib_header_size_check)
	print("img_w_check:              ", img_w_check)
	print("img_h_check:              ", img_h_check)
	print("nb_color_plane_check:     ", nb_color_plane_check)
	print("bit_per_pixel_check:      ", bit_per_pixel_check)
	print("compression_method_check: ", compression_method_check)			
	print("data_size_check:          ", data_size_check)
	print("print_resolution_w_check: ", print_resolution_w_check)
	print("print_resolution_h_check: ", print_resolution_h_check)
	print("nb_color_check:           ", nb_color_check)
	print("nb_important_color_check: ", nb_important_color_check)

	print("size_coherence_check:     ", size_coherence_check)
	print("gray_check:               ", gray_check)
	print("slope_check:              ", slope_check)
	print("zeros_padding_check:      ", zeros_padding_check)

def build_size_array():
	size_array = []
	for i in range(MIN_W, MAX_W +1):
		s = 54 + 3*i*i + i*((4-(3*i)%4)%4)
		size_array.append(s)
	return size_array

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

	if ID_field != "BM":
		ID_field_check = True
	if not size in build_size_array():
		size_check = True
	if unused != 0:
		unused_check = True
	if offset != 54:
		offset_check = True
	if dib_header_size != 40:
		dib_header_size_check = True
	if not MIN_W <= img_w <= MAX_W:
		img_w_check = True
	if not MIN_W <= img_h <= MAX_W:
		img_h_check = True
	if nb_color_plane != 1:
		nb_color_plane_check = True
	if bit_per_pixel != 24:
		bit_per_pixel_check = True 
	if compression_method != 0:
		compression_method_check = True
	if data_size != 16:
		data_size_check = True
	if print_resolution_w != 2835:
		print_resolkution_w_check = True
	if print_resolution_h != 2835:
		print_resolkution_h_check = True
	if nb_color != 0:
		nb_color_check = True
	if nb_important_color != 0:
		nb_important_color_check = True

	if size != 54 + 3*img_w*img_w + img_w*((4-(3*img_w)%4)%4) or img_w != img_h:
		size_coherence_check = True
	for i in range(img_h):
		gray_value_array = []
		for j in range(img_w):
			gray_value_array.append(extract_pixel(f))
		tmp = 0
		for j, gray_value in enumerate(gray_value_array):
			if j > 0 and gray_value < tmp:
					slope_check = True
			tmp = gray_value
		extract_padding(f, (4-(3*img_w)%4)%4)

#print_checkers_result()
with open(sys.argv[2] + "oracle", "a") as f:
	f.write(str(compile_checkers_result()) + "\n")
