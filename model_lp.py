from pulp import LpMaximize, LpProblem, LpVariable

def solve_lp(obj_func: str, constraints: list):
    model = LpProblem("Linear Programming", LpMaximize)

    x = LpVariable("x", lowBound=0)
    y = LpVariable("y", lowBound=0)
    variables = {"x": x, "y": y}

    try:
        # Fungsi objektif
        model += eval(obj_func, {}, variables)

        # Tambahkan kendala
        for constraint in constraints:
            if "<=" in constraint:
                left, right = constraint.split("<=")
                model += eval(left.strip(), {}, variables) <= float(right)
            elif ">=" in constraint:
                left, right = constraint.split(">=")
                model += eval(left.strip(), {}, variables) >= float(right)
            elif "=" in constraint or "==" in constraint:
                left, right = constraint.replace("=", "==").split("==")
                model += eval(left.strip(), {}, variables) == float(right)

        model.solve()

        return {
            "x": x.varValue,
            "y": y.varValue,
            "obj": model.objective.value()
        }

    except Exception as e:
        return {"error": str(e)}
