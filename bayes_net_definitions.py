from read_file import read_file
import random

def probability(p):
	"""	returns True with probability p."""
	return p > random.uniform(0.0, 1.0)

class Node(object):
	"""docstring for Node"""
	def __init__(self, node_dict):
		self.var = node_dict['var']
		self.parents = node_dict['parents']
		self.cpt = node_dict['cpt']
		self.children = []

	def conditional_prob(self, value, events):
		prob_true = self.cpt[tuple([events[var] for var in self.parents])]
		return prob_true if value else 1 - prob_true

	def sample(self, events):
		return probability(self.conditional_prob(True, events))

	def __str__(self):
		return str(self.var) + " : " + str(self.parents)

	def __eq__(self, other):
		return self.var == other.var

	def __neq__(self, other):
		return not self.__eq__(self, other)

	def __repr__(self):
		return str(self.var) + " : " + str(self.parents)

class BayesNet(object):

	def __init__(self, list_nodes=[]):
		""" list_nodes is list of dictionaries for all the values."""
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
		raise Exception("no such variable {}".format(var))

	def markov_blanket(self, node):
		node = self.variable_node(node)
		blanket = [node]
		parents = node.parents
		parents = [self.variable_node(parent) for parent in parents]
		blanket = blanket + parents
		children = [item for item in self.nodes if node.var in item.parents]
		blanket = blanket + children
		spouse = [self.variable_node(parent) for item in children for parent in item.parents]
		blanket = blanket + spouse
		blanket = list(set(blanket))
		return blanket

class Expr(object):
	"""docstring for Expr"""
	def __init__(self, query_vars, cond_vars):
		self.query_vars = query_vars.split()
		self.cond_vars = cond_vars.split()
		self.query_vars = {item[-1]:True if item[0] != "~" else False for item in self.query_vars}
		self.cond_vars = {item[-1]:True if item[0] != "~" else False for item in self.cond_vars}

	def __str__(self):
		return "Query Variables : " + str(self.query_vars.keys()) + ", Condition Variables : " + str(self.cond_vars.keys())
		

def gibbs_ask(X, e, bn, N):
    """[Figure 14.16]
	N times simulation"""
    # assert X not in e, "Query variable must be distinct from evidence"
    counts = {x: 0 for x in [False, True]}  # bold N in [Figure 14.16]
    Z = [var for var in bn.variables if var not in e]
    state = dict(e)  # boldface x in [Figure 14.16]
    for Zi in Z:
        state[Zi] = random.choice([False, True])
    print(state)
    for j in range(N):
        for Zi in Z:
            state[Zi] = markov_blanket_sample(Zi, state, bn)
            counts[state[X]] += 1
    print(counts)
    # return ProbDist(X, counts)


def markov_blanket_sample(X, e, bn):
    Xnode = bn.variable_node(X)
    ei = e.copy()
    ei[X] = True
    child_probs = [Yj.conditional_prob(ei[Yj.var], ei)for Yj in Xnode.children]
    QT = Xnode.conditional_prob(True, e) * reduce(lambda x,y: x*y, child_probs, 1)
    ei[X] = False
    child_probs = [Yj.conditional_prob(ei[Yj.var], ei)for Yj in Xnode.children]
    QF = Xnode.conditional_prob(False, e) * reduce(lambda x,y: x*y, child_probs, 1)

    normalized = QT/(QT + QF)
    return probability(normalized)

def main():
    content = read_file()
    bn = BayesNet(content)
	# for node in bn.nodes:
	# 	print(node)
    X = 'G'
    e = {'O': True, 'A': True, 'X':True, 'N': True, 'H':True}
    # print(markov_blanket_sample(X, e, bn))
    gibbs_ask(X, e, bn, 100)
    # print(bn.markov_blanket('A'))
    test = Expr("~A B ~C", "D ~E F")
    print(test)

main()
