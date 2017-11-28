####################################################################################################
#            2015A7PS0116P
#            Abhishek V Joshi
####################################################################################################

from Tkinter import *
import ttk
from read_file import *
from bayes_net_definitions import *
import copy

content = read_file()
bn = BayesNet(content)

variables = copy.deepcopy(bn.variables)

def display_result():
    values = [[item.get() for item in i] for i in var]
    query_pos = [variables[iterator] for iterator,value in enumerate(values[0]) if value > 0]
    query_neg = ['~' + variables[iterator] for iterator,value in enumerate(values[1]) if value > 0]
    queries = query_pos + query_neg
    evi_pos = [variables[iterator] for iterator,value in enumerate(values[2]) if value > 0]
    evi_neg = ['~' + variables[iterator] for iterator,value in enumerate(values[3]) if value > 0]
    evidences = evi_pos + evi_neg
    query = " ".join(queries)
    evidence = " ".join(evidences)
    
    try:
        error_checking(queries, evidences)
    except:
        v.set('Wrong input, see the rules')
    else:
        total = Expr(query, evidence)
        ls = [gibbs_ask(key, total.cond_vars, bn, 5000)[val] for key, val in total.query_vars.items()]
        prod = mul(ls)
        v.set(prod)

def error_checking(query, evidence):
    assert set(query).intersection(set(evidence)) == set([])
    assert len(query) <= 10
    assert len(evidence) <= 10
    assert len(query) > 0
    for x in query:
        assert not '~'+ x in query
    for y in evidence:
        assert not '~'+ y in evidence


root = Tk()
root.title("Bayesian Belief Network")

Label(root, text = "Query Variables").grid(row = 5, column = 125, sticky = E, pady = 20)
Label(root, text = "Condition Variables").grid(row = 5, column = 425, sticky = E, pady = 20)

var = [[IntVar() for _ in range(len(variables))] for _ in range(4)]

for i, val in enumerate(variables):
    Checkbutton(root, text = str(val), variable=var[0][i]).grid(row = 50 + 5 * i, column = 100, sticky = E, padx = 25, pady = 10)
    Checkbutton(root, text = "~" + str(val), variable=var[1][i]).grid(row = 50 + 5 * i, column = 150, sticky = E, padx = 25, pady = 10)
    Checkbutton(root, text = str(val), variable=var[2][i]).grid(row = 50 + 5 * i, column = 400, sticky = E, padx = 25, pady = 10)
    Checkbutton(root, text = "~" + str(val), variable=var[3][i]).grid(row = 50 + 5 * i, column = 450, sticky = E, padx = 25, pady = 10)

v = StringVar()
v.set("Click show to display the result")
Label(root, textvariable=v).grid(row=750, column=250, sticky=W, pady=4)
Button(text='Show', command=display_result).grid(row=800, column = 250, sticky=W, pady=4)

root.mainloop()