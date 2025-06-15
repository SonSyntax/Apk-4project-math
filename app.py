import streamlit as st
import numpy as np 
import pandas as pd
from model_lp import solve_lp
from model_eoq import hitung_eoq
from model_mm1 import hitung_antrian
from model_forecasting import forecast_regresi
import matplotlib.pyplot as plt


st.set_page_config(page_title="Aplikasi Model Industri", layout="centered")
st.sidebar.title("📘 Instruksi")
st.sidebar.write("Silakan pilih model industri dan masukkan parameter sesuai kebutuhan.")


tabs = st.tabs(["Linear Programming", "EOQ", "Antrian M/M/1", "Forecasting"])

# === TAB 1: Linear Programming ===
with tabs[0]:
    st.header("🔧 Linear Programming")

    st.markdown("### Masukkan Fungsi Objektif")
    obj_func = st.text_input("Contoh: 40000*x + 60000*y", value="40000*x + 60000*y")

    st.markdown("### Masukkan Kendala Produksi")
    constraints_text = st.text_area("Setiap kendala dipisah baris. Contoh:\n2*x + 3*y <= 100", value="2*x + 3*y <= 100")

    if st.button("🔍 Hitung Solusi Optimal"):
        constraints = [c.strip() for c in constraints_text.split("\n") if c.strip()]
        result = solve_lp(obj_func, constraints)

        if "error" in result:
            st.error(f"❌ Terjadi kesalahan: {result['error']}")
        else:
            x_val, y_val, z = result["x"], result["y"], result["obj"]

            st.success("✅ Solusi Optimal Ditemukan:")
            st.write(f"Jumlah ** (x)**: {x_val}")
            st.write(f"Jumlah ** (y)**: {y_val}")
            st.write(f"💰 Keuntungan Maksimum: Rp {z:,.0f}")

            # Grafik visualisasi
            st.markdown("### 📊 Visualisasi Kendala dan Titik Optimal")

            x_range = np.linspace(0, 60, 400)
            fig, ax = plt.subplots(figsize=(7, 5))

            for cons in constraints:
                try:
                    if "<=" in cons:
                        left, right = cons.split("<=")
                        y_vals = eval(f"({float(right)} - ({left.strip().replace('x', '*x_range')})) / 1.0", {"x_range": x_range, "np": np})
                        ax.plot(x_range, y_vals, label=cons, color='blue')
                    elif ">=" in cons:
                        left, right = cons.split(">=")
                        y_vals = eval(f"({float(right)} - ({left.strip().replace('x', '*x_range')})) / 1.0", {"x_range": x_range, "np": np})
                        ax.plot(x_range, y_vals, label=cons, linestyle="dashed", color='green')
                except:
                    continue

            ax.plot(x_val, y_val, 'ro', label='Solusi Optimal')
            ax.set_xlabel("x ")
            ax.set_ylabel("y ")
            ax.set_title("Grafik Linear Programming")
            ax.legend()
            ax.grid(True)

            st.pyplot(fig)

# === TAB 2: EOQ ===
with tabs[1]:
    st.header("📦 Model Persediaan EOQ")
    D = st.number_input("Permintaan Tahunan (D)", value=12000)
    S = st.number_input("Biaya Pemesanan per Order (S)", value=100000)
    H = st.number_input("Biaya Penyimpanan per Unit per Tahun (H)", value=1000)

    if st.button("Hitung EOQ"):
        hasil = hitung_eoq(D, S, H)
        st.success("✅ Hasil:")
        st.write(f"EOQ: {hasil['EOQ']} unit")
        st.write(f"Frekuensi Pemesanan: {hasil['Frekuensi']} kali/tahun")
        st.write(f"Total Biaya Minimum: Rp{hasil['Total_Biaya']:,}")

        # Grafik
        Q_range = list(range(100, int(hasil["EOQ"] * 2 + 500), 100))
        biaya = [(q / 2) * H + (D / q) * S for q in Q_range]

        fig, ax = plt.subplots()
        ax.plot(Q_range, biaya, label="Total Biaya", color='blue')
        ax.axvline(hasil["EOQ"], linestyle="--", color="red", label=f"EOQ = {hasil['EOQ']}")
        ax.set_xlabel("Kuantitas Order")
        ax.set_ylabel("Total Biaya (Rp)")
        ax.set_title("Grafik EOQ vs Total Biaya")
        ax.legend()
        st.pyplot(fig)

# === TAB 3: Antrian M/M/1 ===
with tabs[2]:
    st.title("📈 Model Antrian M/M/1")

    st.markdown("### Masukkan Parameter")
    lam = st.number_input("λ (Laju Kedatangan per Jam)", min_value=0.1, value=10.0)
    mu = st.number_input("μ (Laju Pelayanan per Jam)", min_value=0.1, value=12.0)

    if lam >= mu:
        st.error("⚠️ Sistem tidak stabil! λ harus lebih kecil dari μ.")
    else:
        # Perhitungan langsung
        rho = lam / mu
        L = lam / (mu - lam)
        W = 1 / (mu - lam)
        Wq = lam / (mu * (mu - lam))

        st.markdown("### Hasil Perhitungan Antrian")
        st.write(f"**ρ (Tingkat Utilisasi)**: {round(rho, 3)}")
        st.write(f"**L (Rata-rata pelanggan dalam sistem)**: {round(L, 3)}")
        st.write(f"**W (Waktu rata-rata dalam sistem - jam)**: {round(W, 3)} jam")
        st.write(f"**W (Waktu rata-rata dalam sistem - menit)**: {round(W * 60, 1)} menit")
        st.write(f"**Wq (Waktu menunggu dalam antrean - jam)**: {round(Wq, 3)} jam")
        st.write(f"**Wq (Waktu menunggu dalam antrean - menit)**: {round(Wq * 60, 1)} menit")

        # Visualisasi
        st.markdown("### Visualisasi: Waktu Tunggu Antrean (Wq) vs Laju Kedatangan (λ)")
        lam_range = np.linspace(0.1, mu - 0.01, 100)
        wq_values = [(l / (mu * (mu - l))) * 60 for l in lam_range]  # Wq dalam menit

        fig, ax = plt.subplots()
        ax.plot(lam_range, wq_values, color="orange", label="Wq (menit)")
        ax.axvline(lam, color='red', linestyle='--', label=f"λ saat ini ({lam})")
        ax.set_xlabel("λ (Laju Kedatangan per Jam)")
        ax.set_ylabel("Waktu Antrean Wq (menit)")
        ax.set_title("Grafik Wq terhadap λ (M/M/1 Queue)")
        ax.legend()
        ax.grid(True)
        st.pyplot(fig)

# === TAB 4: Forecasting ===
with tabs[3]:
    st.title("📈 Forecasting Penjualan dengan Moving Average")

    # Input jumlah bulan historis
    st.markdown("### Masukkan Data Penjualan per Bulan")
    bulan_list = []
    penjualan_list = []

    default_bulan = ['Januari', 'Februari', 'Maret', 'April', 'Mei']
    default_penjualan = [120, 150, 130, 160, 170]

    jumlah_data = st.number_input("Jumlah bulan data historis", min_value=3, max_value=12, value=5, step=1)

    with st.form("form_penjualan"):
        for i in range(jumlah_data):
            bulan = st.text_input(f"Bulan ke-{i+1}", value=default_bulan[i] if i < len(default_bulan) else f"Bulan-{i+1}", key=f"bulan_{i}")
            penjualan = st.number_input(f"Penjualan bulan ke-{i+1}", value=default_penjualan[i] if i < len(default_penjualan) else 100, key=f"penjualan_{i}")
            bulan_list.append(bulan)
            penjualan_list.append(penjualan)
        submitted = st.form_submit_button("Proses Peramalan")

    if submitted:
        data = pd.DataFrame({
            'Bulan': bulan_list,
            'Penjualan': penjualan_list
        })

        st.write("### Data Penjualan")
        st.dataframe(data)

        window = st.slider("Gunakan Moving Average berapa bulan?", min_value=2, max_value=jumlah_data, value=3)

        n_pred = st.slider("Prediksi hingga berapa bulan ke depan?", min_value=1, max_value=12, value=3)

        # Lakukan moving average
        forecast = []
        months_extended = bulan_list.copy()
        penjualan_extended = penjualan_list.copy()

        for i in range(n_pred):
            if len(penjualan_extended) < window:
                break
            ma = np.mean(penjualan_extended[-window:])
            forecast.append(round(ma, 2))
            penjualan_extended.append(ma)
            months_extended.append(f"Prediksi-{i+1}")

        # Tampilkan hasil prediksi
        st.write("### Hasil Peramalan")
        for i, val in enumerate(forecast):
            st.write(f"Bulan Prediksi-{i+1}: {val} unit")

        # Visualisasi
        st.markdown("### Visualisasi Penjualan dan Prediksi")
        fig, ax = plt.subplots()
        ax.plot(months_extended[:len(penjualan_list)], penjualan_list, marker='o', label="Penjualan Aktual")
        ax.plot(months_extended[len(penjualan_list):], forecast, marker='x', linestyle='--', color='orange', label="Prediksi")
        ax.set_xlabel("Bulan")
        ax.set_ylabel("Penjualan")
        ax.set_title("Grafik Penjualan dan Prediksi Moving Average")
        ax.legend()
        plt.xticks(rotation=45)
        plt.grid(True)
        st.pyplot(fig)
