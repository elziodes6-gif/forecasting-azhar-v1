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

# --- FUNGSI BANTU PERHITUNGAN (dipisah agar rumus tidak bocor data) ---

def hitung_bobot_linear(n):
    """Menghasilkan bobot linear meningkat (data terbaru mendapat bobot terbesar), total = 1."""
    mentah = list(range(1, n + 1))
    total = sum(mentah)
    return [m / total for m in mentah]

def rata_rata_tertimbang(window):
    """Weighted moving average untuk satu window data (urut lama -> baru)."""
    bobot = hitung_bobot_linear(len(window))
    return sum(w * v for w, v in zip(bobot, window))

# ==========================================
# SLIDE 0: HALAMAN AWAL (PENGENALAN)
# ==========================================
if st.session_state['halaman'] == 0:
    st.markdown(f"<h2 style='text-align: center; margin-bottom: 10px; color: {WARNA_AKSEN}; font-weight: 800; letter-spacing: 1px;'>PANDUAN SISTEM FORECASTING</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #666666; margin-bottom: 20px;'>Pelajari teori dasar sebelum menggunakan aplikasi peramalan.</p>", unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="large")
    with col1:
        teks_forecasting = "Forecasting atau peramalan adalah proses memperkirakan suatu kejadian atau kebutuhan yang akan terjadi pada masa yang akan datang berdasarkan data yang pernah terjadi sebelumnya (data historis). Tujuan forecasting adalah membantu perusahaan dalam mengambil keputusan, seperti menentukan jumlah persediaan, merencanakan pembelian bahan baku, menyusun jadwal produksi, atau memperkirakan permintaan pelanggan. Meskipun hasil forecasting tidak dapat menjamin keadaan yang akan datang secara tepat, hasil peramalan dapat menjadi dasar yang lebih baik dibandingkan mengambil keputusan tanpa menggunakan data."
        gambar_kotak_penjelasan("Apa itu Forecasting?", WARNA_AKSEN, teks_forecasting)
    with col2:
        teks_metode = "<p style='margin-top: 0; margin-bottom: 10px;'><b>Single Exponential Smoothing:</b> Metode yang memberikan bobot lebih besar pada data terbaru dibandingkan data yang lebih lama.</p><p style='margin-bottom: 10px;'><b>Double Exponential Smoothing:</b> Pengembangan dari Single Exponential Smoothing. Digunakan ketika data tidak hanya berubah, tetapi juga menunjukkan tren (terus meningkat/menurun).</p><p style='margin-bottom: 10px;'><b>Moving Average:</b> Metode yang menggunakan rata-rata dari beberapa data terakhir untuk memperkirakan nilai pada periode berikutnya.</p><p style='margin-bottom: 0; padding-top: 10px; border-top: 1px dashed #CCCCCC;'><b>Weighted Moving Average (WMA):</b> Memberikan persentase bobot yang berbeda, di mana data terbaru mendapat porsi terbesar.</p>"
        gambar_kotak_penjelasan("Metode Peramalan", WARNA_AKSEN, teks_metode)

    st.write("")
    st.write("")
    _, col_btn, _ = st.columns([2, 1, 2])
    with col_btn:
        st.button("Halaman Berikutnya ➔", on_click=lanjut_halaman, use_container_width=True)

# ==========================================
# SLIDE 1: PENJELASAN PARAMETER
# ==========================================
elif st.session_state['halaman'] == 1:
    st.markdown(f"<h2 style='text-align: center; margin-bottom: 10px; color: {WARNA_AKSEN}; font-weight: 800; letter-spacing: 1px;'>PARAMETER KONTROL</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #666666; margin-bottom: 20px;'>Penjelasan parameter pembobot yang akan Anda gunakan di dalam aplikasi.</p>", unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="large")
    with col1:
        teks_alpha = "Alpha adalah angka yang digunakan untuk menentukan seberapa besar pengaruh data terbaru terhadap hasil forecast. Nilai alpha berada di antara 0 dan 1.<br><br><b>Alpha kecil (misalnya 0,1)</b> membuat forecast berubah secara perlahan karena lebih banyak mempertimbangkan data sebelumnya.<br><br><b>Alpha besar (misalnya 0,8)</b> membuat forecast lebih cepat mengikuti perubahan data terbaru."
        gambar_kotak_penjelasan("Parameter Alpha", WARNA_AKSEN, teks_alpha)
    with col2:
        teks_beta = "Beta adalah parameter yang digunakan untuk mengatur seberapa cepat perubahan tren diperbarui.<br><br><b>Beta kecil</b> membuat perubahan tren berlangsung lebih lambat.<br><br><b>Beta besar</b> membuat perubahan tren lebih cepat mengikuti kondisi terbaru."
        gambar_kotak_penjelasan("Parameter Beta", WARNA_AKSEN, teks_beta)

    st.write("")
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
                    st.caption(f"Proyeksi: {item['horizon']}")
                    st.dataframe(item['data'], use_container_width=True)

    st.markdown(f"<h1 style='color: {WARNA_AKSEN};'>Dashboard Peramalan & Analisis Error</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #555555;'>Proyeksikan data Anda dan evaluasi akurasinya menggunakan metrik peramalan standar industri.</p>", unsafe_allow_html=True)

    st.markdown(f"<h3 style='color: {WARNA_AKSEN};'>Pengaturan Metode & Output</h3>", unsafe_allow_html=True)
    col_m1, col_m2 = st.columns(2)
    with col_m1:
        metode = st.selectbox(
            "Pilih Metode Peramalan:",
            ["Double Exponential Smoothing (DES)", "Single Exponential Smoothing (SES)", "Moving Average (MA)", "Weighted Moving Average (WMA)"]
        )
    with col_m2:
        opsi_tampilan = st.radio("Pilihan Tampilan:", ["Lengkap (Chart & Tabel)", "Chart Saja", "Tabel Saja"], horizontal=True)

    st.markdown(f"<h3 style='color: {WARNA_AKSEN};'>Pengaturan Waktu Proyeksi (Masa Depan)</h3>", unsafe_allow_html=True)
    col_w1, col_w2 = st.columns(2)
    with col_w1:
        satuan_waktu = st.selectbox("Satuan Waktu:", ["Bulan", "Hari", "Tahun"])
    with col_w2:
        # FIX: sebelumnya horizon dipaksa = 1 khusus untuk Moving Average sehingga
        # pengguna tidak bisa memilih jumlah periode proyeksi. Sekarang semua metode
        # bisa memilih horizon secara bebas.
        horizon = st.number_input(f"Berapa {satuan_waktu} ke depan?", min_value=1, max_value=100, value=3, step=1)

    st.markdown("<hr style='border:1px solid #EEEEEE'>", unsafe_allow_html=True)
    tampilkan_alfa = metode in ["Single Exponential Smoothing (SES)", "Double Exponential Smoothing (DES)"]
    tampilkan_beta = metode == "Double Exponential Smoothing (DES)"
    tampilkan_periode = metode in ["Moving Average (MA)", "Weighted Moving Average (WMA)"]

    col_p1, col_p2 = st.columns(2)
    alfa_global, beta_global = 0.20, 0.11
    periode_window = 3  # default periode untuk MA / WMA

    if tampilkan_alfa:
        with col_p1: alfa_global = st.number_input("Nilai Alfa (α) Global:", min_value=0.0, max_value=1.0, value=0.20, step=0.01)
    if tampilkan_beta:
        with col_p2: beta_global = st.number_input("Nilai Beta (β) Global:", min_value=0.0, max_value=1.0, value=0.11, step=0.01)
    if tampilkan_periode:
        # FIX: sebelumnya periode MA hardcode = 3 dan bobot WMA hardcode 0.6/0.4
        # (hanya 2 periode). Sekarang periode bisa diatur, dan bobot WMA otomatis
        # dihitung secara linear untuk sejumlah periode yang dipilih.
        with col_p1:
            periode_window = st.slider("Jumlah Periode untuk Rata-rata:", min_value=2, max_value=12, value=3, step=1)
        if metode == "Weighted Moving Average (WMA)":
            with col_p2:
                bobot_preview = ", ".join(f"{b:.2f}" for b in hitung_bobot_linear(periode_window))
                st.caption(f"Bobot otomatis (lama → baru): {bobot_preview}")

    st.markdown("<hr style='border:1px solid #EEEEEE'>", unsafe_allow_html=True)
    opsi_input = st.radio("Pilih Metode Input Data:", ["Input Manual via Tabel Menyamping", "Unggah (Upload) File CSV / Excel"], horizontal=True)

    df_input_horizontal = None
    df_raw_upload = None
    kolom_pilihan_upload = None

    # --- TABEL INPUT MENYAMPING ---
    if opsi_input == "Input Manual via Tabel Menyamping":
        st.markdown(f"<h3 style='color: {WARNA_AKSEN};'>Tabel Input Data</h3>", unsafe_allow_html=True)

        jumlah_kolom = st.slider("Geser untuk mengatur jumlah sel data historis:", min_value=3, max_value=60, value=12, step=1)

        kolom_nama = [i + 1 for i in range(jumlah_kolom)]

        df_template = pd.DataFrame(index=["Data Aktual"])
        for col in kolom_nama:
            df_template[col] = [None]

        st.markdown("<p style='color: #666666; font-size: 13px;'>Ketik data Anda menyamping ke kanan. Kolom kosong di akhir akan diabaikan.</p>", unsafe_allow_html=True)
        df_input_horizontal = st.data_editor(df_template, use_container_width=True)

    else:
        st.markdown(f"<h3 style='color: {WARNA_AKSEN};'>Unggah File Data</h3>", unsafe_allow_html=True)
        uploaded_file = st.file_uploader("Pilih file Anda (.csv atau .xlsx):", type=["xlsx", "csv"])
        if uploaded_file is not None:
            try:
                df_raw_upload = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
                st.success("File berhasil diunggah!")
                st.dataframe(df_raw_upload.head(500), use_container_width=True)

                # FIX BUG UTAMA: kode lama langsung mencari kolom bernama persis
                # "Data Historis" pada file upload, padahal kolom itu tidak akan
                # pernah ada di file yang diunggah pengguna -> pasti KeyError/crash.
                # Sekarang pengguna memilih sendiri kolom mana yang berisi data historis.
                kolom_pilihan_upload = st.selectbox(
                    "Pilih kolom yang berisi data historis (angka):",
                    options=list(df_raw_upload.columns)
                )
            except Exception as e:
                st.error(f"Gagal membaca file: {e}")

    st.markdown("<hr style='border:1px solid #EEEEEE'>", unsafe_allow_html=True)

    if st.button("Jalankan Peramalan & Analisis", type="primary"):

        data_valid = True
        df_kerja = pd.DataFrame()

        if opsi_input == "Input Manual via Tabel Menyamping":
            if df_input_horizontal is None:
                st.error("Tabel input belum tersedia.")
                data_valid = False
            else:
                df_kerja = df_input_horizontal.T.reset_index()
                df_kerja.columns = ["Index", "Data Historis"]
                df_kerja['Data Historis'] = pd.to_numeric(df_kerja['Data Historis'], errors='coerce')
        else:
            # FIX: guard eksplisit bila belum ada file / kolom yang dipilih,
            # supaya tidak crash dengan traceback yang membingungkan pengguna.
            if df_raw_upload is None:
                st.error("Silakan unggah file terlebih dahulu.")
                data_valid = False
            elif kolom_pilihan_upload is None:
                st.error("Silakan pilih kolom data historis.")
                data_valid = False
            else:
                df_kerja = pd.DataFrame({
                    "Data Historis": pd.to_numeric(df_raw_upload[kolom_pilihan_upload], errors='coerce')
                })

        if data_valid:
            df_kerja = df_kerja.dropna(subset=["Data Historis"]).reset_index(drop=True)

            if df_kerja.empty:
                st.error("Data masih kosong atau tidak ada angka valid yang terbaca.")
            elif len(df_kerja) < 2:
                st.error("Minimal dibutuhkan 2 data historis untuk melakukan peramalan yang bermakna.")
            else:
                try:
                    df_proses = df_kerja.head(500).copy()

                    hasil_kalkulasi = []
                    actuals_history = []
                    prev_forecast, prev_level, prev_trend = 0.0, 0.0, 0.0

                    for idx, row_data in df_proses.reset_index(drop=True).iterrows():
                        val_bulan = idx + 1
                        val_actual = float(row_data["Data Historis"])

                        val_level, val_trend, val_forecast = 0.0, 0.0, 0.0

                        # PENTING: forecast untuk periode idx HARUS hanya memakai data
                        # sampai idx-1 (actuals_history sebelum di-append). Versi lama
                        # meng-append actual dulu baru menghitung forecast MA/WMA/SES,
                        # sehingga forecast "mengintip" nilai aktual periode itu sendiri
                        # (data leakage) dan membuat MAPE/MAD/MSE tampak jauh lebih baik
                        # dari kenyataan. Di sini urutannya diperbaiki.
                        if metode == "Single Exponential Smoothing (SES)":
                            if idx == 0:
                                val_forecast = val_actual
                            else:
                                val_forecast = (alfa_global * actuals_history[idx - 1]) + ((1 - alfa_global) * prev_forecast)
                            prev_forecast = val_forecast

                        elif metode == "Double Exponential Smoothing (DES)":
                            # DES pada kode asli sudah benar (tidak bocor data): forecast
                            # dihitung dari level & trend sebelumnya, baru level/trend
                            # diperbarui memakai actual saat ini. Dipertahankan.
                            if idx == 0:
                                val_level, val_trend, val_forecast = val_actual, 0.0, val_actual
                            else:
                                val_forecast = prev_level + prev_trend
                                val_level = (alfa_global * val_actual) + ((1 - alfa_global) * (prev_level + prev_trend))
                                val_trend = (beta_global * (val_level - prev_level)) + ((1 - beta_global) * prev_trend)
                            prev_level, prev_trend = val_level, val_trend

                        elif metode == "Moving Average (MA)":
                            if idx == 0:
                                val_forecast = val_actual
                            else:
                                start_idx = max(0, idx - periode_window)
                                window = actuals_history[start_idx:idx]
                                val_forecast = sum(window) / len(window)
                            prev_forecast = val_forecast

                        elif metode == "Weighted Moving Average (WMA)":
                            if idx == 0:
                                val_forecast = val_actual
                            else:
                                start_idx = max(0, idx - periode_window)
                                window = actuals_history[start_idx:idx]
                                val_forecast = rata_rata_tertimbang(window)
                            prev_forecast = val_forecast

                        actuals_history.append(val_actual)

                        hasil_kalkulasi.append({
                            "Index": val_bulan, "Data Historis": val_actual, "Hasil Forecasting": val_forecast,
                            "Upper PI": None, "Lower PI": None
                        })

                    df_hist = pd.DataFrame(hasil_kalkulasi)

                    df_hist['Eror Forecast'] = df_hist['Data Historis'] - df_hist['Hasil Forecasting']
                    df_hist['Absolute Eror'] = df_hist['Eror Forecast'].abs()
                    df_hist['Squared Eror'] = df_hist['Eror Forecast'] ** 2
                    df_hist['PE (%)'] = df_hist.apply(lambda r: (r['Eror Forecast'] / r['Data Historis'] * 100) if r['Data Historis'] != 0 else 0, axis=1)
                    df_hist['APE (%)'] = df_hist['PE (%)'].abs()
                    df_hist['Cumulative Error'] = df_hist['Eror Forecast'].cumsum()
                    df_hist['Cumulative MAD'] = df_hist['Absolute Eror'].expanding().mean()
                    df_hist['Tracking Signal'] = df_hist.apply(lambda r: (r['Cumulative Error'] / r['Cumulative MAD']) if r['Cumulative MAD'] != 0 else 0, axis=1)

                    bias = df_hist['Eror Forecast'].mean()
                    mad = df_hist['Absolute Eror'].mean()
                    mse = df_hist['Squared Eror'].mean()
                    rmse = mse ** 0.5
                    mpe = df_hist['PE (%)'].mean()
                    mape = df_hist['APE (%)'].mean()
                    ts_akhir = df_hist['Tracking Signal'].iloc[-1] if not df_hist.empty else 0

                    # Hitung forecast SATU langkah ke depan (memakai seluruh data historis
                    # yang ada) sebagai titik awal proyeksi masa depan, lalu diperpanjang
                    # datar (naive) untuk horizon > 1, karena tidak ada data aktual baru.
                    n_data = len(actuals_history)
                    if metode == "Single Exponential Smoothing (SES)":
                        forecast_awal_masa_depan = (alfa_global * actuals_history[-1]) + ((1 - alfa_global) * prev_forecast)
                    elif metode == "Moving Average (MA)":
                        window = actuals_history[max(0, n_data - periode_window):n_data]
                        forecast_awal_masa_depan = sum(window) / len(window)
                    elif metode == "Weighted Moving Average (WMA)":
                        window = actuals_history[max(0, n_data - periode_window):n_data]
                        forecast_awal_masa_depan = rata_rata_tertimbang(window)
                    else:  # DES
                        forecast_awal_masa_depan = None  # DES pakai prev_level + h*prev_trend langsung

                    hasil_kalkulasi_future = []
                    jumlah_historis = len(df_proses)

                    for h in range(1, int(horizon) + 1):
                        future_index = jumlah_historis + h

                        if metode == "Double Exponential Smoothing (DES)":
                            future_forecast = prev_level + (h * prev_trend)
                        else:
                            future_forecast = forecast_awal_masa_depan

                        pi_margin = 1.96 * rmse * math.sqrt(h)

                        hasil_kalkulasi_future.append({
                            "Index": future_index,
                            "Data Historis": None,
                            "Hasil Forecasting": future_forecast,
                            "Upper PI": future_forecast + pi_margin,
                            "Lower PI": future_forecast - pi_margin,
                            "Eror Forecast": None, "Absolute Eror": None, "Squared Eror": None,
                            "PE (%)": None, "APE (%)": None, "Tracking Signal": None
                        })

                    df_future = pd.DataFrame(hasil_kalkulasi_future)
                    df_hasil_final = pd.concat([df_hist, df_future], ignore_index=True)

                    waktu_sekarang = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    st.session_state['riwayat_forecasting'].append({
                        "waktu": waktu_sekarang, "metode": metode, "horizon": f"{horizon} {satuan_waktu}", "data": df_hasil_final
                    })

                    st.markdown(f"<br><h1 style='text-align: center; color: {WARNA_AKSEN}; font-size: 40px; font-weight: bold; background-color: #FFF5F5; padding: 20px; border-radius: 10px; border: 1px dashed {WARNA_AKSEN};'>FORECAST SELESAI</h1><br>", unsafe_allow_html=True)
                    st.balloons()

                    if opsi_tampilan in ["Lengkap (Chart & Tabel)", "Chart Saja"]:

                        fig = go.Figure()

                        fig.add_trace(go.Scatter(
                            x=df_hist['Index'], y=df_hist['Data Historis'],
                            mode='lines+markers', name='Actual',
                            line=dict(color='#1F77B4', width=1.5), marker=dict(symbol='circle', size=7, color='#1F77B4'),
                            hovertemplate='<b>Index: %{x}</b><br>Actual: %{y}<extra></extra>'
                        ))

                        fig.add_trace(go.Scatter(
                            x=df_hist['Index'], y=df_hist['Hasil Forecasting'],
                            mode='lines+markers', name='Fits',
                            line=dict(color='#A03A3A', width=1.5, dash='dash'), marker=dict(symbol='square', size=6, color='#A03A3A'),
                            hovertemplate='<b>Index: %{x}</b><br>Fit: %{y:.2f}<extra></extra>'
                        ))

                        fig.add_trace(go.Scatter(
                            x=df_future['Index'], y=df_future['Hasil Forecasting'],
                            mode='lines+markers', name='Forecasts',
                            line=dict(color='#2CA02C', width=1.5, dash='dash'), marker=dict(symbol='diamond', size=6, color='#2CA02C'),
                            hovertemplate='<b>Index: %{x}</b><br>Forecast: %{y:.2f}<extra></extra>'
                        ))

                        fig.add_trace(go.Scatter(
                            x=df_future['Index'], y=df_future['Upper PI'],
                            mode='lines+markers', name='95.0% PI',
                            line=dict(color='#8E44AD', width=1.5, dash='dashdot'), marker=dict(symbol='triangle-up', size=7, color='#8E44AD'),
                            hovertemplate='<b>Index: %{x}</b><br>Upper PI: %{y:.2f}<extra></extra>'
                        ))

                        fig.add_trace(go.Scatter(
                            x=df_future['Index'], y=df_future['Lower PI'],
                            mode='lines+markers', name='95.0% PI Lower',
                            line=dict(color='#8E44AD', width=1.5, dash='dashdot'), marker=dict(symbol='triangle-down', size=7, color='#8E44AD'),
                            hovertemplate='<b>Index: %{x}</b><br>Lower PI: %{y:.2f}<extra></extra>',
                            showlegend=False
                        ))

                        if metode == "Double Exponential Smoothing (DES)":
                            const_text = f"α (level)&nbsp;&nbsp;&nbsp;&nbsp;{alfa_global:.2f}<br>β (trend)&nbsp;&nbsp;&nbsp;{beta_global:.2f}"
                        elif metode == "Single Exponential Smoothing (SES)":
                            const_text = f"α (level)&nbsp;&nbsp;&nbsp;&nbsp;{alfa_global:.2f}"
                        elif metode in ["Moving Average (MA)", "Weighted Moving Average (WMA)"]:
                            const_text = f"Periode&nbsp;&nbsp;&nbsp;&nbsp;{periode_window}"
                        else:
                            const_text = "N/A"

                        fig.update_layout(
                            height=500,
                            title=dict(
                                text=f"<b>Smoothing Plot for Analisis Peramalan</b><br><span style='font-size: 14px; color: #666;'>{metode}</span>",
                                x=0.5, xanchor='center'
                            ),
                            xaxis=dict(domain=[0, 0.78], type='linear', showgrid=True, gridcolor='#EAECEE', title="Index", tickmode='linear', dtick=1),
                            yaxis=dict(showgrid=True, gridcolor='#EAECEE', title="Jumlah / Value"),
                            plot_bgcolor='#FFFFFF', paper_bgcolor='#FFFFFF',
                            legend=dict(
                                title=dict(text="Variable", font=dict(size=12, color="black")),
                                x=0.80, y=0.95, xanchor="left", yanchor="top",
                                bgcolor="rgba(255,255,255,1)", bordercolor="#EAECEE", borderwidth=1
                            ),
                            margin=dict(l=40, r=220, t=80, b=40)
                        )

                        if const_text != "N/A":
                            fig.add_annotation(
                                x=0.80, y=0.55, xref="paper", yref="paper",
                                text=f"<span style='font-size:12px; color:black;'><b>Smoothing Constants</b></span><br><span style='font-size:12px; color:black;'>{const_text}</span>",
                                showarrow=False, align="left", xanchor="left", yanchor="top"
                            )

                        acc_text = f"MAPE&nbsp;&nbsp;&nbsp;{mape:.2f}<br>MAD&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{mad:.2f}<br>MSD&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{mse:.2f}"
                        fig.add_annotation(
                            x=0.80, y=0.30, xref="paper", yref="paper",
                            text=f"<span style='font-size:12px; color:black;'><b>Accuracy Measures</b></span><br><span style='font-size:12px; color:black;'>{acc_text}</span>",
                            showarrow=False, align="left", xanchor="left", yanchor="top"
                        )

                        fig.update_xaxes(mirror=True, ticks='outside', showline=True, linecolor='black')
                        fig.update_yaxes(mirror=True, ticks='outside', showline=True, linecolor='black')

                        st.plotly_chart(fig, use_container_width=True)

                    if opsi_tampilan in ["Lengkap (Chart & Tabel)", "Tabel Saja"]:
                        st.markdown(f"<h3 style='color: {WARNA_AKSEN};'>Tabel Detail Kalkulasi & Error</h3>", unsafe_allow_html=True)
                        st.dataframe(df_hasil_final.style.format(precision=2, na_rep='-'), use_container_width=True)

                    output = io.BytesIO()
                    with pd.ExcelWriter(output, engine='openpyxl') as writer:
                        df_hasil_final.to_excel(writer, index=False, sheet_name='Hasil_Peramalan')
                    st.download_button("Unduh File Excel Lengkap", data=output.getvalue(), file_name=f"Forecasting_{waktu_sekarang.replace(':', '-')}.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

                except Exception as e:
                    # FIX: sebelumnya error apapun saat komputasi akan menampilkan
                    # traceback penuh dan menghentikan seluruh aplikasi tanpa
                    # penjelasan yang jelas bagi pengguna awam.
                    st.error(f"Terjadi kesalahan saat menghitung peramalan: {e}")
