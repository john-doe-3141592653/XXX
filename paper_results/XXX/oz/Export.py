def export(root_node, path):
	with open(path + "oz.csv", "w") as f:
		f.write(str(root_node.get_child_n("field").get_parameter_n("vegetable").values[0]) + "\n")

		nb_row = root_node.get_child_n("field").get_child_n("row").nb_instances
		f.write(str(nb_row) + "\n")
		length = ""
		noise_X = ""
		noise_Y = ""
		disappearance_probability = ""
		vegetable_density = ""
		
		for i in range(nb_row):
			length += str(root_node.get_child_n("field").get_child_n("row").get_parameter_n("length", i).values[0]) + ";"
			noise_X += str(root_node.get_child_n("field").get_child_n("row").get_parameter_n("noise_X", i).values[0]) + ";"
			noise_Y += str(root_node.get_child_n("field").get_child_n("row").get_parameter_n("noise_Y", i).values[0]) + ";"
			disappearance_probability += str(root_node.get_child_n("field").get_child_n("row").get_parameter_n("disappearance_probability", i).values[0]) + ";"
			vegetable_density += str(root_node.get_child_n("field").get_child_n("row").get_parameter_n("vegetable_density", i).values[0]) + ";"
		f.write(length[:-1] + "\n")
		f.write(noise_X[:-1] + "\n")
		f.write(noise_Y[:-1] + "\n")
		f.write(disappearance_probability[:-1] + "\n")
		f.write(vegetable_density[:-1] + "\n")
		
		nb_weed_area = root_node.get_child_n("field").get_child_n("weed_area").nb_instances
		f.write(str(nb_weed_area) + "\n")
		grass_density = ""
		for i in range(nb_weed_area):
			grass_density += str(root_node.get_child_n("field").get_child_n("weed_area").get_parameter_n("grass_density", i).values[0]) + ";"
		f.write(grass_density[:-1] + "\n")
	
		if root_node.get_child_n("field").get_child_n("inner_track_width") == None:
			f.write("0\n\n")
		else:
			nb_inner_track_width = root_node.get_child_n("field").get_child_n("inner_track_width").nb_instances
			f.write(str(nb_inner_track_width) + "\n")
			gap = ""
			for i in range(nb_inner_track_width):
				gap += str(root_node.get_child_n("field").get_child_n("inner_track_width").get_parameter_n("gap", i).values[0]) + ";"
			f.write(gap[:-1] + "\n")
	
		f.write(str(root_node.get_child_n("mission").get_parameter_n("two_pass").values[0]) + "\n")
		f.write(str(root_node.get_child_n("mission").get_parameter_n("is_first_track_outer").values[0]) + "\n")
		f.write(str(root_node.get_child_n("mission").get_parameter_n("final_track_outer").values[0]) + "\n")
		f.write(str(root_node.get_child_n("mission").get_parameter_n("is_track_side_at_left").values[0]) + "\n")
		f.write(str(root_node.get_child_n("mission").get_parameter_n("is_first_uturn_right_side").values[0]) + "\n")
	
		f.write(str(root_node.get_child_n("terrain").get_child_n("heightmap").get_parameter_n("roughness").values[0]) + "\n")
		f.write(str(root_node.get_child_n("terrain").get_child_n("heightmap").get_parameter_n("persistence").values[0]) + "\n")


