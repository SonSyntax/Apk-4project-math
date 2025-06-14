
def mm1_model(lambda_val, mu_val):
    rho = lambda_val / mu_val
    if rho >= 1:
        return "Antrian tidak stabil"
    Lq = rho**2 / (1 - rho)
    Wq = Lq / lambda_val
    return f"Lq = {Lq:.2f}, Wq = {Wq:.2f}"
