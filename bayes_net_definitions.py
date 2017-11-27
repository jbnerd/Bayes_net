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


class BayesNet(object):

	def __init__(self, nodes_spec=[]):
		""" nodes_spec is list of dictionaries for all the values."""
		self.nodes = []
		self.variables = []
		for node_dict in nodes_spec:
			self.add(node_dict)

	def add(self, node_dict):
		node = Node(nodes_dict)
		self.nodes.append(node)
		self.variables.append(node.var)
		for parent in node.parents:
			self.variable_node(parent).children.append(node)

	def variable_node(self, var):
		return [n for n in self.nodes if n.var == var][0]
		raise Exception("no such variable {}".format(var))