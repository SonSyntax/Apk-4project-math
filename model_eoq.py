import math

def hitung_eoq(D, S, H):
    # EOQ Formula
    eoq = math.sqrt((2 * D * S) / H)

    # Frekuensi pemesanan
    frekuensi = D / eoq

    # Total biaya: penyimpanan + pemesanan
    biaya_total = (eoq / 2) * H + (D / eoq) * S

    return {
        "EOQ": round(eoq, 2),
        "Frekuensi": round(frekuensi, 2),
        "Total_Biaya": round(biaya_total, 2)
    }
