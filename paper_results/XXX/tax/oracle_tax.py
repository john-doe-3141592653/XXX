import sys

nb_tax_payer_check = False
birth_year_check = False
disability_rate_check = False
disability_type_check = False
is_resident_check = False
nb_address_check = False
address_check = False
nb_child_check = False
nb_income_check = False
is_local_check = False

c2_check = False
c2a_check = False
c3_check = False
c4_check = False

def compile_checkers_result():
	res = nb_tax_payer_check
	res = res or birth_year_check
	res = res or disability_rate_check
	res = res or disability_type_check
	res = res or is_resident_check
	res = res or nb_address_check
	res = res or address_check
	res = res or nb_child_check
	res = res or nb_income_check
	res = res or is_local_check

	res = res or c2_check
	res = res or c2a_check
	res = res or c3_check
	res = res or c4_check
	return res

def print_checkers_result():
	print("nb_tax_payer_check:         ", nb_tax_payer_check)
	print("birth_year_check:           ", birth_year_check)
	print("disability_rate_check:      ", disability_rate_check)
	print("disability_type_check:      ", disability_type_check)
	print("is_resident_check:          ", is_resident_check)
	print("nb_address_check:           ", nb_address_check)
	print("address_check:              ", address_check)
	print("nb_child_check:             ", nb_child_check)
	print("nb_income_check:            ", nb_income_check)
	print("is_local_check:             ", is_local_check)

	print("c2_check:                   ", c2_check)
	print("c2a_check:                  ", c2a_check)
	print("c3_check:                   ", c3_check)
	print("c4_check:                   ", c4_check)

def check_param(param, a, b):
	if not a <= float(param) <= b:
		return True
	return False

def check_bool(param):
	if not param in ["True", "False"]:
		return True
	return False

def check_c2(dt, dr):
	if dt == "None":
		if dr != 0:
			return False
	if dr == 0:
		if dt != "None":
			return False
	return True

def check_c2a(t):
	for c in t.children:
		if not check_c2(c.disability_type, c.disability_rate):
			return False
	return True

def check_c3(t):
	lu = False
	for a in t.address:
		if a == "LU":
			lu = True
	return not(lu) or t.is_resident

def check_c4(t):
	income_is_local = False
	address_lu = False
	
	income = []
	for i in t.income_pension:
		income.append(i)
	for i in t.income_employment:
		income.append(i)
	for i in t.income_other:
		income.append(i)
	for i in income:
		if income == "True":
			income_is_local = True

	for a in t.address:
		if a == "LU":
			address_lu = True

	if not (income_is_local and not(address_lu) and t.is_resident):
		return True
	return False

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


tax_payer_array = []

with open(sys.argv[1] + "tax.csv", "r") as f:
	for i in range(int(f.readline()[:-1])):
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

if check_param(len(tax_payer_array), 1, 100):
	nb_tax_payer_check = True
for t in tax_payer_array:
	if check_param(t.birth_year, 1920, 2020):
		birth_year_check = True
	if check_param(t.disability_rate, 0, 1):
		disability_rate_check = True
	if not t.disability_type in ["None", "Vision", "A"]:
		disability_type_check = True
	if check_bool(t.is_resident):
		is_resident_check = True
	if check_param(len(t.address), 1, 3):
		nb_address_check = True
	for a in t.address:
		if not a in ["LU", "FR", "BE", "DE", "OTHER"]:
			address_check = True
	if check_param(len(t.children), 0, 3):
		nb_child_check = True
	for c in t.children:
		if check_param(c.birth_year, 1920, 2020):
			birth_year_check = True
		if check_param(c.disability_rate, 0, 1):
			disability_rate_check = True
		if not c.disability_type in ["None", "Vision", "A"]:
			disability_type_check = True
		if check_param(len(c.address), 1, 3):
			nb_address_check = True
		for a in c.address:
			if not a in ["LU", "FR", "BE", "DE", "OTHER"]:
				address_check = True
	if check_param(len(t.income_pension) + len(t.income_employment) + len(t.income_other), 0, 3):
		nb_income_check = True
	for i in t.income_pension:
		if check_bool(i):
			is_local_check = True
	for i in t.income_employment:
		if check_bool(i):
			is_local_check = True
	for i in t.income_other:
		if check_bool(i):
			is_local_check = True

	if not check_c2(t.disability_type, t.disability_rate):
		c2_check = True
	if not check_c2a(t):
		c2a_check = True
	if not check_c3(t):
		c3_check = True
	if not check_c4(t):
		c4_check = True

#print_checkers_result()
with open(sys.argv[2] + "oracle", "a") as f:
	f.write(str(compile_checkers_result()) + "\n")

