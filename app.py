
import streamlit as st
import pandas as pd
from model_lp import solve_lp
from model_eoq import hitung_eoq
from model_mm1 import mm1_model
from model_forecasting import forecasting


st.sidebar.title("📘 Petunjuk Aplikasi")
st.sidebar.markdown("""
- Pilih model matematika di tab atas
- Masukkan parameter sesuai kebutuhan
- Hasil dan grafik akan tampil di bawah
""")

tab1, tab2, tab3, tab4 = st.tabs(["🔧 Linear Programming", "📦 EOQ", "📈 Antrian M/M/1", "📊 Peramalan Permintaan (Forecasting)"])

with tab1:
    st.header("Linear Programming - Optimasi Produksi")
    x, y, z = solve_lp()
    st.success(f"Produksi optimal: A={x}, B={y}, Profit={z}")

with tab2:
    st.header("Model Persediaan EOQ")
    D = st.number_input("Permintaan Tahunan (D)", value=1000)
    S = st.number_input("Biaya Pemesanan (S)", value=50)
    H = st.number_input("Biaya Penyimpanan (H)", value=5)
    eoq = hitung_eoq(D, S, H)
    st.success(f"EOQ = {eoq:.2f}")

with tab3:
    st.header("Model Antrian M/M/1")
    λ = st.number_input("Laju Kedatangan (λ)", value=2.0)
    μ = st.number_input("Laju Pelayanan (μ)", value=4.0)
    result = mm1_model(λ, μ)
    st.success(f"Hasil: {result}")

with tab4:
    st.header("Model Peramalan (Forecasting)")
    st.markdown("Masukkan data permintaan historis per bulan (minimal 3 data).")

    input_data = st.text_area("Masukkan angka permintaan tiap bulan, pisahkan dengan koma", "120, 130, 140")
    try:
        angka = [int(x.strip()) for x in input_data.split(",")]
        if len(angka) >= 3:
            df = pd.DataFrame({"permintaan": angka})
            hasil = forecasting(df)
            st.dataframe(hasil)
        else:
            st.warning("Minimal masukkan 3 data permintaan.")
    except:
        st.error("Format input salah. Gunakan angka dipisah koma, contoh: 120,130,140")
