import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="Air Quality Dashboard", page_icon="🌬️", layout="wide")

st.title("🌬️ Air Quality Analysis Dashboard (PRSA)")
st.markdown("Dashboard interaktif untuk eksplorasi data Kualitas Udara PRSA. Gunakan **filter di sidebar** untuk menyesuaikan rentang waktu pengamatan, dan **klik stasiun pada peta** untuk melihat analisis detailnya.")

# Load Data
@st.cache_data
def load_data():
    import os
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, "main_data.csv")
    df = pd.read_csv(file_path)
    df['datetime'] = pd.to_datetime(df['datetime'])
    return df

try:
    df = load_data()
except FileNotFoundError:
    st.error("File 'main_data.csv' tidak ditemukan. Pastikan Anda telah menjalankan notebook dan menghasilkan file tersebut.")
    st.stop()

# Koordinat stasiun
station_coords = {
    'Aotizhongxin': [39.982, 116.397],
    'Changping': [40.216, 116.230],
    'Dingling': [40.292, 116.220],
    'Dongsi': [39.929, 116.417],
    'Guanyuan': [39.929, 116.339],
    'Gucheng': [39.914, 116.184],
    'Huairou': [40.328, 116.628],
    'Nongzhanguan': [39.937, 116.461],
    'Shunyi': [40.127, 116.655],
    'Tiantan': [39.886, 116.407],
    'Wanliu': [39.987, 116.287],
    'Wanshouxigong': [39.878, 116.352]
}

# --- SIDEBAR: FITUR INTERAKTIF (DATE RANGE) ---
st.sidebar.header("Filter Eksplorasi Data")

min_date = df['datetime'].min().date()
max_date = df['datetime'].max().date()

try:
    start_date, end_date = st.sidebar.date_input(
        label='Rentang Waktu Pengamatan',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )
except ValueError:
    st.error("Harap pilih rentang waktu dengan benar (Start Date dan End Date).")
    st.stop()

# Memastikan ada 2 elemen
if not (start_date and end_date):
    st.stop()

# Filter data utama berdasarkan rentang waktu yang dipilih
main_df = df[(df['datetime'].dt.date >= start_date) & (df['datetime'].dt.date <= end_date)]

if main_df.empty:
    st.warning("Tidak ada data pada rentang waktu tersebut.")
    st.stop()

# Hitung Rata-rata untuk Peta berdasarkan data yang difilter
station_pm25 = main_df.groupby('station')['PM2.5'].mean().reset_index()

# --- PETA UTAMA ---
st.subheader(f"📍 Peta Interaktif Kualitas Udara")
st.markdown(f"Menampilkan agregasi data dari **{start_date} hingga {end_date}**. Semakin besar/merah lingkarannya, semakin tinggi polusinya. **Klik salah satu stasiun** untuk memunculkan grafiknya di bawah!")

# Inisialisasi peta Folium (Pusat di Beijing)
m = folium.Map(location=[40.1, 116.4], zoom_start=9, tiles="CartoDB positron")

# Tambahkan marker ke peta
for index, row in station_pm25.iterrows():
    station_name = row['station']
    pm25_val = row['PM2.5']
    if station_name in station_coords:
        coords = station_coords[station_name]
        
        # Penentuan warna & ukuran berdasarkan PM2.5
        color = 'red' if pm25_val > 80 else 'orange' if pm25_val > 50 else 'green'
        radius = max(5, pm25_val / 8) 
        
        folium.CircleMarker(
            location=coords,
            radius=radius,
            popup=f"{station_name}\\nPM2.5: {pm25_val:.1f}",
            tooltip=station_name,
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.7
        ).add_to(m)

# Tampilkan Peta dan Tangkap Interaksi
map_data = st_folium(m, height=450, use_container_width=True)

# Fungsi mencari stasiun yang diklik
def get_clicked_station(click_lat, click_lon):
    for name, coords in station_coords.items():
        if abs(coords[0] - click_lat) < 0.05 and abs(coords[1] - click_lon) < 0.05:
            return name
    return None

# Ambil data klik
clicked_station = None
if map_data and map_data.get("last_object_clicked"):
    click_lat = map_data["last_object_clicked"]["lat"]
    click_lon = map_data["last_object_clicked"]["lng"]
    clicked_station = get_clicked_station(click_lat, click_lon)

st.markdown("---")

# --- BAGIAN ANALISIS STASIUN (MUNCUL JIKA DIKLIK) ---
if clicked_station:
    st.header(f"📊 Analisis Detail: Stasiun {clicked_station}")
    
    # Filter data khusus stasiun ini, tetapi tetap dalam rentang waktu yang difilter di sidebar
    df_station = main_df[main_df['station'] == clicked_station]
    
    # Metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("Rata-rata PM2.5", f"{df_station['PM2.5'].mean():.2f}")
    col2.metric("Maksimal PM2.5", f"{df_station['PM2.5'].max():.2f}")
    col3.metric("Minimal PM2.5", f"{df_station['PM2.5'].min():.2f}")
    
    # Visualisasi 1: Tren PM2.5 (Berdasarkan waktu)
    st.subheader(f"Tren PM2.5 di {clicked_station} ({start_date} s/d {end_date})")
    
    # Kita resample/kelompokkan by Date agar grafiknya rapi (khususnya jika direntang waktu yang luas)
    daily_pm25 = df_station.groupby(df_station['datetime'].dt.date)['PM2.5'].mean().reset_index()
    
    fig1, ax1 = plt.subplots(figsize=(10, 4))
    sns.lineplot(x='datetime', y='PM2.5', data=daily_pm25, color='purple', ax=ax1)
    ax1.set_xlabel('Tanggal', fontsize=10)
    ax1.set_ylabel('Rata-rata Harian PM2.5', fontsize=10)
    ax1.grid(True, linestyle='--', alpha=0.7)
    
    # Putar label x-axis agar tidak bertumpuk
    plt.xticks(rotation=45)
    st.pyplot(fig1)
    
    # Visualisasi 2: Dampak Cuaca Terhadap Polusi (Musim Panas)
    st.subheader(f"Pengaruh Cuaca Terhadap Polusi PM2.5")
    
    fig2, ax2 = plt.subplots(1, 2, figsize=(14, 4))
    
    # Scatter plot Suhu
    sns.scatterplot(x='TEMP', y='PM2.5', data=df_station, alpha=0.5, ax=ax2[0], color='blue')
    ax2[0].set_title('Suhu vs PM2.5')
    
    # Scatter plot Hujan
    sns.scatterplot(x='RAIN', y='PM2.5', data=df_station, alpha=0.5, ax=ax2[1], color='green')
    ax2[1].set_title('Curah Hujan vs PM2.5')
    
    st.pyplot(fig2)
    st.caption("Interaksi suhu dan curah hujan terhadap tingkat konsentrasi PM2.5 (Data disesuaikan dengan filter rentang waktu).")

else:
    # State awal sebelum klik
    st.info("👆 Silakan klik pada salah satu titik stasiun di peta di atas untuk memunculkan analisis dan grafiknya secara spesifik!")

st.markdown("---")
st.markdown("**Dicoding | Belajar Analisis Data dengan Python**")
