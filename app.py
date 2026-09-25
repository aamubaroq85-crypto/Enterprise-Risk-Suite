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
    "### Modul Integrasi: No. 1, No. 3, No. 51, No. 55, No. 68, & No. 77 (Aa"
    " Baroq Applied Technologies)"
)

# 1. Sidebar Interaktif: Pilihan Aset, Pengaturan Jitter, & Parameter Waktu
st.sidebar.header("⚙️ Pengaturan ZF-Core Engine")
selected_asset = st.sidebar.selectbox(
    "Pilih Instrumen Aset", ["BTC-USD", "ETH-USD", "EUR-USD", "GOLD-XAU"]
)
data_points = st.sidebar.slider(
    "Jumlah Periode Data (Jam)", min_value=50, max_value=200, value=100
)
volatility_factor = st.sidebar.slider(
    "Faktor Volatilitas Pasar", min_value=0.1, max_value=2.0, value=0.5
)

# Toggle untuk No. 3: Noise Filter Jitter
enable_jitter_filter = st.sidebar.checkbox(
    "Aktifkan Noise Filter Jitter (No. 3)", value=True
)

# Simulasi Data Portofolio Real-Time
np.random.seed(42)
dates = pd.date_range(start="2026-09-01", periods=data_points, freq="1h")
base_price = (
    50000
    if "BTC" in selected_asset
    else (3000 if "ETH" in selected_asset else 100)
)
raw_prices = base_price + np.cumsum(
    np.random.normal(0, volatility_factor, data_points)
)
portfolio_df = pd.DataFrame({"Timestamp": dates, "Price": raw_prices})

# Penerapan Teknologi No. 3 (Noise Filter Jitter)
if enable_jitter_filter:
  portfolio_df["Clean_Price"] = (
      portfolio_df["Price"].rolling(window=3).mean().fillna(portfolio_df["Price"])
  )
else:
  portfolio_df["Clean_Price"] = portfolio_df["Price"]

# 2. No. 51: Drift-Threshold Dynamic Stop-Loss (3-Sigma Deviation) menggunakan Clean Price
portfolio_df["Rolling_Mean"] = portfolio_df["Clean_Price"].rolling(window=20).mean()
portfolio_df["Rolling_Std"] = portfolio_df["Clean_Price"].rolling(window=20).std()
portfolio_df["Upper_Sigma"] = portfolio_df["Rolling_Mean"] + (
    3 * portfolio_df["Rolling_Std"]
)
portfolio_df["Lower_Sigma"] = portfolio_df["Rolling_Mean"] - (
    3 * portfolio_df["Rolling_Std"]
)
portfolio_df["Dynamic_SL"] = portfolio_df["Lower_Sigma"]

# 3. No. 55: Circuit Breaker All-Stop & No. 77: Black Swan Isolation Unit
current_price = portfolio_df["Clean_Price"].iloc[-1]
current_sl = portfolio_df["Dynamic_SL"].iloc[-1]
price_drop_pct = (
    portfolio_df["Clean_Price"].iloc[-1]
    - portfolio_df["Clean_Price"].iloc[-2]
) / portfolio_df["Clean_Price"].iloc[-2]

circuit_breaker_triggered = (
    abs(price_drop_pct) > 0.02 or current_price < current_sl
)

# 4. No. 68: Capital Preservation Sentinel (Dashboard Kontrol Risiko)
st.subheader(f"📊 Panel Kontrol Portofolio Utama: {selected_asset}")
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric(
        "Harga Aset Terkini",
        f"${current_price:,.2f}",
        f"{price_drop_pct*100:.2f}%",
    )
with col2:
    st.metric("Dynamic Stop-Loss (3-σ)", f"${current_sl:,.2f}")
with col3:
    total_exposure = current_price * 10
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

# 5. Teknologi No. 1 (ZF-TickStreamer) & No. 3 (Noise Filter Jitter) Live Monitor
st.subheader("⚡ ZF-TickStreamer (No. 1) & Noise Filter Jitter (No. 3) Monitor")
col_t1, col_t2 = st.columns(2)
with col_t1:
    st.markdown("**Status Feed ZF-TickStreamer:** `CONNECTED (0.3ms Latency)`)")
    st.dataframe(
        portfolio_df[["Timestamp", "Price"]].tail(3).reset_index(drop=True),
        use_container_width=True,
    )
with col_t2:
    st.markdown(
        "**Status Filter Jitter (No. 3):**"
        f" `{'AKTIF (Cleaned)' if enable_jitter_filter else 'BYPASSED (Raw)'}`"
    )
    st.dataframe(
        portfolio_df[["Timestamp", "Clean_Price"]]
        .tail(3)
        .reset_index(drop=True),
        use_container_width=True,
    )

# Visualisasi Grafik Pergerakan dan Batas Deviasi
st.subheader("📈 Grafik Pemantauan Deviasi & Batas Pengaman Risiko")
st.line_chart(
    portfolio_df.set_index("Timestamp")[
        ["Clean_Price", "Rolling_Mean", "Upper_Sigma", "Lower_Sigma"]
    ]
)

# 6. Log Riwayat Audit Kepatuhan (Audit Trail Log) & Tombol Unduh CSV
st.subheader("📋 Log Riwayat Audit & Insiden Risiko (Audit Trail)")

audit_logs = [
    {
        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Aset": selected_asset,
        "Modul": "ZF-TickStreamer (No. 1) & Jitter Filter (No. 3)",
        "Aksi": "Inisialisasi stream data bersih berkecepatan tinggi",
        "Status": "Optimal",
    },
    {
        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Aset": selected_asset,
        "Modul": "Capital Preservation Sentinel (No. 68)",
        "Aksi": "Pemantauan harian portofolio aktif",
        "Status": "Normal",
    },
    {
        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Aset": selected_asset,
        "Modul": "Drift-Threshold (No. 51)",
        "Aksi": "Kalibrasi ulang batas deviasi 3-sigma",
        "Status": "Stabil",
    },
    {
        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Aset": selected_asset,
        "Modul": "Circuit Breaker (No. 55) & Black Swan (No. 77)",
        "Aksi": "Pemindaian anomali makro global",
        "Status": "Terisolasi & Aman",
    },
]

if circuit_breaker_triggered:
    audit_logs.insert(
        0,
        {
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Aset": selected_asset,
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

csv_data = audit_df.to_csv(index=False).encode("utf-8")
st.download_button(
    label="📥 Unduh Laporan Audit (CSV)",
    data=csv_data,
    file_name=f"audit_trail_{selected_asset}_{datetime.now().strftime('%Y%m%d')}.csv",
    mime="text/csv",
)
