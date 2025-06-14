
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

def forecasting(data: pd.DataFrame):
    # data harus memiliki kolom 'bulan' dan 'permintaan'
    data = data.copy()
    data['bulan'] = np.arange(1, len(data) + 1).reshape(-1, 1)
    model = LinearRegression()
    model.fit(data[['bulan']], data['permintaan'])

    # Prediksi 3 bulan ke depan
    bulan_prediksi = np.arange(len(data) + 1, len(data) + 4).reshape(-1, 1)
    prediksi = model.predict(bulan_prediksi)
    hasil = pd.DataFrame({
        'Bulan': ['Bulan ke-' + str(i) for i in range(len(data)+1, len(data)+4)],
        'Prediksi Permintaan': np.round(prediksi, 2)
    })
    return hasil
