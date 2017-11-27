from read_file import read_file

def probability(p):
	"""	returns True with probability p."""
	return p > random.uniform(0.0, 1.0)

class ProbDist(object):
    def __init__(self, var = "UNK", freqs = None):
        self.var = var
        self.prob = freqs

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

def main():
    content = read_file()
    bn = BayesNet(content)

main()
