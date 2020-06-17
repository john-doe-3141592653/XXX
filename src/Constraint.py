'''
Copyright or © or Copr.

This software is a computer program whose purpose is to generate random
test case from a template file describing the data model.

This software is governed by the CeCILL-B license under French law and
abiding by the rules of distribution of free software.  You can  use,
modify and/ or redistribute the software under the terms of the CeCILL-B
license as circulated by CEA, CNRS and INRIA at the following URL
"http://www.cecill.info".

As a counterpart to the access to the source code and  rights to copy,
modify and redistribute granted by the license, users are provided only
with a limited warranty  and the software's author,  the holder of the
economic rights,  and the successive licensors  have only  limited
liability.

In this respect, the user's attention is drawn to the risks associated
with loading,  using,  modifying and/or developing or reproducing the
software by the user in light of its specific status of free software,
that may mean  that it is complicated to manipulate,  and  that  also
therefore means  that it is reserved for developers  and  experienced
professionals having in-depth computer knowledge. Users are therefore
encouraged to load and test the software's suitability as regards their
requirements in conditions enabling the security of their systems and/or
data to be ensured and,  more generally, to use and operate it in the
same conditions as regards security.

The fact that you are presently reading this means that you have had
knowledge of the CeCILL-B license and that you accept its terms.
'''

from Element import Element
import Miscellaneous as misc

###############################################################################
# --- Constraint ------------------------------------------------------------ #
###############################################################################
class Constraint(Element):
	"""
	A Constraint object ...
	"""
	def __init__(self, n, d, p, e, t, q=[], r=[]):
		"""
		:param n	: name
		:param d	: depth
		:param p	: parent
		:param e	: expression
		:param t	: type
		:param q	: quantifiers
		:param r	: ranges
		"""
		Element.__init__(self, n, d)

		self.__parent = p
		if t:
			self.__type = t[0]
		else:
			self.__type = "forall"
		self.__var_depth = -1

		self.__raw_expressions = e
		self.__expressions = []
		self.__raw_quantifiers = q
		self.__quantifiers = None
		self.__raw_ranges = r
		self.__ranges = []

		self.__variables = {}

	def build_constraint(self):
		depth_array = []

		for e in self.__raw_expressions:
			l = Lexer(e)
			token_array = l.get_token_array()

			for token in token_array:
				if token.type == "VARIABLE":
					depth_array.append(self.__get_variable_depth_array(token.value))

		self.__set_var_depth(depth_array)
		self.__check_depth(depth_array)

	def __set_var_depth(self, depth_array):
		for depth in depth_array:
			if depth and depth[-1] > self.__var_depth:
				self.__var_depth = depth[-1]

	def __preprocess_variable(self, var):
		nb_instances_flag = False
		if var[-13:] == ".nb_instances":
			nb_instances_flag = True
			var = var[:-13]
		elif var[-7:] == ".values":
			var = var[:-7]
		return var, nb_instances_flag

	def __check_depth(self, depth_array):
		for depth in depth_array:
			depth = depth[:-1]
			for d in depth:
				if d >= self.__var_depth:
					misc.error("Constraint::__check_variable_depth() -> constraint \"" + self._name + "\" is not consistant")
					raise ValueError
		depth_array = []
		for r in self.__raw_ranges:
			for i in range(2):
				l = Lexer(r[i])
				token_array = l.get_token_array()
				for token in token_array:
					if token.type == "VARIABLE":
						depth_array.append(self.__get_variable_depth_array(token.value))
		for depth in depth_array:
			for d in depth:
				if d >= self.__var_depth:
					misc.error("Constraint::__check_variable_depth() -> constraint \"" + self._name + "\" is not consistant")
					raise ValueError

	def __get_variable_depth_array(self, var):
		depth_array = []
		simplified_var = ""
		var, nb_instances_flag = self.__preprocess_variable(var)

		while "[" in var:
			index = var.find("[") + 1
			simplified_var += var[:index]
			var = var[index:]
			index, var = self.__extract_index(var)

			l = Lexer(index)
			token_array = l.get_token_array()
			for token in token_array:
				if token.type == "VARIABLE":
					depth_array += self.__get_variable_depth_array(token.value)
			simplified_var += "0"
		simplified_var += var

		elem = self.__parent.get_element_from_current_node(simplified_var)
		if elem is not None:
			depth_array.append(elem.depth - int(nb_instances_flag))
		return depth_array

	def __build_ranges(self):
		for r in self.__raw_ranges:
			tmp = []
			for i in range(2):
				l = Lexer(r[i])
				ta = l.get_token_array()
				self.__preprocess_token_array(ta)
				str_value = self.__build_token_array(ta)
				if str_value is None:
					return False
				else:
					tmp.append(eval(str_value))
			self.__ranges.append(tmp)
		return True

	def process(self):
		if self.__raw_quantifiers:
			if self.__build_ranges():
				self.__quantifiers = Quantifier(self.__raw_quantifiers, self.__ranges)
			else:
				return False

			while True:
				#print("current quantifier(s):")
				#print(self.__quantifiers.get_current_values())
				self.__build_expressions()
				if not self.__quantifiers.next_combination():
					break
		else:
			self.__build_expressions()

	def __build_expressions(self):
		for e in self.__raw_expressions:
			l = Lexer(e)
			token_array = l.get_token_array()
			self.__preprocess_token_array(token_array)

			expr = self.__build_token_array(token_array)
			if expr is not None:
				s, v = self.__build_string_parameter_expression(token_array)
				for i in range(len(s)):
					expr = expr.replace(s[i], v[i])
				self.__expressions.append(expr)


	def __build_string_parameter_expression(self, token_array):
		str_array = []
		val_array = []
		for i, token in enumerate(token_array):
			if token.type == "STRING":
				tp = ""
				var, nb_instances_flag = self.__preprocess_variable(token_array[i-2].value)

				while "[" in var:
					index = var.find("[") + 1
					tp += var[:index]
					var = var[index:]
					index, var = self.__extract_index(var)

					l = Lexer(index)
					token_array = l.get_token_array()
					self.__preprocess_token_array(token_array)
					index = self.__build_token_array(token_array)
					tp += str(eval(index))
				tp += var

				index = 0
				if tp[-1] == "]":
					i = tp.rfind("[")
					index = int(tp[i + 1:-1])
					tp = tp[:i]

				string_parameter = self.__parent.get_element_from_current_node(tp)
				values_array = string_parameter.values_array
				if token.value not in values_array:
					misc.error("Constraint::__build_string_parameter_expression() -> undefined string \"" + token.value + "\"")
				str_array.append(token.value)
				val_array.append(str(values_array.index(token.value)))
		return str_array, val_array

	def __preprocess_token_array(self, token_array):
		for token in token_array:
			if token.type == "COMPARISON_OPERATOR":
				token.value = self.__get_comparison_operator_eq(token.value)
			elif token.type == "QUANTIFIER":
				if not token.value in self.__raw_quantifiers:
					misc.error("Constraint::__preprocess_token_array() -> undefined quantifer \"" + token.value + "\"")
					raise ValueError

	def __build_token_array(self, token_array):
		expr = ""
		for token in token_array:
			if token.type == "VARIABLE":
				var = self.__evaluate_variable(token.value)
				if var is None:
					return None
				else:
					expr += var + " "
			elif token.type == "QUANTIFIER":
				expr += str(self.__quantifiers.get_current_values()[token.value]) + " "
			elif token.type != "EOF":
				expr += token.value + " "
		return misc.remove_starting_and_ending_space(expr)

	def __evaluate_variable(self, var):
		tp = ""
		var, nb_instances_flag = self.__preprocess_variable(var)

		while "[" in var:
			index = var.find("[") + 1
			tp += var[:index]
			var = var[index:]
			index, var = self.__extract_index(var)

			l = Lexer(index)
			token_array = l.get_token_array()
			self.__preprocess_token_array(token_array)
			index = self.__build_token_array(token_array)
			tp += str(eval(index))
		tp += var

		index = 0
		if tp[-1] == "]":
			i = tp.rfind("[")
			index = int(tp[i + 1:-1])
			tp = tp[:i]

		element = self.__parent.get_element_from_current_node(tp)
		if element is None:
			return None

		if nb_instances_flag:
			if element.depth - 1 < self.__var_depth or element.nb_instances_lock:
				return str(element.nb_instances)
			else:
				if element.get_type() == "node":
					var_id = "_" + element.name + element.get_nb_instances_parameter().identifier[4:]
				else: #element.get_type() == "parameter"
					var_id = "_" + element.identifier
				self.__variables[var_id] = element
				return var_id
		else:
			if element.depth < self.__var_depth or element.locks[index]:
				if element.get_type() == "string":
					return str(element.get_values_array().index(element.values[index]))
				else:
					return str(element.values[index])
			else:
				var_id = element.identifier + "_" + str(index)
				self.__variables[var_id] = element
				return var_id

	def __extract_index(self, v):
		i = 0
		brackets_counter = 0

		for char in v:
			if char == "[":
				brackets_counter += 1
			if char == "]":
				if brackets_counter != 0:
					brackets_counter -= 1
				else:
					break
			i += 1
		return v[:i], v[i:]

	def __get_comparison_operator_eq(self, op):
		if op == "SUP":
			return ">"
		elif op == "SUPEQ":
			return ">="
		elif op == "INF":
			return "<"
		elif op == "INFEQ":
			return "<="
		elif op == "EQ":
			return "=="
		elif op == "DIF":
			return "!="
		else:
			misc.error("error")
			raise ValueError

	def duplicate(self):
		c = Constraint(self._name, self._depth, self.__parent, self.__raw_expressions, self.__type, self.__raw_quantifiers, self.__raw_ranges)
		return c

	def set_parent(self, p):
		self.__parent = p

	def get_type(self):
		return self.__type

	def get_var_depth(self):
		return self.__var_depth
	var_depth = property(get_var_depth)

	def get_variables(self):
		return self.__variables
	variables = property(get_variables)

	def get_expressions(self):
		return self.__expressions
	expressions = property(get_expressions)

	def __repr__(self):
		return misc.color("--- Constraint \"" + self._name + "\" ---", "yellow") +\
				" (parent: " + self.__parent.name + " / depth: " + str(self._depth) + " / var_depth: " + str(self.__var_depth) + ")" +\
				"\nexpression: " + str(self.__raw_expressions) +\
				"\nquantifiers: " + str(self.__raw_quantifiers) +\
				"\nranges: " + str(self.__raw_ranges)

###############################################################################
# --- Quantifier ------------------------------------------------------------ #
###############################################################################
class Quantifier():
	def __init__(self, n, r):
		self.__names = n
		self.__ranges = r
		self.__current_values = []

		for r in self.__ranges:
			self.__current_values.append(r[0])

	def reset_i(self, i):
		self.__current_values[i] = self.__ranges[i][0]

	def reset_all(self):
		for i in range(len(self.__names)):
			self.reset_i(i)

	def next_i(self, i):
		if self.__current_values[i] < self.__ranges[i][1]:
			self.__current_values[i] += 1
			return True
		else:
			self.reset_i(i)
			return False

	def next_combination(self, i=0):
		if i == len(self.__names):
			return False

		if self.next_i(i):
			return True
		else:
			return self.next_combination(i + 1)

	def get_current_values(self):
		q = {}
		for i in range(len(self.__names)):
			q[self.__names[i]] = self.__current_values[i]
		return q
	values = property(get_current_values)


###############################################################################
# --- Token ----------------------------------------------------------------- #
###############################################################################
class Token:
	def __init__(self, t, v):
		self.type = t
		self.value = v


###############################################################################
# --- Lexer ----------------------------------------------------------------- #
###############################################################################
class Lexer():
	def __init__(self, t):
		self.__text = t
		self.__pos = 0
		self.__current_char = self.__text[self.__pos]

		self.__token_array = []

		self.__basic_check()
		self.__set_token_array()

	def __basic_check(self):
		self.__check_brakets("(", ")")
		self.__check_brakets("[", "]")

	def __check_brakets(self, opening_bracket, closing_bracket):
		counter = self.__text.count(opening_bracket)
		if counter != self.__text.count(closing_bracket):
			misc.error("Lexer::__basic_checks -> The bracket structure is not coherent")
			raise NameError

	def __move_forward(self):
		self.__pos += 1
		if self.__pos > len(self.__text) - 1:
			self.__current_char = None
		else:
			self.__current_char = self.__text[self.__pos]

	def __skip_space(self):
		while self.__current_char is not None and self.__current_char.isspace():
			self.__move_forward()

	def __extract_number(self):
		number = ""
		while self.__current_char is not None and self.__current_char.isdigit():
			number += self.__current_char
			self.__move_forward()
		if self.__current_char == ".":
			number += self.__current_char
			self.__move_forward()
		while self.__current_char is not None and self.__current_char.isdigit():
			number += self.__current_char
			self.__move_forward()
		return Token("NUMBER", number)

	def __extract_word(self):
		word = ""
		while self.__current_char is not None and self.__current_char.isalpha() or self.__current_char is "_":
			word += self.__current_char
			self.__move_forward()
		if self.__current_char is not None and (self.__current_char in [".", "\\", "["] or self.__current_char.isdigit()):
			return self.__extract_variable(word)
		else:
			if len(word) == 1:
				return Token("QUANTIFIER", word)
			elif word in ["OR", "AND", "NOT", "IMPLIES", "DISTINCT"]:
				return Token("BOOLEAN_OPERATOR", "z3." + word[0] + word[1:].lower())
			elif word in ["SUP", "SUPEQ", "INF", "INFEQ", "EQ", "DIF"]:
				return Token("COMPARISON_OPERATOR", word)
			elif word in ["True", "true"]:
				return Token("BOOLEAN_TRUE", "True")
			elif word in ["False", "false"]:
				return Token("BOOLEAN_FALSE", "False")
			else:
				return Token("STRING", word)

	def __extract_variable(self, w=""):
		variable = w
		while self.__current_char is not None and self.__current_char not in [" ", ")", "+", "-", "*", "/", "%", ","]:
			if self.__current_char == "[":
				self.__move_forward()
				variable += self.__extract_index()
			else:
				variable += self.__current_char
				self.__move_forward()
		return Token("VARIABLE", variable)

	def __extract_index(self):
		index = "["
		while self.__current_char != "]":
			if self.__current_char == "[":
				self.__move_forward()
				index += self.__extract_index()
			else:
				index += self.__current_char
				self.__move_forward()
		index += self.__current_char
		self.__move_forward()
		return index

	def __get_next_token(self):
		while self.__current_char is not None:
			if self.__current_char.isspace():
				self.__skip_space()

			if self.__current_char.isdigit():
				return self.__extract_number()
			elif self.__current_char.isalpha():
				return self.__extract_word()
			elif self.__current_char == ".":
				return self.__extract_variable()
			elif self.__current_char in ["+", "-", "*", "/", "%"]:
				operator = self.__current_char
				self.__move_forward()
				return Token("OPERATOR", operator)
			elif self.__current_char == "(":
				self.__move_forward()
				return Token("LPAR", "(")
			elif self.__current_char == ")":
				self.__move_forward()
				return Token("RPAR", ")")
			elif self.__current_char == ",":
				self.__move_forward()
				return Token("COMA", ",")
			else:
				misc.error("Lexer::__get_next_token() -> invalid character \"" + self.__current_char + "\"")
				raise NameError
		return Token("EOF", self.__current_char)

	def __set_token_array(self):
		self.__token_array.append(self.__get_next_token())
		while self.__token_array[-1].type != "EOF":
			self.__token_array.append(self.__get_next_token())

	def get_token_array(self):
		return self.__token_array
	token_array = property(get_token_array)

	def print_token_array(self):  # for debugging
		for token in self.__token_array:
			print (token.type + " -> " + str(token.value))

