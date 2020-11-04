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

###############################################################################
# --- Xml module ------------------------------------------------------------ #
###############################################################################
import xml.etree.ElementTree as ET

import Miscellaneous as misc
from Node import Node
from Parameter import Boolean_Parameter, String_Parameter, Integer_Parameter, Real_Parameter
from Constraint import Constraint

def parse_xml(path):
	try:
		tree = ET.parse(path)
		return tree.getroot()
	except ET.ParseError:
		misc.error("Xml::parse_xml() -> the template \"" + path + "\" does not respect xml format")
		return None


def read_template(path):
	root_xml = parse_xml(path)
	if root_xml is None:
		raise ValueError

	if root_xml.tag != "root":
		misc.error("Xml::read_xml() -> the template root tag must be \"root\"" + path + "\"")
		raise ValueError

	name = check_attribute(root_xml, "name", True)
	nb_instances = Integer_Parameter(name + "_nb_instances", -1, 1, 1, "u", None, None, None, None, 1)
	nb_instances.set_value_i(0, 1)
	nb_instances.lock_i(0)
	root_node = Node(name, 0, None, None, nb_instances)
	read_node(root_xml, root_node)
	return root_node


def read_node(node_xml, node, d=0):
	for child in node_xml:
		name = check_attribute(child, "name", True)
		if child.tag == "parameter":
			node.add_parameter(build_parameter(name, d, child))
		elif child.tag == "constraint":
			node.add_constraint(build_constraint(name, d, node, child))
		elif child.tag == "node":
			node.add_child(build_node(name, d+1, node, child))
			read_node(child, node.get_child_n(name), d+1)
		else:
			misc.error("Xml::read_node() -> \"" + child.tag + "\" unknown xml tag")
			raise NameError


def build_node(n, d, p, node_xml):
	minimum = check_attribute(node_xml, "min")
	maximum = check_attribute(node_xml, "max")
	nb = check_attribute(node_xml, "nb_instances")

	if nb and check_nb_instances(nb):
		nb = int(nb)
		if minimum is not None or maximum is not None:
			misc.error("Xml::build_node() -> \"" + n + "\" min and max should not be specified along with nb_instances attribute")
			raise ValueError
		node_xml.attrib["min"] = nb
		node_xml.attrib["max"] = nb
		nb_instances = build_integer_parameter(n + "_nb_instances", d-1, node_xml, 1)
		nb_instances.set_value_i(0, nb)
		nb_instances.lock_i(0)

	elif minimum is not None or maximum is not None:
		if minimum is None and maximum is not None:
			misc.error("Xml::build_node() -> \"" + n + "\" missing min attribute")
			raise ValueError
		elif maximum is None and minimum is not None:
			misc.error("Xml::build_node() -> \"" + n + "\" missing max attribute")
			raise ValueError
		nb_instances = build_integer_parameter(n + "_nb_instances", d-1, node_xml, 1)
		if nb_instances.m < 0:
			misc.error("Xml::build_node() -> \"" + n + "\" min and max attributes must be positive integers")
			raise ValueError

	else: 	#not nb_instances and not minimum and not maximum
		node_xml.attrib["min"] = "1"
		node_xml.attrib["max"] = "1"
		nb_instances = build_integer_parameter(n + "_nb_instances", d-1, node_xml, 1)
		nb_instances.set_value_i(0, 1)
		nb_instances.lock_i(0)

	return Node(n, d, p, None, nb_instances)


def build_parameter(n, d, node_xml):
	parameter_type = check_attribute(node_xml, "type", True)
	nbi = check_attribute(node_xml, "nb_instances")
	to_lock = False
	if nbi and check_nb_instances(nbi):
		nbi = int(nbi)
		to_lock = True
	else:
		nbi = 1

	if parameter_type == "boolean":
		p = build_boolean_parameter(n, d, node_xml, nbi)
	elif parameter_type == "string":
		p = build_string_parameter(n, d, node_xml, nbi)
	elif parameter_type == "integer":
		p = build_integer_parameter(n, d, node_xml, nbi)
	elif parameter_type == "real":
		p = build_real_parameter(n, d, node_xml, nbi)
	else:
		misc.error("Xml::build_parameter() -> \"" + parameter_type + "\" unknown parameter type")
		raise NameError

	if to_lock:
		p.lock_nb_instances()
	return p


def build_categorical_parameter(node_xml):
	values = []
	tmp = check_attribute(node_xml, "values", False)
	if tmp:
		tmp = tmp.split(";")
		for v in tmp:
			values.append(misc.remove_starting_and_ending_space(v))
	else:
		values = [True, False]
	return values, build_weights(check_attribute(node_xml, "weights", False))


def build_weights(str_weights):
	weights = []
	if str_weights:
		str_weights = str_weights.split(";")
		for w in str_weights:
			w = misc.remove_starting_and_ending_space(w)
			if misc.check_integer(w, True):
				w = int(w)
				if w >= 0:
					weights.append(int(w))
				else:
					misc.error("Xml::build_weights() -> weight must be positive or null")
		if sum(weights) == 0:
			misc.error("Xml::build_weights() -> at least one weight must be positive")
			raise ValueError
	return weights


def build_boolean_parameter(n, d, node_xml, nbi):
	values, weights = build_categorical_parameter(node_xml)

	if len(values) != 2:
		misc.error("Xml::build_boolean_parameter() -> wrong boolean parameter values")
		raise ValueError
	for i in range(2):
		if values[i] in [True, "True", "true", 1]:
			values[i] = True
		elif values[i] in [False, "False", "false", "0"]:
			values[i] = False
		else:
			misc.error("Xml::build_boolean_parameter() -> wrong boolean parameter values")
			raise ValueError
	return Boolean_Parameter(n, d, values, weights, nbi)


def build_string_parameter(n, d, node_xml, nbi):
	values, weights = build_categorical_parameter(node_xml)
	return String_Parameter(n, d, values, weights, nbi)


def build_numerical_parameter(node_xml):
	minimum = check_attribute(node_xml, "min", True)
	maximum = check_attribute(node_xml, "max", True)

	distribution = check_attribute(node_xml, "distribution")
	mean = check_attribute(node_xml, "mean", False)
	variance = check_attribute(node_xml, "variance", False)
	ranges = []

	if not distribution:
		distribution = "u"
	if mean and misc.check_number(mean, True):
		mean = float(mean)
	else:
		mean = None
	if variance and misc.check_number(variance, True):
		variance = float(variance)
	else:
		variance = None
	if ranges:
		pass

	tmp = check_attribute(node_xml, "ranges", False)
	if tmp:
		tmp = tmp.split(";")
		for r in tmp:
			r = misc.remove_starting_and_ending_space(r)
			r = r[1:-1].split(",")
			if len(r) != 2:
				misc.error("Xml::build_numerical_parameter() -> invalid ranges")
				raise ValueError
			for i in range(2):
				r[i] = misc.remove_starting_and_ending_space(r[i])
			ranges.append((r[0], r[1]))

	return minimum, maximum, distribution, mean, variance, ranges, build_weights(check_attribute(node_xml, "weights", False))


def build_integer_parameter(n, d, node_xml, nbi):
	minimum, maximum, distribution, mean, variance, str_ranges, weights = build_numerical_parameter(node_xml)
	misc.check_integer(minimum, True)
	minimum = int(minimum)
	misc.check_integer(maximum, True)
	maximum = int(maximum)

	ranges = []
	for r in str_ranges:
		if misc.check_integer(r[0], True) and misc.check_integer(r[1], True):
			ranges.append((int(r[0]), int(r[1])))
	return Integer_Parameter(n, d, minimum, maximum, distribution, mean, variance, ranges, weights, nbi)


def build_real_parameter(n, d, node_xml, nbi):
	minimum, maximum, distribution, mean, variance, str_ranges, weights = build_numerical_parameter(node_xml)
	misc.check_number(minimum, True)
	minimum = float(minimum)
	misc.check_number(maximum, True)
	maximum = float(maximum)

	ranges = []
	for r in str_ranges:
		if misc.check_number(r[0], True) and misc.check_number(r[1], True):
			ranges.append((float(r[0]), float(r[1])))
	return Real_Parameter(n, d, minimum, maximum, distribution, mean, variance, ranges, weights, nbi)


def build_constraint(n, d, node, node_xml):
	expressions = []
	raw_expressions = check_attribute(node_xml, "expressions", True)
	raw_expressions = raw_expressions.split(";")
	for e in raw_expressions:
		expressions.append(misc.remove_starting_and_ending_space(e))

	types = []
	raw_constraint_types = check_attribute(node_xml, "types", False)
	if raw_constraint_types is not None:
		raw_constraint_types = raw_constraint_types.split(";")
		for c in raw_constraint_types:
			c = misc.remove_starting_and_ending_space(c)
			if c in ["forall", "exist", "unique"]:
				types.append(c)
			else:
				misc.error("Xml::__build_constraint() -> unknown constraint type \"" + c + "\"")
				raise NameError

	quantifiers = []
	raw_quantifiers = check_attribute(node_xml, "quantifiers", False)
	if raw_quantifiers is not None:
		raw_quantifiers = raw_quantifiers.split(";")
		for l in raw_quantifiers:
			l = misc.remove_starting_and_ending_space(l)
			if misc.check_letter(l, True):
				quantifiers.append(l)

	ranges = []
	raw_ranges = check_attribute(node_xml, "ranges", False)
	if raw_ranges is not None:
		raw_ranges = raw_ranges.split(";")
		for r in raw_ranges:
			r = misc.remove_starting_and_ending_space(r)
			if r == "all":
				ranges.append(r)
			elif r[0] is "[" and r[-1] is "]":
				boundaries = r[1:-1].split(",")
				if len(boundaries) != 2:
					misc.error("Xml::build_constraint() -> wrong ranges syntax")
					raise ValueError
				ranges.append((misc.remove_starting_and_ending_space(boundaries[0]), misc.remove_starting_and_ending_space(boundaries[1])))
			else:
				misc.error("Xml::build_constraint() -> wrong ranges syntax")
				raise ValueError

	if len(quantifiers) != len(ranges) or len(quantifiers) != len(types):
		misc.error("Xml::build_constraint() -> the number of quantifiers must equal the number of ranges and types")
		raise ValueError

	return Constraint(n, d, node, expressions, types, quantifiers, ranges)


def check_nb_instances(nb):
	misc.check_integer(nb, True)
	if int(nb) >= 0:
		return True
	else:
		misc.error("Xml::check_nb_instances() -> nb_instances must be a positive integer value")
		raise ValueError


def check_attribute(node_xml, att, err=False):
	if att in node_xml.attrib:
		return node_xml.attrib[att]
	else:
		if err:
			misc.error("Xml::check_attribute() -> \"" + att + "\" attribute is missing")
			raise NameError
		else:
			return None


def write_test_case(root_node, seed, path):
	with open(path, "w") as f:
		f.write("<?xml version=\"1.0\"?>\n\n")
		f.write(write_root_node(root_node, seed))


def write_root_node(root_node, seed):
	s = "<root name=\"" + root_node.name + "\">\n"
	s +="\t<seed value =\"" + seed + "\"/>\n"
	current_container = root_node.get_container_i(0)
	s += write_data(current_container)
	s += "</root>"
	return s


def write_node(node, tab):
	s = ""
	for i in range(node.nb_instances):
		s += tab + "<node name=\"" + node.name + "\" instance=\"" + str(i) + "/" + str(node.nb_instances - 1) + "\">\n"
		current_container = node.get_container_i(i)
		s += write_data(current_container, tab)
		s += tab + "</node>\n"
	return s


def write_data(current_container, tab=""):
	s = ""
	for p in current_container.parameters:
		tmp_param = current_container.get_parameter_n(p)
		values = ""
		for i in range(tmp_param.nb_instances):
			values += str(tmp_param.values[i]) + ";"
		values = values[:-1]

		s += tab + "\t<parameter name=\"" + p + "\" values=\"" + values + "\"/>\n"
	for c in current_container.children:
		s += write_node(current_container.get_child_n(c), tab + "\t")
	return s


def read_test_case(path, root_node):
	root_xml = parse_xml(path)
	seed = "r"

	if root_node.name == root_xml.attrib["name"]:
		if root_xml[0].tag == "seed":
			if root_xml[0].attrib["value"]:
				seed = root_xml[0].attrib["value"]
				root_xml.remove(root_xml[0])
			else:
				misc.error("Xml::read_template() -> seed value is missing")
				raise ValueError
	else:
		misc.error("Xml::read_genotype() -> node name does not match")
		raise ValueError

	set_element(root_xml, root_node)
	return seed


def set_element(node_xml, node, i=0):
	for child in node_xml:
		name = check_attribute(child, "name", True)
		if child.tag == "parameter":
			set_parameter(name, child, node, i)
		elif child.tag == "node":
			set_node(name, child, node, i)
		else:
			misc.error("Xml::set_element() -> unknown xml tag\"" + child.tag + "\"")
			raise NameError


def set_parameter(name, node_xml, node, i):
	if name in node.parameters:
		param = node.get_parameter_n(name, i)
		values = check_attribute(node_xml, "values", True).split(";")
		length = len(values)

		param.change_nb_instances(length)
		for i in range(length):
			if not values[i] in ["r", ""]:
				param.set_value_i(i, misc.remove_starting_and_ending_space(values[i]))
				param.lock_i(i)
	else:
		misc.error("Xml::set_parameter() -> parameter name \"" + name + "\" does not match")
		raise NameError


def set_node(name, node_xml, node, i):
	if name in node.children:
		elem = node.get_child_n(name, i)

		raw_identifier = check_attribute(node_xml, "instance")
		if raw_identifier is None:
			raw_identifier = "0"

		identifier = raw_identifier.split("/")[0]
		if misc.check_integer(identifier, True):
			identifier = int(identifier)
		if "/" in raw_identifier:
			max_identifier = raw_identifier.split("/")[1]
			if misc.check_integer(max_identifier, True):
				max_identifier = int(max_identifier)
				if not elem.nb_instances_lock:
					elem.change_nb_instances(max_identifier + 1)
					elem.lock_nb_instances()
		if elem.nb_instances is None or identifier + 1 > elem.nb_instances:
			elem.change_nb_instances(identifier + 1)
			set_element(node_xml, elem, identifier)
			if not elem.nb_instances_lock:
				elem.reduce_nb_instances_interval(identifier)
		else:
			set_element(node_xml, elem, identifier)

