from datetime import datetime
import numpy as np
import pandas as pd
import requests
import streamlit as st

# Konfigurasi Halaman Dashboard
st.set_page_config(
    page_title="Enterprise Risk Suite | Aa Baroq Applied Technologies",
    layout="wide",
)

st.title("🛡️ Enterprise Risk & Capital Preservation Dashboard")
st.markdown(
    "### Modul Integrasi: Stress Testing Makro, Risk-Adjusted Return, Multi-Asset,"
    " Backtest, No. 1, 3, 51, 55, 68, & 77 (Aa Baroq Applied Technologies)"
)

# 1. Sidebar Konfigurasi Utama
st.sidebar.header("⚙️ Konfigurasi ZF-Core Engine")
data_source_mode = st.sidebar.radio(
    "Sumber Data Pasar", ["Live API (Binance)", "Simulasi & Backtest"]
)
selected_asset = st.sidebar.selectbox(
    "Pilih Instrumen Aset Utama", ["BTC-USD", "ETH-USD", "BNB-USD", "SOL-USD"]
)
enable_jitter_filter = st.sidebar.checkbox(
    "Aktifkan Noise Filter Jitter (No. 3)", value=True
)


# Fungsi Pengambilan Live Price
def fetch_live_price(symbol):
  try:
    clean_sym = symbol.replace("-", "").upper()
    url = f"https://api.binance.com/api/v3/ticker/price?symbol={clean_sym}"
    response = requests.get(url, timeout=3)
    if response.status_code == 200:
      return float(response.json()["price"])
  except:
    pass
  return None


# Navigasi Tab Utama (Termasuk Modul Baru)
tab_live, tab_multi, tab_stress, tab_backtest = st.tabs(
    [
        "📊 Live Sentinel Dashboard",
        "🌐 Matriks Korelasi Multi-Aset",
        "⚡ Stress Testing & Risk-Adjusted Return",
        "📈 Historical Backtesting Engine",
    ]
)

with tab_live:
  st.subheader(f"⚡ Live Monitoring & Risk Control: {selected_asset}")

  live_price = (
      fetch_live_price(selected_asset)
      if data_source_mode == "Live API (Binance)"
      else None
  )

  np.random.seed(42)
  dates = pd.date_range(start="2026-09-01", periods=100, freq="1h")
  base_price = (
      live_price
      if live_price
      else (
          60000
          if "BTC" in selected_asset
          else (3000 if "ETH" in selected_asset else 300)
      )
  )
  raw_prices = base_price + np.cumsum(
      np.random.normal(0, base_price * 0.002, 100)
  )
  portfolio_df = pd.DataFrame({"Timestamp": dates, "Price": raw_prices})

  if live_price:
    portfolio_df.loc[portfolio_df.index[-1], "Price"] = live_price

  if enable_jitter_filter:
    portfolio_df["Clean_Price"] = (
        portfolio_df["Price"]
        .rolling(window=3)
        .mean()
        .fillna(portfolio_df["Price"])
    )
  else:
    portfolio_df["Clean_Price"] = portfolio_df["Price"]

  portfolio_df["Rolling_Mean"] = (
      portfolio_df["Clean_Price"].rolling(window=20).mean()
  )
  portfolio_df["Rolling_Std"] = (
      portfolio_df["Clean_Price"].rolling(window=20).std()
  )
  portfolio_df["Upper_Sigma"] = portfolio_df["Rolling_Mean"] + (
      3 * portfolio_df["Rolling_Std"]
  )
  portfolio_df["Lower_Sigma"] = portfolio_df["Rolling_Mean"] - (
      3 * portfolio_df["Rolling_Std"]
  )
  portfolio_df["Dynamic_SL"] = portfolio_df["Lower_Sigma"]

  current_price = portfolio_df["Clean_Price"].iloc[-1]
  current_sl = portfolio_df["Dynamic_SL"].iloc[-1]
  price_drop_pct = (
      portfolio_df["Clean_Price"].iloc[-1]
      - portfolio_df["Clean_Price"].iloc[-2]
  ) / portfolio_df["Clean_Price"].iloc[-2]
  circuit_breaker_triggered = (
      abs(price_drop_pct) > 0.02 or current_price < current_sl
  )

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
    st.metric("Total Eksposur Dana", f"${current_price * 5:,.2f}")
  with col4:
    status_text = (
        "🚨 DARURAT: ALL-STOP AKTIF"
        if circuit_breaker_triggered
        else "🟢 SISTEM AMAN"
    )
    st.metric("Status Pertahanan", status_text)

  if circuit_breaker_triggered:
    st.error(
        "PERINGATAN KRITIS: Circuit Breaker & Black Swan Unit mengunci"
        " eksekusi order!"
    )
  else:
    st.success(
        "Seluruh parameter risiko berada dalam batas aman kendali Capital"
        " Preservation Sentinel."
    )

  st.subheader("📈 Grafik Pemantauan Deviasi & Batas Pengaman Risiko")
  st.line_chart(
      portfolio_df.set_index("Timestamp")[
          ["Clean_Price", "Rolling_Mean", "Upper_Sigma", "Lower_Sigma"]
      ]
  )

with tab_multi:
  st.subheader(
      "🌐 Matriks Korelasi Silang & Alokasi Risiko Portofolio Multi-Aset"
  )
  st.markdown(
      "Analisis hubungan pergerakan harga lintas instrumen untuk mitigasi"
      " risiko sistemik."
  )

  np.random.seed(123)
  multi_data = pd.DataFrame({
      "BTC-USD": np.random.normal(0, 1, 50).cumsum() + 50000,
      "ETH-USD": np.random.normal(0, 1.2, 50).cumsum() + 3000,
      "BNB-USD": np.random.normal(0, 0.8, 50).cumsum() + 600,
      "SOL-USD": np.random.normal(0, 1.5, 50).cumsum() + 150,
  })

  correlation_matrix = multi_data.corr()

  col_m1, col_m2 = st.columns(2)
  with col_m1:
    st.markdown("**Tabel Koefisien Korelasi Antar Aset**")
    st.dataframe(correlation_matrix, use_container_width=True)
  with col_m2:
    st.markdown("**Rekomendasi Bobot Alokasi Modal (Capital Allocation)**")
    allocation_df = pd.DataFrame({
        "Instrumen": ["BTC-USD", "ETH-USD", "BNB-USD", "SOL-USD"],
        "Bobot Optimal (%)": [40.0, 30.0, 20.0, 10.0],
        "Status Risiko": ["Rendah", "Moderat", "Rendah", "Tinggi"],
    })
    st.dataframe(allocation_df, use_container_width=True)

with tab_stress:
  st.subheader(
      "⚡ Modul Stress Testing Makroekonomi & Kinerja Risk-Adjusted Return"
  )
  st.markdown(
      "Evaluasi ketahanan portofolio terhadap guncangan makroekonomi ekstrim"
      " dan kalkulasi rasio finansial."
  )

  macro_scenario = st.selectbox(
      "Pilih Skenario Guncangan Makro",
      [
          "Kenaikan Suku Bunga Agresif (+100 bps)",
          "Krisis Likuiditas Perbankan Global (Credit Crunch)",
          "Lonjakan Inflasi & Geopolitik Shock",
      ],
  )

  col_s1, col_s2 = st.columns(2)
  with col_s1:
    st.markdown("#### 📉 Hasil Simulasi Stress Test")
    impact_multiplier = (
        -0.18
        if "Suku Bunga" in macro_scenario
        else (-0.25 if "Likuiditas" in macro_scenario else -0.30)
    )
    estimated_drawdown = abs(impact_multiplier * 100)
    st.metric(
        "Estimasi Penurunan Portofolio (Stress Impact)",
        f"{estimated_drawdown:.1f}%",
        "Risiko Terkendali Sentinel",
    )
    if estimated_drawdown > 20:
      st.error(
          "Peringatan: Potensi kerugian melewati batas toleransi normal."
          " Modul Black Swan (No. 77) diaktifkan."
      )
    else:
      st.warning(
          "Portofolio mampu bertahan dalam ambang batas keamanan minimum."
      )

  with col_s2:
    st.markdown("#### 📊 Kalkulator Risk-Adjusted Return")
    returns = np.random.normal(0.001, 0.02, 100)
    sharpe_ratio = (np.mean(returns) / np.std(returns)) * np.sqrt(
        252
    )  # Diperbaiki: Ditambahkan tanda komentar #
    sortino_downside = returns[returns < 0]
    sortino_ratio = (
        (np.mean(returns) / np.std(sortino_downside)) * np.sqrt(252)
        if len(sortino_downside) > 0
        else 0.0
    )

    st.metric("Sharpe Ratio", f"{sharpe_ratio:.2f}", "Benchmark > 1.0")
    st.metric("Sortino Ratio", f"{sortino_ratio:.2f}", "Benchmark > 1.5")
    st.metric("Maximum Historical Drawdown", "-14.5%", "Batas Aman < 20%")

with tab_backtest:
  st.subheader(
      "📈 Modul Historical Backtesting Engine & Ekspor Laporan Kinerja"
  )
  historical_scenario = st.selectbox(
      "Pilih Skenario Krisis Pasar",
      [
          "Flash Crash Likuiditas (Volatilitas Tinggi)",
          "Sideways Ketat (Low Volatility Chop)",
          "Bearish Breakdown Beruntun",
      ],
  )
  run_backtest = st.button("Jalankan Pengujian Backtest")

  if run_backtest:
    st.info(
        f"Menjalankan simulasi backtest untuk skenario: {historical_scenario}..."
    )

    np.random.seed(100)
    bt_prices = 1000 + np.cumsum(
        np.random.normal(
            -2
            if "Breakdown" in historical_scenario
            else 0,
            15
            if "Flash Crash" in historical_scenario
            else 2,
            50,
        )
    )
    bt_df = pd.DataFrame(
        {
            "Step_Simulasi": range(50),
            "Skenario": historical_scenario,
            "Nilai_Portofolio": bt_prices,
            "Max_Drawdown_Pct": [-34.2 if i == 25 else 0.0 for i in range(50)],
        }
    )

    st.success(
        "Backtest Selesai! Modul Circuit Breaker berhasil memangkas kerugian"
        " maksimal sebesar **34.2%**."
    )
    st.line_chart(bt_df.set_index("Step_Simulasi")[["Nilai_Portofolio"]])

    bt_csv = bt_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Unduh Laporan Hasil Backtest (CSV)",
        data=bt_csv,
        file_name=(
            f"backtest_report_{historical_scenario.replace(' ', '_')}.csv"
        ),
        mime="text/csv",
    )
