####################################################################################################
#            2015A7PS0116P
#            Abhishek V Joshi
####################################################################################################

from read_file import read_file
import random
import copy

def prob_true(p):
	# returns True with prob_true p
	return p > random.uniform(0.0, 1.0)

def mul(ls):
	prod = 1
	for item in ls:
		prod *= item
	return prod

class Node(object):

	def __init__(self, node_dict):
		self.var = node_dict['var']
		self.parents = node_dict['parents']
		self.cpt = node_dict['cpt']
		self.children = []

	def cond_prob(self, value, events):
		prob = self.cpt[tuple([events[var] for var in self.parents])]
		if value:
			return prob
		else:
			return (1 - prob)

	def sample(self, events):
		return prob_true(self.cond_prob(True, events))

	def __str__(self):
		return str(self.var) + " : " + str(self.parents)

	def __eq__(self, other):
		return self.var == other.var

	def __ne__(self, other):
		return not self.__eq__(self, other)

	def __repr__(self):
		return str(self.var) + " : " + str(self.parents)

	def __hash__(self):
		return hash(tuple([tuple(self.var), tuple(self.parents)]))

class BayesNet(object):

	def __init__(self, list_nodes=[]):
		self.nodes = []
		self.variables = []
		for node_dict in list_nodes:
			self.add(node_dict)

	def add(self, node_dict):
		node = Node(node_dict)
		self.nodes.append(node)
		self.variables.append(node.var)
		for parent in node.parents:
			self.variable_node(parent).children.append(node)

	def variable_node(self, var):
		return [n for n in self.nodes if n.var == var][0]

	def markov_blanket(bn, var):
		node = bn.variable_node(var)
		blanket = dict()
		blanket["node"] = node
		parents = node.parents
		parents = [bn.variable_node(parent) for parent in parents]
		blanket["parents"] = parents
		children = node.children
		blanket["children"] = children
		spouse = [bn.variable_node(parent) for item in children for parent in item.parents]
		blanket["spouse"] = list(set(spouse))
		return blanket

class Expr(object):

	def __init__(self, query_vars, cond_vars):
		self.query_vars = query_vars.split()
		self.cond_vars = cond_vars.split()
		self.query_vars = {item[-1]:True if item[0] != "~" else False for item in self.query_vars}
		self.cond_vars = {item[-1]:True if item[0] != "~" else False for item in self.cond_vars}

	def __str__(self):
		return "Query Variables : " + str(self.query_vars.keys()) + ", Condition Variables : " + str(self.cond_vars.keys())

def gibbs_ask(X, e, bn, N):
	probs = {False: 0, True: 0}
	Z = [var for var in bn.variables if var not in e]
	state = dict(e)
	for z in Z:
		state[z] = random.choice([False, True])
	for j in range(N):
		for z in Z:
			state[z] = markov_blanket_sample(z, state, bn)
			temp = state[X]
			probs[temp] += 1
	tot = probs[True] + probs[False]
	normalized = {True:float(probs[True])/tot, False:float(probs[False])/tot}
	return normalized

def markov_blanket_sample(X, e, bn):
	node = bn.variable_node(X)
	blanket = bn.markov_blanket(X)
	temp_e = copy.deepcopy(e)
	temp_e[X] = True
	child_probs = [Yj.cond_prob(temp_e[Yj.var], temp_e) for Yj in blanket['children']]
	true_prob = node.cond_prob(True, e) * mul(child_probs)
	temp_e[X] = False
	child_probs = [Yj.cond_prob(temp_e[Yj.var], temp_e) for Yj in blanket['children']]
	false_prob = node.cond_prob(False, e) * mul(child_probs)
	normalized = true_prob/(true_prob + false_prob)
	return prob_true(normalized)

def main():
	content = read_file()
	bn = BayesNet(content)
	# for node in bn.nodes:
	# 	print(node)
	# X = 'G'
	# e = {'O': True, 'A': True, 'X':True, 'N': True, 'H':True}
 #    # print(markov_blanket_sample(X, e, bn))
	# print(gibbs_ask(X, e, bn, 100))
	print(bn.markov_blanket('A'))
	# test = Expr("B", "L")
 #    # print(test)
	# prod = 1
	# for key, val in test.query_vars.items():
	# 	prod *= gibbs_ask(key, test.cond_vars, bn, 5000)[val]
	# print(prod)

if __name__ == "__main__":
	main()
