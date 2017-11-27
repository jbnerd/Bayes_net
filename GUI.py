from Tkinter import *
import ttk
from read_file import *
from bayes_net_definitions import *
import copy

content = read_file()
bn = BayesNet(content)


varlist = copy.deepcopy(bn.variables)

def calculation():
    values = [[item.get() for item in baccha] for baccha in var]
    pos_query_item = [varlist[i] for i,val in enumerate(values[0]) if val > 0]
    neg_query_item = ['~' + varlist[i] for i,val in enumerate(values[1]) if val > 0]
    query_item = pos_query_item + neg_query_item
    pos_evidence_item = [varlist[i] for i,val in enumerate(values[2]) if val > 0]
    neg_evidence_item = ['~' + varlist[i] for i,val in enumerate(values[3]) if val > 0]
    evidence_item = pos_evidence_item + neg_evidence_item
    query = " ".join(query_item)
    evidence = " ".join(evidence_item)
    try:
        querychecks(query_item, evidence_item)
    except AssertionError:
        v.set('Wrong input, see the rules')
    else:
        tota = Expr(query, evidence)
        prod = 1
        for key, val in tota.query_vars.items():
            prod *= gibbs_ask(key, tota.cond_vars, bn, 5000)[val]
        v.set(prod)

def querychecks(query, evidence):
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

var = [[IntVar() for _ in range(len(varlist))] for _ in range(4)]

for i, val in enumerate(varlist):
    Checkbutton(root, text = str(val), variable=var[0][i]).grid(row = 50 + 5 * i, column = 100, sticky = E, padx = 25, pady = 10)
    Checkbutton(root, text = "~" + str(val), variable=var[1][i]).grid(row = 50 + 5 * i, column = 150, sticky = E, padx = 25, pady = 10)
    Checkbutton(root, text = str(val), variable=var[2][i]).grid(row = 50 + 5 * i, column = 400, sticky = E, padx = 25, pady = 10)
    Checkbutton(root, text = "~" + str(val), variable=var[3][i]).grid(row = 50 + 5 * i, column = 450, sticky = E, padx = 25, pady = 10)

v = StringVar()
v.set("Click show to display the result")
Label(root, textvariable=v).grid(row=750, column=250, sticky=W, pady=4)
Button(text='Show', command=calculation).grid(row=800, column = 250, sticky=W, pady=4)

root.mainloop()