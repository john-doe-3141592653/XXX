import numpy as np

def generate_size():
	s = np.random.randint(5, 30)
	print(s)
	return s, s

def get_random_increment():
	return np.random.randint(int(255/img_w))

def generate_pixels(w, h):
	p = [0]*(w*h)

	for i in range(h):
		for j in range(w):
			if i == 0 and j == 0:
				p[i*w + j] = get_random_increment()
			else:
				if i == 0:
					p[i*w + j] = min(p[i*w + j-1] + get_random_increment(), 255)
				elif j ==0:
					p[i*w + j] = min(p[(i-1)*w + j] + get_random_increment(), 255)
				else:
					p[i*w + j] = min(max(p[i*w + j-1], p[(i-1)*w + j])  + get_random_increment(), 255)
	for i in range(h):
		for j in range(w):
			p[i*w + j] = tuple((p[i*w + j], p[i*w + j], p[i*w + j]))
	return p

def add_pixel(f, p):
	for i in p:
		f.write(i.to_bytes(1, 'little'))

def add_padding(f, w):
	p= (4-(3*w)%4)%4
	for i in range(p):
		f.write((0).to_bytes(1, 'little'))

def add_pixels(w, h, p):
	with open("./bmp.bmp", "ab") as f:
		for i in range(h):
			for j in range(w):
				add_pixel(f, p[h*i+j])
			add_padding(f, w)


img_w, img_h = generate_size()
pixels = generate_pixels(img_w, img_h)

ID_field = "BM"
padding = img_h*((4-(img_w*3)%4)%4)
offset = 54
size = offset + img_w*img_h*3 + padding

dib_header_size = 40
nb_color_planes = 1
bit_per_pixel = 24
compression_method = 0
data_size = 16
print_resolution_w = 2835
print_resolution_h = 2835
nb_color = 0
nb_important_color = 0

#red_pixel = (0, 0, 255)
#white_pixel = (255, 255, 255)
#blue_pixel = (255, 0, 0)
#green_pixel = (0, 255, 0)
#black_pixel = (0, 0, 0)

with open("./bmp.bmp", "wb") as f:
	f.write(bytes(ID_field, 'utf-8'))
	f.write(size.to_bytes(4, 'little'))
	#f.write((size-5-(4-(5*3)%2)).to_bytes(4, 'little'))
	f.write((0).to_bytes(4, 'little'))
	f.write((54).to_bytes(4, 'little'))
	f.write(dib_header_size.to_bytes(4, 'little'))
	f.write(img_w.to_bytes(4, 'little'))
	f.write(img_h.to_bytes(4, 'little'))
	f.write(nb_color_planes.to_bytes(2, 'little'))
	f.write(bit_per_pixel.to_bytes(2, 'little'))
	f.write(compression_method.to_bytes(4, 'little'))
	f.write(data_size.to_bytes(4, 'little'))
	f.write(print_resolution_w.to_bytes(4, 'little'))
	f.write(print_resolution_h.to_bytes(4, 'little'))
	f.write(nb_color.to_bytes(4, 'little'))
	f.write(nb_important_color.to_bytes(4, 'little'))

add_pixels(img_w, img_h, pixels)

