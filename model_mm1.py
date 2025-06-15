# model_queue.py

def hitung_antrian(lam, mu):
    if lam >= mu:
        return {"error": "Sistem tidak stabil (λ ≥ μ), gunakan nilai μ > λ"}

    rho = lam / mu
    L = lam / (mu - lam)
    Lq = lam**2 / (mu * (mu - lam))
    W = 1 / (mu - lam)
    Wq = lam / (mu * (mu - lam))

    return {
        "ρ (Utilisasi)": round(rho, 3),
        "L (Pelanggan di sistem)": round(L, 3),
        "Lq (Pelanggan dalam antrean)": round(Lq, 3),
        "W (Waktu di sistem - jam)": round(W, 3),
        "Wq (Waktu antre - jam)": round(Wq, 3)
    }
