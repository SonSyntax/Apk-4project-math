
from pulp import LpMaximize, LpProblem, LpVariable

def solve_lp():
    model = LpProblem("Optimasi Produksi", LpMaximize)
    x = LpVariable("Produk_A", lowBound=0)
    y = LpVariable("Produk_B", lowBound=0)

    model += 20 * x + 30 * y
    model += 2 * x + y <= 100
    model += x + 3 * y <= 90

    model.solve()
    return x.varValue, y.varValue, model.objective.value()
