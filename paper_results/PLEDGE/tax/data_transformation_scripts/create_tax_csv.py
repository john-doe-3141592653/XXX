import statistics as stat
import os

def array_to_string(array):
	res = ""
	for a in array:
		res += str(a) + ";"
	return res[:-1] + "\n"

for i in range(10):
	for j in range(100):
		none_id = ""
		vision_id = ""
		a_id = ""
		fr_id = ""
		lu_id = ""
		de_id = ""
		be_id = ""
		other_id = ""
		
		nb_tax_payer = -1
		disability_type = []
		is_resident = []
		address = []
		income = []
		country = {}
		is_local = {}
		nb_none = -1
		nb_vision = -1
		nb_a = -1

		line_counter = 0
		previous_lines = []
		save_line_address = 0
		save_line_income = 0
		tmp_address = []
		tmp_income = []

		

		with open("./" + str(i) + "/test_case_" + str(j) + "/tax.uml", "r") as f:
			for line in f:
				line_counter += 1
				if "Tax_payer" in line:
					nb_tax_payer += 1
				if "None" in line and "ownedLiteral" in line:
					none_id = line.split(" ")[5][8:][:-1]
				elif "Vision" in line and "ownedLiteral" in line:
					vision_id = line.split(" ")[5][8:][:-1]
				elif "\"A\"" in line and "ownedLiteral" in line:
					a_id = line.split(" ")[5][8:][:-1]
				elif "\"FR\"" in line and "ownedLiteral" in line:
					fr_id = line.split(" ")[5][8:][:-1]
				elif "\"LU\"" in line and "ownedLiteral" in line:
					lu_id = line.split(" ")[5][8:][:-1]
				elif "\"DE\"" in line and "ownedLiteral" in line:
					de_id = line.split(" ")[5][8:][:-1]
				elif "\"BE\"" in line and "ownedLiteral" in line:
					be_id = line.split(" ")[5][8:][:-1]
				elif "\"Other\"" in line and "ownedLiteral" in line:
					other_id = line.split(" ")[5][8:][:-1]
				elif none_id != "" and none_id in line:
					nb_none += 1
					if nb_none >= 0:
						disability_type.append("none")
				elif vision_id != "" and vision_id in line:
					nb_vision += 1
					if nb_vision >= 0:
						disability_type.append("vision")
				elif a_id != "" and a_id in line:
					nb_a += 1
					if nb_a >= 0:
						disability_type.append("a")
				elif "is_resident" in line and not "ownedAttribute" in line:
					if "value=" in line:
						is_resident.append(True)
					else:
						is_resident.append(False)
				elif "address" in line and "instance" in line:
					tmp = line.split(" ")[10][10:][:-4]

					if save_line_address == 0:
						save_line_address = line_counter
					if line_counter < save_line_address + 3:
						tmp_address.append(tmp)
					else:
						address.append(tmp_address)
						tmp_address = []
						tmp_address.append(tmp)
						save_line_address = line_counter
				elif "country" in line:
					if not " type" in line:
						tmp = line.split(" ")[10][10:][:-4]
						if tmp == fr_id:
							tmp = "FR"
						elif tmp == lu_id:
							tmp = "LU"
						elif tmp == de_id:
							tmp = "DE"
						elif tmp == be_id:
							tmp = "BE"
						else #other
							tmp = "OTHER"
						country[previous_lines[1].split(" ")[4][8:][:-1]] = tmp
				elif "income" in line and "instance" in line and not "Tax_card" in previous_lines[1]:
					tmp = line.split(" ")[10][10:][:-4]
				
					if save_line_income == 0:
						save_line_income = line_counter
					if line_counter < save_line_income + 3:
						tmp_income.append(tmp)
					else:
						income.append(tmp_income)
						tmp_income = []
						tmp_income.append(tmp)
						save_line_income = line_counter
				elif "is_local" in line and "Pension" in previous_lines[1]:
					if "value=" in line:
						tmp = ("P", line.split(" ")[-1][7:][:-4])
					else:
						tmp = ("P", "false")
					is_local[previous_lines[1].split(" ")[4][8:][:-1]] = tmp
				elif "is_local" in line and "Employment" in previous_lines[1]:
					if "value=" in line:
						tmp = ("E", line.split(" ")[-1][7:][:-4])
					else:
						tmp = ("E", "false")
					is_local[previous_lines[1].split(" ")[4][8:][:-1]] = tmp
				elif "is_local" in line and "Other" in previous_lines[1]:
					if "value=" in line:
						tmp = ("O", line.split(" ")[-1][7:][:-4])
					else:
						tmp = ("O", "false")
					is_local[previous_lines[1].split(" ")[4][8:][:-1]] = tmp


					
				if len(previous_lines) > 2:
					previous_lines = previous_lines[1:]
				previous_lines.append(line)



		address.append(tmp_address)
		income.append(tmp_income)

		with open("./" + str(i) + "/test_case_" + str(j) + "/tax.csv", "w") as f:
			f.write(str(nb_tax_payer) + "\n")
			for k in range(nb_tax_payer):
				tmp = ""
				tmp += "1920;"
				if disability_type[k] == "none":
					tmp += "0.0;"
				else:
					tmp += "1.0;"
				tmp += disability_type[k] + ";"
				tmp += str(is_resident[k]) + "\n"
				for add in address[k]:
					tmp += country[add] + ";"
				tmp = tmp[:-1] + "\n0\n"
				p = []
				e = []
				o = []
				for inc in income[k]:
					if is_local[inc][0] == "P":
						p.append(is_local[inc][1])
					elif is_local[inc][0] == "E":
						e.append(is_local[inc][1])
					else:
						o.append(is_local[inc][1])
				tmp += str(len(p)) + "\n"
				if len(p) > 0:
					for isloc in p:
						tmp += isloc + ";"
					tmp = tmp[:-1] + "\n"
				tmp += str(len(e)) + "\n"
				if len(e) > 0:
					for isloc in e:
						tmp += isloc + ";"
					tmp = tmp[:-1] + "\n"
				tmp += str(len(o)) + "\n"
				if len(o) > 0:
					for isloc in o:
						tmp += isloc + ";"
					tmp = tmp[:-1] + "\n"
				f.write(tmp)
