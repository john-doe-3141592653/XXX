class Node():
	def __init__(self, n, f, d):
		self.nb = n
		self.father = f
		self.depth = d
		self.children = []
		
	def __repr__(self):
		return "\n\n--- Node ---" +\
			"\nnb: " + str(self.nb) +\
			"\nfather: " + str(self.father) +\
			"\ndepth: " + str(self.depth)

def export(root_node, path):
	node = []
	
	for i in range(root_node.get_child_n("node").nb_instances):
		node.append(Node(i, root_node.get_child_n("node").get_parameter_n("father", i).values[0], root_node.get_child_n("node").get_parameter_n("depth", i).values[0]))
	
	for i in range(len(node)):
		if node[i].father != -1:
			node[node[i].father].children.append(i)

	with open(path + "tree.gv", "w") as f:
		f.write("digraph G {\n")
		for n in node:
			if n.nb != 0:
				f.write("\t" + str(n.father) + "->" + str(n.nb) + "\n")
		f.write("}")
		#os.system("dot -Tsvg tree_graph.gv -o tree_graph.svg")

	with open(path + "tree.csv", "w") as f:
		for n in node:
			f.write(str(n.nb) + ";" + str(n.father) + ";" + str(n.depth))
			for i in n.children:
				f.write(";" + str(i))
			f.write("\n")
