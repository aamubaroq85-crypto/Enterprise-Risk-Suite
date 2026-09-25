from datetime import datetime
import numpy as np
import pandas as pd
import streamlit as st

# Konfigurasi Halaman Dashboard
st.set_page_config(
    page_title="Enterprise Risk Suite | Aa Baroq Applied Technologies",
    layout="wide",
)

st.title("🛡️ Enterprise Risk & Capital Preservation Dashboard")
st.markdown(
    "### Modul Integrasi: No. 51, No. 55, No. 68, & No. 77 (Aa Baroq"
    " Applied Technologies)"
)

# Simulasi Data Portofolio Real-Time (Menggunakan freq='1h' agar kompatibel dengan pandas terbaru)
np.random.seed(42)
dates = pd.date_range(start="2026-09-01", periods=100, freq="1h")
prices = 100 + np.cumsum(np.random.normal(0, 0.5, 100))
portfolio_df = pd.DataFrame({"Timestamp": dates, "Price": prices})

# 1. No. 51: Drift-Threshold Dynamic Stop-Loss (3-Sigma Deviation)
portfolio_df["Rolling_Mean"] = portfolio_df["Price"].rolling(window=20).mean()
portfolio_df["Rolling_Std"] = portfolio_df["Price"].rolling(window=20).std()
portfolio_df["Upper_Sigma"] = portfolio_df["Rolling_Mean"] + (
    3 * portfolio_df["Rolling_Std"]
)
portfolio_df["Lower_Sigma"] = portfolio_df["Rolling_Mean"] - (
    3 * portfolio_df["Rolling_Std"]
)
portfolio_df["Dynamic_SL"] = portfolio_df[
    "Lower_Sigma"
]  # Stop-loss adaptif batas bawah

# 2. No. 55: Circuit Breaker All-Stop & No. 77: Black Swan Isolation Unit
current_price = portfolio_df["Price"].iloc[-1]
current_sl = portfolio_df["Dynamic_SL"].iloc[-1]
price_drop_pct = (
    portfolio_df["Price"].iloc[-1] - portfolio_df["Price"].iloc[-2]
) / portfolio_df["Price"].iloc[-2]

# Logika Pemicu Circuit Breaker (Volatilitas Ekstrem / Black Swan)
circuit_breaker_triggered = (
    abs(price_drop_pct) > 0.02 or current_price < current_sl
)

# 3. No. 68: Capital Preservation Sentinel (Dashboard Kontrol Risiko yang Diperluas)
st.subheader("📊 Panel Kontrol Portofolio Utama")
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric(
        "Harga Aset Terkini", f"${current_price:.2f}", f"{price_drop_pct*100:.2f}%"
    )
with col2:
    st.metric("Dynamic Stop-Loss (3-σ)", f"${current_sl:.2f}")
with col3:
    total_exposure = current_price * 1000  # Simulasi ukuran lot/posisi
    st.metric("Total Eksposur Dana", f"${total_exposure:,.2f}")
with col4:
    status_text = (
        "🚨 DARURAT: ALL-STOP AKTIF"
        if circuit_breaker_triggered
        else "🟢 SISTEM AMAN"
    )
    st.metric("Status Pertahanan", status_text)

if circuit_breaker_triggered:
    st.error(
        "PERINGATAN KRITIS: Circuit Breaker All-Stop dan Black Swan Isolation"
        " Unit berhasil mengunci seluruh eksekusi order otomatis untuk"
        " melindungi portofolio!"
    )
else:
    st.success(
        "Seluruh parameter risiko berada dalam batas aman kendali Capital"
        " Preservation Sentinel."
    )

# Visualisasi Grafik Pergerakan dan Batas Deviasi
st.subheader("📈 Grafik Pemantauan Deviasi & Batas Pengaman Risiko")
st.line_chart(
    portfolio_df.set_index("Timestamp")[
        ["Price", "Rolling_Mean", "Upper_Sigma", "Lower_Sigma"]
    ]
)

# 4. Penambahan Tabel Riwayat Audit Kepatuhan (Audit Trail Log) untuk Fund Manager
st.subheader("📋 Log Riwayat Audit & Insiden Risiko (Audit Trail)")

# Simulasi pembuatan log data riwayat sistem keamanan
audit_logs = [
    {
        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Modul": "Capital Preservation Sentinel (No. 68)",
        "Aksi": "Inisialisasi sistem pemantauan harian",
        "Status": "Normal",
    },
    {
        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Modul": "Drift-Threshold (No. 51)",
        "Aksi": "Kalibrasi ulang batas deviasi 3-sigma",
        "Status": "Stabil",
    },
    {
        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Modul": "Circuit Breaker (No. 55)",
        "Aksi": "Pemeriksaan integritas order pasar",
        "Status": "Standby",
    },
    {
        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Modul": "Black Swan Isolation (No. 77)",
        "Aksi": "Pemindaian anomali makro global",
        "Status": "Terisolasi & Aman",
    },
]

if circuit_breaker_triggered:
    audit_logs.insert(
        0,
        {
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Modul": "Circuit Breaker / Black Swan Unit",
            "Aksi": (
                "Pemicu darurat aktif karena deviasi ekstrem melampaui ambang"
                " batas"
            ),
            "Status": "TRIGGERED",
        },
    )

audit_df = pd.DataFrame(audit_logs)
st.dataframe(audit_df, use_container_width=True)
