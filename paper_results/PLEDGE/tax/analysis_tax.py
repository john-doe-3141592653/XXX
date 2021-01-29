import sys

class Physical_person():
	def __init__(self, by, dr, dt, ad):
		self.birth_year = by
		self.disability_rate = dr
		self.disability_type = dt
		self.address = ad

	def __repr__(self):
		return "birth_year: " + str(self.birth_year) + "\n" +\
			   "disability_rate: " + str(self.disability_rate) + "\n" +\
			   "disability_type: " + str(self.disability_type) + "\n" +\
			   "address: " + str(self.address) + "\n"

class Tax_payer(Physical_person):
	def __init__(self, by, dr, dt, ad, ir):
		Physical_person.__init__(self, by, dr, dt, ad)
		self.is_resident = ir
		self.children = []
		self.income_pension = []
		self.income_employment = []
		self.income_other = []

	def __repr__(self):
		return Physical_person.__repr__(self) +\
			   "is_resident: " + str(self.is_resident) + "\n" +\
			   "nb_child: " + str(len(self.children)) + "\n" +\
			   "income_pension: " + str(self.income_pension) + "\n" +\
			   "income_employment: " + str(self.income_employment) + "\n" +\
			   "income_other: " + str(self.income_other) + "\n"

class Child(Physical_person):
	def __init__(self, by, dr, dt, ad):
		Physical_person.__init__(self, by, dr, dt, ad)

	def __repr__(self):
		return Physical_person.__repr__(self)

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

def analyse_nb_tax_payer():
	return return_interval((nb_tax_payer-1)/100, "nb_tax_payer")

def analyse_birth_year():
	tmp = []
	for t in tax_payer_array:
		tmp.append((t.birth_year-1920)/100)
	return return_interval_array(tmp, "birth_year")

def analyse_disability_rate():
	tmp = []
	for t in tax_payer_array:
		tmp.append(t.disability_rate)
	return return_interval_array(tmp, "disability_rate")

def analyse_disability_type():
	type_none = False
	type_vision = False
	type_a = False

	for t in tax_payer_array:
		if t.disability_type == "None":
			type_none = True
		elif t.disability_type == "Vision":
			type_vision = True
		else:
			type_a = True
	return str(type_none) + ";" + str(type_vision) + ";" + str(type_a)

def analyse_is_resident():
	tr = False
	fa = False

	for t in tax_payer_array:
		if t.is_resident == "True":
			tr = True
		else:
			fa = True
	return str(tr) + ";" + str(fa)

def analyse_tax_payer_nb_address():
	tmp = []
	for t in tax_payer_array:
		tmp.append((len(t.address)-1)/2)
	return return_interval_array(tmp, "tax_payer_nb_address")

def analyse_tax_payer_address():
	lu = False
	fr = False
	be = False
	de = False
	ot = False

	for t in tax_payer_array:
		for a in t.address:
			if a == "LU":
				lu = True
			elif a == "FR":
				fr = True
			elif a == "BE":
				be = True
			elif a == "DE":
				de = True
			else:
				ot = True
	return str(lu) + ";" + str(fr) + ";" + str(be) + ";" + str(de) + ";" + str(ot)

def analyse_nb_child():
	zer = False
	one = False
	two = False
	thr = False

	for t in tax_payer_array:
		nb_child = len(t.children)
		if nb_child == 0:
			zer = True
		elif nb_child == 1:
			one = True
		elif nb_child == 2:
			two = True
		else:
			thr = True
	return str(zer) + ";" + str(one) + ";" + str(two) + ";" + str(thr)

def analyse_child_birth_year():
	tmp = []
	for t in tax_payer_array:
		for c in t.children:
			tmp.append((c.birth_year-1920)/100)
	return return_interval_array(tmp, "child_birth_year")

def analyse_child_disability_rate():
	tmp = []
	for t in tax_payer_array:
		for c in t.children:
			tmp.append(t.disability_rate)
	return return_interval_array(tmp, "child_disability_rate")

def analyse_child_disability_type():
	type_none = False
	type_vision = False
	type_a = False
	
	for t in tax_payer_array:
		for c in t.children:
			if c.disability_type == "None":
				type_none = True
			elif c.disability_type == "Vision":
				type_vision = True
			else:
				type_a = True
	return str(type_none) + ";" + str(type_vision) + ";" + str(type_a)

def analyse_child_nb_address():
	tmp = []
	for t in tax_payer_array:
		for c in t.children:
			tmp.append((len(t.address)-0.5)/3)
	return return_interval_array(tmp, "child_nb_address")

def analyse_child_address():
	lu = False
	fr = False
	be = False
	de = False
	ot = False
	
	for t in tax_payer_array:
		for c in t.children:
			for a in t.address:
				if a == "LU":
					lu = True
				elif a == "FR":
					fr = True
				elif a == "BE":
					be = True
				elif a == "DE":
					de = True
				else:
					ot = True
	return str(lu) + ";" + str(fr) + ";" + str(be) + ";" + str(de) + ";" + str(ot)

def analyse_nb_pension():
	zer = False
	one = False
	two = False
	thr = False
	
	for t in tax_payer_array:
		nb_pension = len(t.income_pension)
		if nb_pension == 0:
			zer = True
		elif nb_pension == 1:
			one = True
		elif nb_pension == 2:
			two = True
		else:
			thr = True
	return str(zer) + ";" + str(one) + ";" + str(two) + ";" + str(thr)

def analyse_nb_employment():
	zer = False
	one = False
	two = False
	thr = False
	
	for t in tax_payer_array:
		nb_employment = len(t.income_employment)
		if nb_employment == 0:
			zer = True
		elif nb_employment == 1:
			one = True
		elif nb_employment == 2:
			two = True
		else:
			thr = True
	return str(zer) + ";" + str(one) + ";" + str(two) + ";" + str(thr)

def analyse_nb_other():
	zer = False
	one = False
	two = False
	thr = False
	
	for t in tax_payer_array:
		nb_other = len(t.income_other)
		if nb_other == 0:
			zer = True
		elif nb_other == 1:
			one = True
		elif nb_other == 2:
			two = True
		else:
			thr = True
	return str(zer) + ";" + str(one) + ";" + str(two) + ";" + str(thr)

def analyse_pension_is_local():
	tr = False
	fa = False
	
	for t in tax_payer_array:
		for i in t.income_pension:
			if i == "True":
				tr = True
			else:
				fa = True
	return str(tr) + ";" + str(fa)

def analyse_employment_is_local():
	tr = False
	fa = False
	
	for t in tax_payer_array:
		for i in t.income_employment:
			if i == "True":
				tr = True
			else:
				fa = True
	return str(tr) + ";" + str(fa)

def analyse_other_is_local():
	tr = False
	fa = False
	
	for t in tax_payer_array:
		for i in t.income_other:
			if i == "True":
				tr = True
			else:
				fa = True
	return str(tr) + ";" + str(fa)

def analyse_nb_income():
	tmp = []
	for t in tax_payer_array:
		tmp.append((len(t.income_pension) + len(t.income_employment) + len(t.income_other) - 1)/2)
	return return_interval_array(tmp, "nb_income")

def analyse_lu_address():
	no_lu = False
	lu = False
	all_lu = False

	for t in tax_payer_array:
		counter = 0
		for a in t.address:
			if a == "LU":
				counter += 1

		if counter == len(t.address):
			all_lu = True
		elif counter == 0:
			no_lu = True
		else:
			lu = True
	return str(no_lu) + ";" + str(lu) + ";" + str(all_lu)

def analyse_c4():
	pension_lu = False
	employment_lu = False
	other_lu = False

	for t in tax_payer_array:
		tmp = False
		for a in t.address:
			if a == "LU":
				tmp = True

		if tmp:
			for i in t.income_pension:
				if i == "True":
					pension_lu = True
			for i in t.income_employment:
				if i == "True":
					employment_lu = True
			for i in t.income_other:
				if i == "True":
					other_lu = True
	return str(pension_lu) + ";" + str(employment_lu) + ";" + str(other_lu)

tax_payer_array = []

with open(sys.argv[1] + "tax.csv", "r") as f:
	nb_tax_payer = int(f.readline()[:-1])
	for i in range(nb_tax_payer):
		tmp = f.readline()[:-1].split(";")
		address = f.readline()[:-1].split(";")
		t = Tax_payer(int(tmp[0]), float(tmp[1]), tmp[2], address, tmp[3])
		
		nb_child = int(f.readline()[:-1])
		for j in range(nb_child):
			tmp = f.readline()[:-1].split(";")
			address = f.readline()[:-1].split(";")
			c = Child(int(tmp[0]), float(tmp[1]), tmp[2], address)
			t.children.append(c)

		nb_income_pension = int(f.readline()[:-1])
		if nb_income_pension > 0:
			t.income_pension = f.readline()[:-1].split(";")
		
		nb_income_employment = int(f.readline()[:-1])
		if nb_income_employment > 0:
			t.income_employment = f.readline()[:-1].split(";")
				
		nb_income_other = int(f.readline()[:-1])
		if nb_income_other > 0:
			t.income_other = f.readline()[:-1].split(";")

		tax_payer_array.append(t)

with open(sys.argv[2] + "analysis.csv", "a") as f:
	f.write(analyse_nb_tax_payer() + ";" + analyse_birth_year() + ";" + analyse_disability_rate() + ";" + analyse_disability_type() + ";" + analyse_is_resident() + ";" + analyse_tax_payer_nb_address() + ";" + analyse_tax_payer_address() + ";" + analyse_nb_child() + ";" + analyse_child_birth_year() + ";" + analyse_child_disability_rate() + ";" + analyse_child_disability_type() + ";" + analyse_child_nb_address() + ";" + analyse_child_address() + ";" + analyse_nb_pension() + ";" + analyse_nb_employment() + ";" + analyse_nb_other() + ";" + analyse_pension_is_local() + ";" + analyse_employment_is_local() + ";" + analyse_other_is_local() + ";" + analyse_nb_income() + ";" + analyse_lu_address() + ";" + analyse_c4() + "\n")
