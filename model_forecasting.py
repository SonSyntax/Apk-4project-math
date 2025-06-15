import numpy as np

def forecast_regresi(data_bulanan, bulan_ke):
    x = np.arange(1, len(data_bulanan) + 1)
    y = np.array(data_bulanan)
    coef = np.polyfit(x, y, 1)
    a, b = coef
    prediksi = a * bulan_ke + b
    return round(prediksi, 2), a, b
