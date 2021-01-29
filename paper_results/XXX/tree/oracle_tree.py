import sys

MIN_N = 1
MAX_N = 50

nb_node_check = False
root_check = False
father_check = False
height_check = False
coherence_check = False

def compile_checkers_result():
	res = nb_node_check
	res = res or root_check
	res = res or father_check
	res = res or height_check
	res = res or coherence_check
	return res

def print_checkers_result():
	print("nb_node_check:     ", nb_node_check)
	print("root_check:        ", root_check)
	print("father_check:      ", father_check)
	print("height_check:      ", height_check)
	print("coherence_check:   ", coherence_check)

class Node():
	def __init__(self, n, f, h):
		self.nb = n
		self.father = f
		self.depth = h
		self.children = []

	def __repr__(self):
		return "\n\n--- Node ---" +\
				 "\nnb: " + str(self.nb) +\
				 "\nfather: " + str(self.father) +\
				 "\ndepth: " + str(self.depth) +\
				 "\nchildren: " + str(self.children)

def read_csv():
	with open(sys.argv[1] + "tree.csv", "r") as f:
		for line in f:
			tmp = line.split(";")
			tmp[-1] = tmp[-1][:-1]
			n = Node(int(tmp[0]), int(tmp[1]), int(tmp[2]))
			for c in tmp[3:]:
				n.children.append(int(c))
			node.append(n)

def check_nb_node():
	if not MIN_N <= len(node) <= MAX_N:
		nb_node_check = True

def check_root():
	if node[0].father != -1 or node[0].depth != 0:
		root_check = True

def check_father():
	for n in node[1:]:
		if n.father >= len(node):
			father_check = True

def check_height():
	height = 0
	for n in node:
		if n.depth > height:
			height = n.depth
	if height >= len(node):
		height_check = True

def check_coherence(i=0, counter=0, res=False):
	for c in node[i].children:
		if node[c].depth != node[i].depth+1:
			coherence_check = True
		counter += 1
		retro_counter = check_coherence(c, counter, res)
		counter += retro_counter
	if i == 0:
		if counter != len(node):
			coherence_check = True
	else:
		return counter

node = []
read_csv()
check_nb_node()
check_root()
check_father()
check_height()
check_coherence()
#print_checkers_result()

with open(sys.argv[2] + "oracle", "a") as f:
	f.write(str(compile_checkers_result()) + "\n")

