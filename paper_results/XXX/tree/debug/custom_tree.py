import numpy as np
import os

class Node():
	def __init__(self, n, f, d):
		self.nb = n
		self.father = f
		self.depth = d

	def __repr__(self):
		return "\n\n--- Node ---" +\
				 "\nnb: " + str(self.nb) +\
				 "\nfather: " + str(self.father) +\
				 "\ndepth: " + str(self.depth)

def print_nodes():
	for n in node:
		print(n)

def get_dnode(d):
	dnode = []
	for n in node:
		if n.depth == d:
			dnode.append(n)
	return dnode

def get_children_array():
	for i in range(len(node)):
		children_array.append([])

	for n in node:
		if n.father != -1:
			children_array[n.father].append(n.nb)
	print(children_array)

def generate_tree():
	node.append(Node(0, -1, 0))
	
	current_depth = 1
	current_nb = 1
	
	while 1:
		nb_node = np.random.randint(5)
		#print("nb_node: ", nb_node)
		if nb_node == 0:
			return
		else:
			dnode = get_dnode(current_depth -1)
			for i in range(nb_node):
				f = np.random.randint(len(dnode))
				node.append(Node(current_nb, dnode[f].nb, current_depth))
				current_nb +=1
		current_depth +=1

def order_array():
	for i in range(1, len(node)-1):
		for j in range(len(node)-i):
			print(j, " - ", j+1)
			if node[j].nb > node[j+1].nb:
				tmp = node[j]
				node[j] = node[j+1]
				node[j+1] = tmp

def export_to_dot():
	with open("tree.gv", "w") as f:
		f.write("digraph G {\n")
		for n in node:
			if n.nb != 0:
				f.write("\t" + str(n.father) + "->" + str(n.nb) + "\n")
		f.write("}")
	os.system("dot -Tsvg tree.gv -o tree.svg")

def export_to_csv():
	with open("tree_graph.csv", "w") as f:
		for n in node:
			f.write(str(n.nb) + ";" + str(n.father) + ";" + str(n.depth))
			for i in children_array[n.nb]:
				f.write(";" + str(i))
			f.write("\n")

node = []
children_array = []
generate_tree()
get_children_array()
order_array()
#print_nodes()
export_to_dot()
export_to_csv()
