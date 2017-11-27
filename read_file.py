def read(filename):
	with open(filename) as fp:
		content = fp.readlines()
	content = [item.replace("\n", "") for item in content]
	content = [item.split(">>") for item in content]
	content = [[x.strip() for x in item] for item in content]
	del content[-1]
	# print(content)
	return content

def t_f(n):
    num_states = 2**n
    t_f_vals = []
    for x in range(num_states):
        t_f_vals.append(list("".join(str((x >> i)&1)) for i in xrange(n-1, -1, -1)))
    t_f_vals = [tuple([True if v=='1' else False for v in item]) for item in t_f_vals]
    print(t_f_vals)

def pack_in_dict(prob):	
	cause_list = prob[1]
	cause_list = cause_list.replace("[", "")
	cause_list = cause_list.replace("]", "")
	cause_list = cause_list.replace(",", "")
	cause_list = cause_list.split()

	cpt = prob[2].replace(",", "")
	cpt = cpt.split()
	cpt = [float(item) for item in cpt]
    
	ret = {
		"var" : prob[0],
		"parents" : cause_list,
		"cpt" : cpt
	}
	return ret

def main():
	content = read("input.txt")
	content = [pack_in_dict(item) for item in content]
	print(content)

if __name__ == '__main__':
	main()