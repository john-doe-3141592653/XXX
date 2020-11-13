from Element import Element
from Lexer import Expr_lexer, Tree_path_lexer

class Constraint(Element):
	def __init__(self, n, d, p, e, t=[], q=[], r=[]):
		"""
		:param n		: name
		:param d		: depth
		:param p		: parent
		:param e		: expressions
		:param t		: types
		:param q		: quantifiers
		:param r		: ranges
		"""
		Element.__init__(self, n, d)
		
		self.__parent = p
		self.__var_depth = -1

		self.__basic_checks(e)
		self.__raw_expressions = e
		self.__quantifiers = []
		for i, n in enumerate(q):
			self.__quantifiers.append(Quantifier(n, r[i][0], r[i][1], t[i]))

		self.__expressions = []
		self.__variables = {}

	def __basic_checks(self, expr_array):
		for expr in expr_array:
			self.__check_brackets(expr, "(", ")")
			self.__check_brackets(expr, "{", "}")
			self.__check_brackets(expr, "[", "]")
	
	def __check_brackets(self, expr, opening_bracket, closing_bracket):
		counter = expr.count(opening_bracket)
		if expr.count(closing_bracket) != counter:
			print("Constraint::__check_brackets -> The bracket structure is not coherent")
			raise NameError

	def build_constraint(self):
		depth_array = []
		for e in self.__raw_expressions:
			l = Expr_lexer(e)
			token_array = l.get_token_array()
			for token in token_array:
				if token.type == "TREE_PATH":
					depth_array.append(self.__get_tree_path_depth_array(token.value))
		self.__check_depth(depth_array)
		self.__set_var_depth(depth_array)

	def __get_tree_path_depth_array(self, tp):
		depth_array = []
		simplified_tree_path = ""
		nb_instances_flag = False

		tp_l = Tree_path_lexer(tp)
		tp_token_array = tp_l.get_token_array()
		for tp_token in tp_token_array[:-1]:
			if tp_token.type == "INDEX":
				e_l = Expr_lexer(tp_token.value[1:-1])
				e_token_array = e_l.get_token_array()
				for e_token in e_token_array:
					if e_token.type == "TREE_PATH":
						depth_array += self.__get_tree_path_depth_array(e_token.value)
				simplified_tree_path += "[0]"
			elif tp_token.type == "NB_INSTANCES":
				nb_instances_flag = True
			else:
				simplified_tree_path += tp_token.value

		elem = self.__parent.get_element_from_current_node(simplified_tree_path)
		if elem is not None:
			depth_array.append(elem.depth - int(nb_instances_flag))
		return depth_array
			
	def __set_var_depth(self, depth_array):
		for depth in depth_array:
			if depth and depth[-1] > self.__var_depth:
				self.__var_depth = depth[-1]
	
	def __check_depth(self, depth_array):
		pass

	def process(self):
		for e in self.__raw_expressions:
			expr = ""			
			if len(self.__quantifiers) == 0:
				expr = e
			else:	
				expr = self.__process_quantified_expr(self.__quantifiers, e)
			self.__expressions.append(self.__build_z3_query(expr))

	def __process_quantified_expr(self, q_list, expr):
		new_expr = ""
		sub_expr = ""
		
		q_first = q_list[0]
		q_tail = q_list[1:]

		m = int(self.__evaluate_expr(q_first.m))
		M = int(self.__evaluate_expr(q_first.M))

		if m > M:
			if q_first == "forall":
				return "True"
			else: #exist
				return "False"
		elif m == M:
			multiple = False
		else: #m < M
			multiple = True
			if q_first.type == "forall":
				new_expr = "z3.And("
			elif q_first.type == "exist":
				new_expr = "z3.Or("
			else: #UNIQUE
				print("Constraint::__process_quantified_expr -> UNIQUE feature is not available yet")
				raise NameError

		for q in range(m, M+1):
			sub_expr = self.__substitute(expr, q_first.name, str(q))
			if len(q_tail) > 0:
				updated_q_tail = self.__update_q_range(q_tail, q_first.name, str(q))
				sub_expr = self.__process_quantified_expr(updated_q_tail, sub_expr)	
			if multiple and q < M:
				new_expr += sub_expr + ", "
			elif multiple and q == M:
				new_expr += sub_expr + ")"
			elif not multiple:
				new_expr = sub_expr
		return new_expr

	def __substitute(self, expr, q_name, val):
		new_expr = ""		
		l = Expr_lexer(expr)
		token_array = l.get_token_array()
		for token in token_array[:-1]:
			if token.type == "QUANTIFIER" and token.value == q_name:
				new_expr += val + " "
			elif token.type == "TREE_PATH":
				new_expr += self.__substitute_tree_path_index(token.value, q_name, val) + " "
			else:
				new_expr += token.value + " "
		return new_expr[:-1]

	def __substitute_tree_path_index(self, tree_path, q_name, val):
		new_tree_path = ""
		l = Tree_path_lexer(tree_path)
		token_array = l.get_token_array()
		for token in token_array[:-1]:
			if token.type == "INDEX":
				new_tree_path += "[" + self.__substitute(token.value[1:-1], q_name, val) + "]"
			elif token.type == "NB_INSTANCES":
				new_tree_path += ".nb_instances"
			else:
				new_tree_path += token.value
		return new_tree_path

	def __update_q_range(self, q_list, q_name, val):
		new_q_list = []
		for q in q_list:
			new_q_list.append(Quantifier(q.name, self.__substitute(q.m, q_name, val), self.__substitute(q.M, q_name, val), q.type))
		return new_q_list
	
	def __evaluate_expr(self, expr):
		new_expr = ""
	
		l = Expr_lexer(expr)
		token_array = l.get_token_array()
		for token in token_array[:-1]:
			if token.type == "TREE_PATH":
				new_expr += self.__evaluate_tree_path(token.value)
			else:
				new_expr += token.value
		return str(eval(new_expr))

	def __evaluate_tree_path(self, tp):
		new_tree_path = ""
		nb_instances_flag = False
		
		l = Tree_path_lexer(tp)
		token_array = l.get_token_array()
		
		for token in token_array[:-1]:
			if token.type == "INDEX":
				new_tree_path += "[" + self.__evaluate_expr(token.value[1:-1]) + "]"
			elif token.type == "NB_INSTANCES":
				nb_instances_flag = True
			else:
				new_tree_path += token.value
		
		index = 0
		if new_tree_path[-1] == "]":
			i = new_tree_path.rfind("[")
			index = int(new_tree_path[i + 1:-1])
			new_tree_path = new_tree_path[:i]
			
		element = self.__parent.get_element_from_current_node(new_tree_path)
		if element is None:
			if nb_instances_flag:
				return "0"
			else:
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

	def __build_z3_query(self, expr):
		new_expr = ""
		l = Expr_lexer(expr)
		token_array = l.get_token_array()

		for token in token_array[:-1]:
			if token.type == "TREE_PATH":
				new_expr += self.__evaluate_tree_path(token.value) + " "
			elif token.type == "COMPARISON_OPERATOR":
				new_expr += self.__get_comparison_operator_eq(token.value) + " "
			else:
				new_expr += token.value + " "
		return new_expr


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
		else: #op == DIF
			return "!="			

	def duplicate(self):
		ta = []
		qa = []
		ra = []
		for q in self.__quantifiers:
			ta.append(q.type)
			qa.append(q.name)
			ra.append((q.m, q.M))					
		return Constraint(None, None, None, self.__raw_expressions, ta, qa, ra)

	def set_parent(self, p):
		self.__parent = p

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
		str_q = ""
		str_e = ""
		for i, q in enumerate(self.__quantifiers):
			str_q += " - q" + str(i) + ": " + q.type + " " + q.name + " in [" + q.m + ", " + q.M + "]" + "\n"
		str_q = str_q[:-1]
		for i, e in enumerate(self.__raw_expressions):
			str_e += " - e" + str(i) + ": " + e + "\n"
		str_e = str_e[:-1]

		return "--- Constraint ---\n" +\
			   "expression(s): " + "\n" + str_e + "\n" +\
			   "quantifier(s): " + "\n" + str_q + "\n"

class Quantifier:
	def __init__(self, n, m, M, t):
		self.name = n
		self.m = m
		self.M = M
		self.type = t

	def duplicate(self):
		return Quantifer(self.name, self.m, self.M, self.type)

	def __repr__(self):
		return "--- Quantifier ---\n" +\
			   "  name : " + self.name + "\n" +\
			   "  min  : " + self.m + "\n" +\
			   "  max  : " + self.M + "\n" +\
			   "  type : " + self.type + "\n"
