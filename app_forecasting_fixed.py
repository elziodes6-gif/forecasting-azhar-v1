import streamlit as st
import pandas as pd
import io
import math
import plotly.graph_objects as go
from datetime import datetime

# --- PENGATURAN HALAMAN & STATE ---
st.set_page_config(page_title="Sistem Peramalan Profesional", layout="wide", initial_sidebar_state="expanded")

if 'halaman' not in st.session_state:
    st.session_state['halaman'] = 0

if 'riwayat_forecasting' not in st.session_state:
    st.session_state['riwayat_forecasting'] = []

def lanjut_halaman():
    if st.session_state['halaman'] < 2:
        st.session_state['halaman'] += 1

def kembali_halaman():
    if st.session_state['halaman'] > 0:
        st.session_state['halaman'] -= 1

# --- KUSTOMISASI CSS (TEMA PUTIH AKSEN MERAH SEDANG) ---
st.markdown("""
<style>
    [data-testid="stAppViewContainer"] {
        background-color: #FFFFFF !important; 
        background-image: linear-gradient(to bottom, #FFFFFF 0%, #F9F9F9 100%) !important;
    }
    [data-testid="stHeader"] {
        background-color: rgba(0,0,0,0) !important;
    }
    [data-testid="stSidebar"] {
        background-color: #FAFAFA !important;
        box-shadow: 2px 0 15px rgba(0,0,0,0.03) !important;
        border-right: 1px solid #EEEEEE !important;
    }
    .main .block-container label, .main .block-container p, .main .block-container span {
        color: #333333 !important;
    }
    .stDataFrame *, div[data-testid="stDataEditor"] * {
        color: #000000 !important;
    }
</style>
""", unsafe_allow_html=True)

# --- FUNGSI PEMBUAT KOTAK DESAIN ---
def gambar_kotak_penjelasan(judul, warna_aksen, teks):
    html = f"""<div style="margin-top: 30px; margin-bottom: 10px;"><div style="border: 2px solid {warna_aksen}; border-radius: 12px; padding: 30px 25px 20px 25px; position: relative; background-color: #FFFFFF; box-shadow: 0 4px 15px rgba(0,0,0,0.03);"><div style="background-color: {warna_aksen}; color: #FFFFFF; padding: 6px 25px; border-radius: 6px; font-weight: bold; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; font-size: 15px; position: absolute; top: -18px; left: 50%; transform: translateX(-50%); white-space: nowrap; text-transform: uppercase; box-shadow: 0 4px 10px rgba(217, 83, 79, 0.3);">{judul}</div><div style="color: #444444; font-size: 15px; line-height: 1.7; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; text-align: justify;">{teks}</div></div></div>"""
    st.markdown(html, unsafe_allow_html=True)

WARNA_AKSEN = "#D9534F"

# --- FUNGSI BANTU PERHITUNGAN ---
def hitung_bobot_linear(n):
    mentah = list(range(1, n + 1))
    total = sum(mentah)
    return [m / total for m in mentah]

def rata_rata_tertimbang(window):
    bobot = hitung_bobot_linear(len(window))
    return sum(w * v for w, v in zip(bobot, window))

# ==========================================
# SLIDE 0: HALAMAN AWAL
# ==========================================
if st.session_state['halaman'] == 0:
    st.markdown(f"<h2 style='text-align: center; margin-bottom: 10px; color: {WARNA_AKSEN}; font-weight: 800; letter-spacing: 1px;'>PANDUAN SISTEM FORECASTING</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #666666; margin-bottom: 20px;'>Pelajari teori dasar sebelum menggunakan aplikasi peramalan.</p>", unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="large")
    with col1:
        teks_forecasting = "Forecasting atau peramalan adalah proses memperkirakan suatu kejadian atau kebutuhan yang akan terjadi pada masa yang akan datang berdasarkan data yang pernah terjadi sebelumnya (data historis)."
        gambar_kotak_penjelasan("Apa itu Forecasting?", WARNA_AKSEN, teks_forecasting)
    with col2:
        teks_metode = "<p style='margin-top: 0; margin-bottom: 10px;'><b>Single, Double, dan Triple Exponential Smoothing:</b> Metode ini mengakomodasi data berpola acak, tren, hingga yang memiliki unsur musiman.</p><p style='margin-bottom: 0;'><b>Moving Average & WMA:</b> Metode yang menggunakan rata-rata data terakhir untuk peramalan berikutnya.</p>"
        gambar_kotak_penjelasan("Metode Peramalan", WARNA_AKSEN, teks_metode)

    st.write("")
    _, col_btn, _ = st.columns([2, 1, 2])
    with col_btn:
        st.button("Halaman Berikutnya ➔", on_click=lanjut_halaman, use_container_width=True)

# ==========================================
# SLIDE 1: PENJELASAN PARAMETER
# ==========================================
elif st.session_state['halaman'] == 1:
    st.markdown(f"<h2 style='text-align: center; margin-bottom: 10px; color: {WARNA_AKSEN}; font-weight: 800; letter-spacing: 1px;'>PARAMETER KONTROL</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2, gap="large")
    with col1:
        teks_alpha = "Alpha (α) menentukan seberapa besar pengaruh data terbaru terhadap hasil forecast."
        gambar_kotak_penjelasan("Parameter Alpha", WARNA_AKSEN, teks_alpha)
    with col2:
        teks_beta = "Beta (β) mengatur kecepatan pembaruan tren. Gamma (γ) mengatur komponen musiman."
        gambar_kotak_penjelasan("Parameter Beta & Gamma", WARNA_AKSEN, teks_beta)

    st.write("")
    col_btn_kiri, _, col_btn_kanan = st.columns([1, 2, 1])
    with col_btn_kiri:
        st.button("⬅️ Sebelumnya", on_click=kembali_halaman, use_container_width=True)
    with col_btn_kanan:
        st.button("Mulai Aplikasi ➔", on_click=lanjut_halaman, use_container_width=True, type="primary")

# ==========================================
# SLIDE 2: APLIKASI UTAMA (DASHBOARD)
# ==========================================
elif st.session_state['halaman'] == 2:
    with st.sidebar:
        st.button("🏠 Kembali ke Buku Panduan", on_click=lambda: st.session_state.update(halaman=0), use_container_width=True)
        st.markdown("---")
        st.markdown(f"<h3 style='color: {WARNA_AKSEN};'>🕰️ Riwayat Forecasting</h3>", unsafe_allow_html=True)
        if st.button("🗑️ Hapus Semua Riwayat", type="primary"):
            st.session_state['riwayat_forecasting'] = []
            st.success("Riwayat berhasil dibersihkan!")
        st.markdown("---")

        if not st.session_state['riwayat_forecasting']:
            st.info("Belum ada riwayat peramalan.")
        else:
            for idx, item in enumerate(reversed(st.session_state['riwayat_forecasting'])):
                with st.expander(f"🕒 {item['waktu']}"):
                    st.caption(f"Metode: {item['metode']}")
                    st.dataframe(item['data'], use_container_width=True)

    st.markdown(f"<h1 style='color: {WARNA_AKSEN};'>Dashboard Peramalan & Analisis Error</h1>", unsafe_allow_html=True)
    
    col_m1, col_m2 = st.columns(2)
    with col_m1:
        metode = st.selectbox(
            "Pilih Metode Peramalan:",
            ["Single Exponential Smoothing (SES)", "Double Exponential Smoothing (DES)", "Triple Exponential Smoothing (TES)", "Moving Average (MA)", "Weighted Moving Average (WMA)"]
        )
    with col_m2:
        opsi_tampilan = st.radio("Pilihan Tampilan:", ["Lengkap (Chart & Tabel)", "Chart Saja", "Tabel Saja"], horizontal=True)

    col_w1, col_w2 = st.columns(2)
    with col_w1:
        satuan_waktu = st.selectbox("Satuan Waktu:", ["Bulan", "Hari", "Tahun"])
    with col_w2:
        horizon = st.number_input(f"Berapa {satuan_waktu} ke depan?", min_value=1, max_value=100, value=3, step=1)

    st.markdown("<hr style='border:1px solid #EEEEEE'>", unsafe_allow_html=True)
    
    # Pengaturan visibilitas parameter
    tampilkan_alfa = metode in ["Single Exponential Smoothing (SES)", "Double Exponential Smoothing (DES)", "Triple Exponential Smoothing (TES)"]
    # Menampilkan beta untuk SES seperti permintaan, meskipun secara matematis SES tidak memiliki tren
    tampilkan_beta = metode in ["Single Exponential Smoothing (SES)", "Double Exponential Smoothing (DES)", "Triple Exponential Smoothing (TES)"]
    tampilkan_gamma = metode == "Triple Exponential Smoothing (TES)"
    tampilkan_periode = metode in ["Moving Average (MA)", "Weighted Moving Average (WMA)"]

    alfa_global, beta_global, gamma_global = 0.20, 0.11, 0.10
    periode_musiman = 4
    periode_window = 3

    col_p1, col_p2, col_p3 = st.columns(3)
    
    if tampilkan_alfa:
        with col_p1: alfa_global = st.number_input("Nilai Alfa (α):", min_value=0.0, max_value=1.0, value=0.20, step=0.01)
    if tampilkan_beta:
        with col_p2: beta_global = st.number_input("Nilai Beta (β):", min_value=0.0, max_value=1.0, value=0.11, step=0.01)
    if tampilkan_gamma:
        with col_p3: gamma_global = st.number_input("Nilai Gamma (γ):", min_value=0.0, max_value=1.0, value=0.10, step=0.01)
        with col_p3: periode_musiman = st.number_input("Periode Musiman (L):", min_value=2, max_value=24, value=4, step=1)
    if tampilkan_periode:
        with col_p1: periode_window = st.slider("Jumlah Periode Rata-rata:", min_value=2, max_value=12, value=3, step=1)

    st.markdown("<hr style='border:1px solid #EEEEEE'>", unsafe_allow_html=True)
    opsi_input = st.radio("Pilih Metode Input Data:", ["Input Manual via Tabel Excel", "Unggah (Upload) File CSV / Excel"], horizontal=True)

    df_input_vertikal = None
    df_raw_upload = None
    kolom_pilihan_upload = None

    if opsi_input == "Input Manual via Tabel Excel":
        st.markdown(f"<h3 style='color: {WARNA_AKSEN};'>Tabel Input Data (Excel-like)</h3>", unsafe_allow_html=True)
        st.markdown("<p style='color: #666666; font-size: 13px;'>Ketik angka ke bawah. Tekan <b>Enter</b> untuk otomatis turun ke baris baru di bawahnya. Anda dapat menghapus atau menambah baris secara dinamis.</p>", unsafe_allow_html=True)
        
        # Membuat tabel vertikal (mirip excel) menggunakan num_rows="dynamic"
        df_template = pd.DataFrame({"Data Historis": [None] * 12})
        df_input_vertikal = st.data_editor(df_template, use_container_width=True, num_rows="dynamic")

    else:
        st.markdown(f"<h3 style='color: {WARNA_AKSEN};'>Unggah File Data</h3>", unsafe_allow_html=True)
        uploaded_file = st.file_uploader("Pilih file Anda (.csv atau .xlsx):", type=["xlsx", "csv"])
        if uploaded_file is not None:
            df_raw_upload = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
            st.dataframe(df_raw_upload.head(), use_container_width=True)
            kolom_pilihan_upload = st.selectbox("Pilih kolom berisi data historis (angka):", options=list(df_raw_upload.columns))

    st.markdown("<hr style='border:1px solid #EEEEEE'>", unsafe_allow_html=True)

    if st.button("Jalankan Peramalan & Analisis", type="primary"):
        data_valid = True
        df_kerja = pd.DataFrame()

        if opsi_input == "Input Manual via Tabel Excel":
            if df_input_vertikal is None:
                data_valid = False
            else:
                df_kerja = df_input_vertikal.copy()
                df_kerja['Data Historis'] = pd.to_numeric(df_kerja['Data Historis'], errors='coerce')
        else:
            if df_raw_upload is None or kolom_pilihan_upload is None:
                st.error("Pastikan file telah diunggah dan kolom data dipilih.")
                data_valid = False
            else:
                df_kerja = pd.DataFrame({"Data Historis": pd.to_numeric(df_raw_upload[kolom_pilihan_upload], errors='coerce')})

        if data_valid:
            df_kerja = df_kerja.dropna(subset=["Data Historis"]).reset_index(drop=True)

            if len(df_kerja) < 2:
                st.error("Minimal dibutuhkan 2 data historis untuk peramalan.")
            else:
                df_proses = df_kerja.copy()
                hasil_kalkulasi = []
                actuals_history = []
                
                # Setup Variabel TES
                L = periode_musiman
                seasonals = []
                if metode == "Triple Exponential Smoothing (TES)":
                    if len(df_proses) < L:
                        st.error(f"Triple Exponential Smoothing membutuhkan data minimal sebanyak periode musiman ({L}).")
                        st.stop()
                    else:
                        initial_level = df_proses["Data Historis"].iloc[0:L].mean()
                        initial_trend = (df_proses["Data Historis"].iloc[L:2*L].mean() - initial_level) / L if len(df_proses) >= 2*L else 0.0
                        seasonals = [(df_proses["Data Historis"].iloc[i] - initial_level) for i in range(L)]
                        prev_level, prev_trend = initial_level, initial_trend

                prev_forecast, prev_level_des, prev_trend_des = 0.0, 0.0, 0.0

                for idx, row_data in df_proses.iterrows():
                    val_bulan = idx + 1
                    val_actual = float(row_data["Data Historis"])
                    val_forecast = 0.0

                    if metode == "Single Exponential Smoothing (SES)":
                        if idx == 0:
                            val_forecast = val_actual
                        else:
                            val_forecast = (alfa_global * actuals_history[idx - 1]) + ((1 - alfa_global) * prev_forecast)
                        prev_forecast = val_forecast

                    elif metode == "Double Exponential Smoothing (DES)":
                        if idx == 0:
                            val_level_des, val_trend_des, val_forecast = val_actual, 0.0, val_actual
                        else:
                            val_forecast = prev_level_des + prev_trend_des
                            val_level_des = (alfa_global * val_actual) + ((1 - alfa_global) * (prev_level_des + prev_trend_des))
                            val_trend_des = (beta_global * (val_level_des - prev_level_des)) + ((1 - beta_global) * prev_trend_des)
                        prev_level_des, prev_trend_des = val_level_des, val_trend_des
                    
                    elif metode == "Triple Exponential Smoothing (TES)":
                        s_index = idx % L
                        if idx == 0:
                            val_forecast = val_actual
                        else:
                            val_forecast = prev_level + prev_trend + seasonals[s_index]
                        
                        val_level = (alfa_global * (val_actual - seasonals[s_index])) + ((1 - alfa_global) * (prev_level + prev_trend))
                        val_trend = (beta_global * (val_level - prev_level)) + ((1 - beta_global) * prev_trend)
                        seasonals[s_index] = (gamma_global * (val_actual - val_level)) + ((1 - gamma_global) * seasonals[s_index])
                        prev_level, prev_trend = val_level, val_trend

                    elif metode == "Moving Average (MA)":
                        if idx == 0:
                            val_forecast = val_actual
                        else:
                            window = actuals_history[max(0, idx - periode_window):idx]
                            val_forecast = sum(window) / len(window)

                    elif metode == "Weighted Moving Average (WMA)":
                        if idx == 0:
                            val_forecast = val_actual
                        else:
                            window = actuals_history[max(0, idx - periode_window):idx]
                            val_forecast = rata_rata_tertimbang(window)

                    actuals_history.append(val_actual)
                    hasil_kalkulasi.append({"Index": val_bulan, "Data Historis": val_actual, "Hasil Forecasting": val_forecast, "Upper PI": None, "Lower PI": None})

                df_hist = pd.DataFrame(hasil_kalkulasi)
                df_hist['Eror Forecast'] = df_hist['Data Historis'] - df_hist['Hasil Forecasting']
                df_hist['Absolute Eror'] = df_hist['Eror Forecast'].abs()
                df_hist['Squared Eror'] = df_hist['Eror Forecast'] ** 2
                df_hist['PE (%)'] = df_hist.apply(lambda r: (r['Eror Forecast'] / r['Data Historis'] * 100) if r['Data Historis'] != 0 else 0, axis=1)
                df_hist['APE (%)'] = df_hist['PE (%)'].abs()

                mse = df_hist['Squared Eror'].mean()
                rmse = mse ** 0.5
                mape = df_hist['APE (%)'].mean()
                mad = df_hist['Absolute Eror'].mean()

                n_data = len(actuals_history)
                if metode == "Single Exponential Smoothing (SES)":
                    forecast_awal_masa_depan = (alfa_global * actuals_history[-1]) + ((1 - alfa_global) * prev_forecast)
                elif metode == "Moving Average (MA)":
                    window = actuals_history[max(0, n_data - periode_window):n_data]
                    forecast_awal_masa_depan = sum(window) / len(window)
                elif metode == "Weighted Moving Average (WMA)":
                    window = actuals_history[max(0, n_data - periode_window):n_data]
                    forecast_awal_masa_depan = rata_rata_tertimbang(window)
                else: 
                    forecast_awal_masa_depan = None

                hasil_kalkulasi_future = []
                for h in range(1, int(horizon) + 1):
                    future_index = n_data + h
                    
                    if metode == "Double Exponential Smoothing (DES)":
                        future_forecast = prev_level_des + (h * prev_trend_des)
                    elif metode == "Triple Exponential Smoothing (TES)":
                        s_idx = (n_data + h - 1) % L
                        future_forecast = prev_level + (h * prev_trend) + seasonals[s_idx]
                    else:
                        future_forecast = forecast_awal_masa_depan

                    pi_margin = 1.96 * rmse * math.sqrt(h)
                    hasil_kalkulasi_future.append({
                        "Index": future_index, "Data Historis": None, "Hasil Forecasting": future_forecast,
                        "Upper PI": future_forecast + pi_margin, "Lower PI": future_forecast - pi_margin
                    })

                df_future = pd.DataFrame(hasil_kalkulasi_future)
                df_hasil_final = pd.concat([df_hist, df_future], ignore_index=True)

                waktu_sekarang = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                st.session_state['riwayat_forecasting'].append({
                    "waktu": waktu_sekarang, "metode": metode, "data": df_hasil_final
                })

                st.markdown(f"<br><h1 style='text-align: center; color: {WARNA_AKSEN};'>FORECAST SELESAI</h1><br>", unsafe_allow_html=True)
                st.balloons()

                if opsi_tampilan in ["Lengkap (Chart & Tabel)", "Chart Saja"]:
                    fig = go.Figure()
                    fig.add_trace(go.Scatter(x=df_hist['Index'], y=df_hist['Data Historis'], mode='lines+markers', name='Actual', line=dict(color='#1F77B4')))
                    fig.add_trace(go.Scatter(x=df_hist['Index'], y=df_hist['Hasil Forecasting'], mode='lines+markers', name='Fits', line=dict(color='#A03A3A', dash='dash')))
                    fig.add_trace(go.Scatter(x=df_future['Index'], y=df_future['Hasil Forecasting'], mode='lines+markers', name='Forecasts', line=dict(color='#2CA02C', dash='dash')))
                    
                    if metode == "Double Exponential Smoothing (DES)":
                        const_text = f"α: {alfa_global:.2f}<br>β: {beta_global:.2f}"
                    elif metode == "Single Exponential Smoothing (SES)":
                        const_text = f"α: {alfa_global:.2f}<br>β: {beta_global:.2f}"
                    elif metode == "Triple Exponential Smoothing (TES)":
                        const_text = f"α: {alfa_global:.2f}<br>β: {beta_global:.2f}<br>γ: {gamma_global:.2f}"
                    else:
                        const_text = f"Periode: {periode_window}"

                    fig.update_layout(title=dict(text=f"<b>Smoothing Plot</b><br><span style='font-size: 14px;'>{metode}</span>"), margin=dict(l=40, r=220, t=80, b=40))
                    
                    fig.add_annotation(x=0.80, y=0.55, xref="paper", yref="paper", text=f"<b>Constants</b><br>{const_text}", showarrow=False, xanchor="left")
                    fig.add_annotation(x=0.80, y=0.30, xref="paper", yref="paper", text=f"<b>Accuracy</b><br>MAPE: {mape:.2f}<br>MAD: {mad:.2f}", showarrow=False, xanchor="left")
                    st.plotly_chart(fig, use_container_width=True)

                if opsi_tampilan in ["Lengkap (Chart & Tabel)", "Tabel Saja"]:
                    st.dataframe(df_hasil_final.style.format(precision=2, na_rep='-'), use_container_width=True)
