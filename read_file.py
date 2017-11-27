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
        t_f_vals.append(list("".join(str((x >> i)&1)) for i in range(n-1, -1, -1)))
    t_f_vals = [tuple([True if v == '1' else False for v in item]) for item in t_f_vals]
    # print(t_f_vals)
    return t_f_vals

def pack_in_dict(prob):	
    cause_list = prob[1]
    cause_list = cause_list.replace("[", "")
    cause_list = cause_list.replace("]", "")
    cause_list = cause_list.replace(",", "")
    cause_list = cause_list.split()

    cpt = prob[2].replace(",", "")
    cpt = cpt.split()
    cpt = [float(item) for item in cpt]
    t_f_vals = t_f(len(cause_list))
    ret = dict()
    cpt = {torf:likeliness for torf,likeliness in zip(t_f_vals, cpt)}
    if len(cause_list) == 0:
        for key, val in cpt.items():
            if key == ():
                cpt = val
        # cause_list = " ".join(cause_list)
        ret['cpt'] = cpt
    elif len(cause_list) == 1:
        cpt_temp = {}
        for key, val in cpt.items():
            if key == (False,):
                cpt_temp[False] = val
            elif key == (True,):
                cpt_temp[True] = val
        # cause_list = " ".join(cause_list)
        ret['cpt'] = cpt_temp
    else:
        # cause_list = " ".join(cause_list)
        ret['cpt'] = cpt
    ret['var'] = prob[0]
    ret['parents'] = cause_list
    return ret

def read_file():
    content = read("input.txt")
    content = [pack_in_dict(item) for item in content]
    return content

if __name__ == '__main__':
	read_file()