import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(layout="wide", page_title="Dashboard Kualitas Udara")

st.title("📊 Dashboard Kualitas Udara")

# === Load Data Gabungan ===
@st.cache_data
def load_data():
    df = pd.read_csv("dashboard/main_data.csv")
    return df

df = load_data()

# === Sidebar: Filter Interaktif ===
st.sidebar.header("🔍 Filter Data")

# Dropdown pilih stasiun
stasiun_list = df["station"].unique()
selected_station = st.sidebar.selectbox("Pilih Stasiun", stasiun_list)

# Multiselect tahun & bulan
years = sorted(df["year"].unique())
months = sorted(df["month"].unique())

selected_years = st.sidebar.multiselect("Pilih Tahun", years, default=years)
selected_months = st.sidebar.multiselect("Pilih Bulan", months, default=months)

# Filter berdasarkan input
filtered_df = df[
    (df["station"] == selected_station) &
    (df["year"].isin(selected_years)) &
    (df["month"].isin(selected_months))
]

# === Rata-rata PM2.5 per Bulan dan Jam ===
st.subheader("Rata-rata PM2.5 per Bulan dan Jam")

col1, col2 = st.columns(2)

with col1:
    avg_pm25_month = filtered_df.groupby("month")["PM2.5"].mean()
    fig1, ax1 = plt.subplots()
    ax1.plot(avg_pm25_month.index, avg_pm25_month.values, marker='o')
    ax1.set_title("Rata-rata PM2.5 per Bulan")
    ax1.set_xlabel("Bulan")
    ax1.set_ylabel("PM2.5")
    st.pyplot(fig1)

with col2:
    avg_pm25_hour = filtered_df.groupby("hour")["PM2.5"].mean()
    fig2, ax2 = plt.subplots()
    ax2.plot(avg_pm25_hour.index, avg_pm25_hour.values, marker='o')
    ax2.set_title("Rata-rata PM2.5 per Jam")
    ax2.set_xlabel("Jam")
    ax2.set_ylabel("PM2.5")
    st.pyplot(fig2)

# === Korelasi Polutan dan Faktor Cuaca ===
st.subheader("Korelasi Polutan dan Faktor Cuaca")

corr_columns = ["PM10", "NO2", "TEMP", "DEWP", "RAIN"]
corr_matrix = filtered_df[corr_columns].corr()

fig3, ax3 = plt.subplots(figsize=(6, 5))
sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", ax=ax3)
ax3.set_title("Korelasi Polutan dan Faktor Cuaca")
st.pyplot(fig3)

# Cari info puncak jam dan bulan PM2.5
jam_tertinggi = avg_pm25_hour.idxmax() if not avg_pm25_hour.empty else "-"
nilai_pm25_jam = avg_pm25_hour.max() if not avg_pm25_hour.empty else "-"

bulan_tertinggi = avg_pm25_month.idxmax() if not avg_pm25_month.empty else "-"
nilai_pm25_bulan = avg_pm25_month.max() if not avg_pm25_month.empty else "-"

# Korelasi suhu dan PM10
korelasi_temp_pm10 = corr_matrix.loc["TEMP", "PM10"] if "TEMP" in corr_matrix.columns and "PM10" in corr_matrix.columns else 0

# Korelasi hujan dan NO2
korelasi_rain_no2 = corr_matrix.loc["RAIN", "NO2"] if "RAIN" in corr_matrix.columns and "NO2" in corr_matrix.columns else 0

# Interpretasi korelasi sederhana
def interpret_korelasi(nilai):
    if abs(nilai) < 0.1:
        return "tidak signifikan"
    elif nilai > 0:
        return "positif"
    else:
        return "negatif"

interpretasi_temp = interpret_korelasi(korelasi_temp_pm10)
interpretasi_rain = interpret_korelasi(korelasi_rain_no2)

# === Insight Dinamis ===
# Cari info puncak jam dan bulan PM2.5
jam_tertinggi = avg_pm25_hour.idxmax() if not avg_pm25_hour.empty else "-"
nilai_pm25_jam = avg_pm25_hour.max() if not avg_pm25_hour.empty else "-"

bulan_tertinggi = avg_pm25_month.idxmax() if not avg_pm25_month.empty else "-"
nilai_pm25_bulan = avg_pm25_month.max() if not avg_pm25_month.empty else "-"

# Korelasi suhu dan PM10
korelasi_temp_pm10 = corr_matrix.loc["TEMP", "PM10"] if "TEMP" in corr_matrix.columns and "PM10" in corr_matrix.columns else 0

# Korelasi hujan dan NO2
korelasi_rain_no2 = corr_matrix.loc["RAIN", "NO2"] if "RAIN" in corr_matrix.columns and "NO2" in corr_matrix.columns else 0

# Interpretasi korelasi sederhana
def interpret_korelasi(nilai):
    if abs(nilai) < 0.1:
        return "tidak signifikan"
    elif nilai > 0:
        return "positif"
    else:
        return "negatif"

interpretasi_temp = interpret_korelasi(korelasi_temp_pm10)
interpretasi_rain = interpret_korelasi(korelasi_rain_no2)

st.markdown(f"""
### 📌 Insight Berdasarkan Filter

- **Puncak PM2.5 per Jam:** jam **{jam_tertinggi}** dengan nilai rata-rata **{nilai_pm25_jam:.2f}**
- **Puncak PM2.5 per Bulan:** bulan **{bulan_tertinggi}** dengan nilai rata-rata **{nilai_pm25_bulan:.2f}**
- **Hubungan antara suhu (TEMP) dan PM10:** korelasi = **{korelasi_temp_pm10:.2f}** (**{interpretasi_temp}**)
- **Hubungan antara hujan (RAIN) dan NO2:** korelasi = **{korelasi_rain_no2:.2f}** (**{interpretasi_rain}**)
""")
