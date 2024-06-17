import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Judul aplikasi
st.title("Proyek Analisis Data: Bike Sharing Dataset")

# Memuat data
df_hour = pd.read_csv('hour.csv')
df_daily = pd.read_csv('day.csv')

# Cleaning data
df_hour['dteday'] = pd.to_datetime(df_hour['dteday'])
df_daily['dteday'] = pd.to_datetime(df_daily['dteday'])

# Data Merging
hourly_agg = df_hour.groupby('dteday').agg({
    'season': 'first',
    'yr': 'first',
    'mnth': 'first',
    'holiday': 'first',
    'weekday': 'first',
    'workingday': 'first',
    'weathersit': 'mean',
    'temp': 'mean',
    'atemp': 'mean',
    'hum': 'mean',
    'windspeed': 'mean',
    'casual': 'sum',
    'registered': 'sum',
    'cnt': 'sum'
}).reset_index()

df = pd.merge(df_daily, hourly_agg, on='dteday', suffixes=('_daily', '_hourly'))

# Fungsi untuk kategorisasi
def categorize_season(month):
    if month in [3, 4, 5]:
        return 'Spring'
    elif month in [6, 7, 8]:
        return 'Summer'
    elif month in [9, 10, 11]:
        return 'Fall'
    else:
        return 'Winter'

def categorize_weather(weather):
    if weather == 1:
        return 'Clear'
    elif weather == 2:
        return 'Mist'
    elif weather == 3:
        return 'Light Snow/Rain'
    else:
        return 'Heavy Rain/Snow'

df['season_category'] = df['mnth_daily'].apply(categorize_season)
df['weather_category'] = df['weathersit_daily'].apply(categorize_weather)

# Sidebar untuk interaksi
st.sidebar.header("Filter Data")
selected_season = st.sidebar.selectbox("Pilih Musim", df['season_category'].unique())
selected_weather = st.sidebar.selectbox("Pilih Cuaca", df['weather_category'].unique())

filtered_data = df[(df['season_category'] == selected_season) & (df['weather_category'] == selected_weather)]

# Pertanyaan 1: Tren penyewaan sepeda
st.header("Tren Penyewaan Sepeda dari Waktu ke Waktu")
plt.figure(figsize=(10, 6))
sns.lineplot(data=filtered_data, x='dteday', y='cnt_daily')
plt.title(f'Total Rentals Over Time (Daily) - {selected_season}, {selected_weather}')
st.pyplot(plt)

# Visualisasi interaktif
st.header("Pengaruh Musim dan Cuaca terhadap Penyewaan Sepeda")
season_cluster = filtered_data.groupby('season_category').agg({
    'cnt_daily': 'mean',
    'temp_daily': 'mean',
    'hum_daily': 'mean',
    'windspeed_daily': 'mean'
}).reset_index()

weather_cluster = filtered_data.groupby('weather_category').agg({
    'cnt_daily': 'mean',
    'temp_daily': 'mean',
    'hum_daily': 'mean',
    'windspeed_daily': 'mean'
}).reset_index()

st.subheader("Rata-rata Penyewaan Sepeda Berdasarkan Musim")
plt.figure(figsize=(10, 6))
sns.barplot(data=season_cluster, x='season_category', y='cnt_daily')
plt.title('Average Rentals by Season')
st.pyplot(plt)

st.subheader("Rata-rata Penyewaan Sepeda Berdasarkan Cuaca")
plt.figure(figsize=(10, 6))
sns.barplot(data=weather_cluster, x='weather_category', y='cnt_daily')
plt.title('Average Rentals by Weather')
st.pyplot(plt)

# Pertanyaan 3: Pengaruh Suhu, Kelembapan, dan Kecepatan Angin
st.header("Pengaruh Suhu, Kelembapan, dan Kecepatan Angin terhadap Penyewaan Sepeda Harian")
st.subheader("Rentals vs Temperature (Daily)")
plt.figure(figsize=(10, 6))
sns.scatterplot(data=filtered_data, x='temp_daily', y='cnt_daily')
plt.title('Rentals vs Temperature (Daily)')
st.pyplot(plt)

st.subheader("Rentals vs Humidity (Daily)")
plt.figure(figsize=(10, 6))
sns.scatterplot(data=filtered_data, x='hum_daily', y='cnt_daily')
plt.title('Rentals vs Humidity (Daily)')
st.pyplot(plt)

st.subheader("Rentals vs Wind Speed (Daily)")
plt.figure(figsize=(10, 6))
sns.scatterplot(data=filtered_data, x='windspeed_daily', y='cnt_daily')
plt.title('Rentals vs Wind Speed (Daily)')
st.pyplot(plt)
